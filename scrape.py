import os, uuid
import re
import time
import json
import requests
from elasticsearch import Elasticsearch, helpers
import configparser
import datetime
from requests.auth import HTTPBasicAuth

username = 'elastic'
password = '7ovLivoSD4kegggL1MJTToKq'

response = requests.get('http://localhost:9200', auth = HTTPBasicAuth(username, password))
print(response.content)


air_movie_data, apiKey = {}, 'd44cc6dc'
AA_URL = "https://entertainment.aa.com/api/proxy/request?api=/film/&resource=buckets/69/films&lang=en&flightdate=&flightsystem=&routes=&services=&type=Movies&page=1&pageSize=600&orderBy=titleasc&subsId=&dubsId="
AirCanada_URL = "https://entertainment.aircanada.com/api/proxy/request?api=/film/&resource=buckets/47/films&lang=en&flightdate=&flightsystem=&routes=&services=&type=Movies&page=1&pageSize=480&orderBy=yeardesc&subsId=&dubsId="
BritishAirways_URL = "https://entertainment.ba.com/api/proxy/request?api=/film/&resource=buckets/68/films&lang=en&flightdate=&flightsystem=&routes=&services=&type=Undefined&page=1&pageSize=60&orderBy=titleasc&subsId=&dubsId="
URL_List = [AA_URL, AirCanada_URL, BritishAirways_URL]
URL_Properties = ["AA", "AC", "BA"]
# Calling OMDB API for movie ratings/reviews and correspondly appending info to the matched movie
DeltaAirlines_URL = "https://www.delta.com/us/en/onboard/inflight-entertainment/current-movies"

# Needs Selenium
EmiratesAirlines_URL = "https://www.emirates.com/service/exp/ice?date=2023-05-18&group=movies"
AlaskAirlines_URL = "https://api.themoviedb.org/4/list/104189?api_key=a1b011e727b03fda91b225838563b27b&sort_by=title.asc&language=en-US&page=1"
#JetBlue uses Amazon, need to do more research about that flight

SouthwestAirlines_URL= "https://www.southwest.com/inflight-entertainment-portal/"
 
def filterMovieTitle(title):
    # a = ['Your Turn to Kill: The Movie\n' , 'Frozen (2013)', 'Valeria Mithatenet (Valeria is Getting Married)\n']
    # Need to figure out proper regex expression to filter out text
    if '\n' in title:
        title = title[:len(title)-1]
    if "(" in title and ")" in title:
        title = re.sub("\(.*?\)","()", title)
        arrtitle = title.split()
        arrtitle = arrtitle[0:len(arrtitle) - 1]
        title = ' '.join(arrtitle)
    return title

movieTitles = {}
def multiscrapURL(urls, props):
    for i in range(len(urls)):
        f = requests.get(urls[i])
        rawMovieData = json.loads(f.text)
        for movie in rawMovieData["data"]:
            movieTitle = filterMovieTitle(movie["title"])
            keyMovieInfo = (movieTitle, str(movie["year"]))
            if keyMovieInfo in movieTitles:
                if props[i][0] == ' ':
                    props[i] = props[i][1:]
                movieTitles[keyMovieInfo].append(props[i])
            else:
                movieTitles[keyMovieInfo] = [props[i]] 
    return movieTitles

def checkMultipleGenres(query):
    if " " in query["Genre"]:
        query["Genre"] = query["Genre"].split(',')
    else:
        query["Genre"] = [query["Genre"]]
    return query

def scrapeMovies():
    failedTitles = []
    movieProps = multiscrapURL(URL_List, URL_Properties)

    for movie in movieProps:
        movieTitle, year, props = movie[0], movie[1], movieTitles[movie]
        # movieTitle, year = movieInfo[0], movieInfo[1]
        data_URL = 'http://www.omdbapi.com/?t='+movieTitle+'&y='+year+'&apikey='+apiKey
        metaQuery = requests.get(data_URL).json()
        if metaQuery["Response"] == "True":
            metaQuery['Airline'] = props
            air_movie_data[metaQuery["Title"]] = checkMultipleGenres(metaQuery)
        elif metaQuery["Response"] == "False":
            failedTitles.append((movieTitle, year))
    return failedTitles

