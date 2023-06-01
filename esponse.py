import configparser
from elasticsearch import Elasticsearch
# from elasticsearch_dsl import Search
import warnings

def filterMovieResponse():
    config = configparser.ConfigParser()
    config.read('example.ini')
    client = Elasticsearch(cloud_id=config['ELASTIC']['cloud_id'], http_auth=(config['ELASTIC']['user'], config['ELASTIC']['password']))
    resp = client.search(query={"terms": {"Airline": ["AA"]}, "terms": {"Genre": ["Drama"]}},)
    print(resp)
filterMovieResponse()   