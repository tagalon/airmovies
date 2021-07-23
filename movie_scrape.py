from bs4 import BeautifulSoup
import requests
import json
import mysql.connector

# db = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   passwd="rahul!",
#   database="testdatabase"
# )

# mycursor = db.cursor()

apiKey ='d44cc6dc'
url = 'https://entertainment.aa.com/en/film/results/15114-15117-Allmoviesvariesbyaircraft?orderBy=titleasc&previousPageId=1051'
source = requests.get(url)
def get_html (url):
    try:
        r = requests.get(url)
        return r.text
    except requests.exceptions.TooManyRedirects:
        pass

l = [None] * 1000 # Make a list of 1000 None's
x = range (1000)
for i in x:
    # baz
    l[i] = None
    # qux

movies_dict = {}
movies_string = ""
movies_int_dict = {}
index = 0
with open('movies.html') as html_file:
	soup = BeautifulSoup(html_file, "lxml")
	for movie in soup.find_all('h3'):
		movie_title = movie.text
		data_URL = 'http://www.omdbapi.com/?t='+movie_title+'&apikey='+apiKey
		year = ''
		response = requests.get(data_URL).json()
		response['Airline'] = 'AA'
		if response != None:
			movies_dict[str(movie_title)] = response
			movies_int_dict[index] = movie_title
			index += 1
			# movies_string += " " +movie_title
		else:
			break;
# input_format = '''(INSERT INTO testdatabase.tbluser 
# 				(Title, Year, Rated, Released, Runtime, Genre, Director, Writer, Actors, Plot, Language, Country, Awards, Poster, Ratings, Metascore, imdbRating, imdbVotes, imdbID, Type, DVD, BoxOffice, Production, Website, Response, Airline) 
# 				VALUES (%(Title)s, %(Year)s, %(Rated)s, %(Released)s, %(Runtime)s, %(Genre)s, %(Director)s, %(Writer)s, %(Actors)s %(Plot)s, %(Language)s, %(Country)s, %(Awards)s, %(Poster)s, %(Ratings)s, %(Metascore)s, %(imdbRating)s, %(imdbVotes)s, %(imdbID)s, %(Type)s, %(DVD)s, %(BoxOffice)s, %(Production)s, %(Website)s, %(Response)s, %(Airline)s))'''row_tuple

iter_count = 0
source_names = ['Internet Movie Database', 'Rotten Tomatoes', 'Metacritic']
for index in range(0, len(movies_int_dict)):
	movie_index = movies_int_dict[index]
	insert_movie_dict = movies_dict[movie_index]
	# print(len(insert_movie_dict))
	row_list = []
	for meta_property in insert_movie_dict.values():
		# placeholders = ', '.join(['%s'] * len(insert_movie_dict))
		# columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in insert_movie_dict.keys())
		# values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in insert_movie_dict.values())
		if type(meta_property) == list:
			source_properties = []
			for item in meta_property:
				if type(item) == dict:
					for element in item.values():
						try:
							int(element[0])
						except ValueError:
							source_properties.append(element)
							source_properties.append(item['Value'])
			for name in source_names:
				if name not in source_properties:
					source_properties.append(name)
					source_properties.append('N/A')
			row_list.extend(source_properties)
		else:
			row_list.append(meta_property)
	row_tuple = tuple(row_list)
	input_format = '''INSERT INTO omdb_sql
				(Title, Year, Rated, Released, Runtime, Genre, Director, Writers, Actors, Plot, Language, Country, Awards, Poster, imd, imdVal, Rotten, RottenVal, Meta, MetaVal, Metascore, imdbRating, imdbVotes, imdbID, Type, DVD, BoxOffice, Production, Website, Response, Airline) 
				VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
	# mycursor.execute(input_format, row_tuple)
g = open("test.txt", 'w')
g.write(str(row_tuple))

# mycursor.close()
# db.close()
# sql_file = open("C:/Users/Srinivasa/Documents/MovieProject/movie.sql", "a")
# sql_file.write(sql + '\n')


def index():
	return "<>"

# movies = div.find('h3', 'bucket__item').content

# movies = soup.find_all('div', class_='container globalanchorchk').p.text
# print(soup.prettify())