def loadJSONMovies():

    # Setting up ElasticSearch Configuration to API
    config = configparser.ConfigParser()
    config.read('example.ini')
    # build_doc = {}
    # build_doc["_index"] = "am-movies"
    # build_doc["_id"] = 12345
    # build_doc["doc_type"]
    # build_doc["_source"] = str(air_movie_data)

    es = Elasticsearch(cloud_id=config['ELASTIC']['cloud_id'], basic_auth=(config['ELASTIC']['user'], config['ELASTIC']['password']))

    # actions = [{"_id" : uuid.uuid4(), "doc_type" : "movies", "doc": air_movie_data}
    # for doc in range(100)]
     
    mapping = {}
    data = json.dumps(air_movie_data)
    with open("data.json", "w") as outfile:
        outfile.write(data)
    
    def script_path():
        path = os.path.dirname(os.path.realpath(__file__))
        if os.name == 'posix': # posix is for macOS or Linux
            path = path + "/"
        else:
            path = path + chr(92) # backslash is for Windows
        return path

    def get_data_from_file(file_name):
        if "/" in file_name or chr(92) in file_name:
            file = open(file_name, encoding="utf8", errors='ignore')
        else:
        # use the script_path() function to get path if none is passed
            file = open(script_path() + str(file_name), encoding="utf8", errors='ignore')
        data = [line.strip() for line in file]
        file.close()
        return data
    
    def bulk_json_data(json_file, _index, doc_type):
        json_list = get_data_from_file(json_file)
        for doc in json_list:
            # use a `yield` generator so that the data
            # isn't loaded into memory
            if "{Title" not in doc:
                yield {
                    "_index": _index,
                    "_id": uuid.uuid4(),
                    "_source": doc
                }
        return

    try:
    # make the bulk call, and get a response
        # response = helpers.bulk(es, bulk_json_data("data.json", "am-movies", "movies"))
        response = es.index(
            #Index name in Kibana
            index = 'search-movies',
            document = data
        )
    #response = helpers.bulk(elastic, actions, index='employees', doc_type='people')
        print ("\nRESPONSE:", response)
    except Exception as e:
        print("\nERROR:", e)

    # try:
    # # create JSON string of doc _source data
    #     json_source = json.dumps(build_doc["source"])

    # # get the dict object's _id
    #     json_id = build_doc["id"]
    #     build_doc["source"] = json_source
    # # make an API call to the Elasticsearch cluster
    #     response = es.index(
    #         #Index name in Kibana
    #         index = 'search-am',
    #         document = json_source
    #     )
    #     print
    #     # print a pretty response to the index() method call response
    #     print ("\nclient.index response:", json.dumps(response, indent=4))
    # except Exception as error:
    #     print ("Error type:", type(error))
    #     print ("client.index() ERROR:", error)
    # print(es.info)

    # print ("\nbuild_doc items:", build_doc.items())

    # es.index(index="my-index-000001", document=air_movie_data.values())
    # helpers.bulk(es, json_str)

    # all_docs = {}
    # all_docs["size"] = 9999
    # all_docs["query"] = {"match_all" : {}}
    # print ("\nall_docs:", all_docs)
    # print ("all_docs TYPE:", type(all_docs))


    # try:
    #     # pass the JSON string in an API call to the Elasticsearch cluster
    #     response = es.search(
    #     index = "some_index",
    #     body = all_docs
    #     )

    #     # print all of the documents in the Elasticsearch index
    #     print ("all_docs query response:", response)

    #     # use the dumps() method's 'indent' parameter to print a pretty response
    #     print ("all_docs pretty:", json.dumps(response, indent=4))

    # except Exception as error:
    #     print ("Error type:", type(error))
    #     print ("client.search() ValueError for JSON object:", error)

    #Testing for proper JSON Format

# Ingests movies into ElasticSearch
    
failCount = scrapeMovies()
# print("Total Movie Count:" + str(len(movieTitles)))
# print("Total Filtered:" + str(len(air_movie_data)))
loadJSONMovies()
# Elasticsearch

