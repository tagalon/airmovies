# airmovies
The goal of Airmovies is to deploy a web application that allows users to search through airline movie entertainment catalogs, 
in which users can search by multiple parameters, inclusive with genre and airline. The idea of this project is to build it around
Elasticsearch and implement the Search UI using React or Python as I need great help on being able to build React components.

- Done
  - Built universal webscraper for airline entertainment catalogs
  - Able to ingest data into Elastic Cluster and make REST API calls
  - Able to filter data from Elastic Cluster using REST API calls 

- Not Done
  - Building front-end web interface with React and TailwindCSS (Main Goal)
  - Ingesting all the data from every airline
  - Accounting for all the titles that haven't been ingested

Explanation of every file

scrape.py - universal webscraper utilizing BS4
webscrape.py - init webscraper for dynamic websites (yet to see for the need)
esponse.py - connecting to ES cluster and making GET REST API calls with filter
example.ini - ES cluster configuration information
data.json & movie_data.json - structured/unstructured format of the data

- How To Webscrape -
  - Dynamic Webpages
  - Static Webpages



Refer to OMDB API to understand the values of the parameters if not understandable
- {"42": 
  - {"Title": "42", 
  - "Year": "2013", 
  - "Rated": "PG-13", 
  - "Released": "12 Apr 2013", 
  - "Runtime": "128 min", 
  - "Genre": ["Biography", " Drama", " Sport"], 
  - "Director": "Brian Helgeland", 
  - "Writer": "Brian Helgeland", 
  - "Actors": "Chadwick Boseman, T.R. Knight, Harrison Ford", 
  - "Plot": "In 1947, Jackie Robinson becomes the first African-American to play in Major League Baseball in the modern era when he was         - signed by the Brooklyn Dodgers and faces considerable racism in the process.", 
  - "Language": "English", 
  - "Country": "United States",
  -  "Awards": "3 wins & 21 nominations", 
  -  "Poster": "https://m.media-amazon.com/images/M/MV5BMTQwMDU4MDI3MV5BMl5BanBnXkFtZTcwMjU1NDgyOQ@@._V1_SX300.jpg", 
  - "Ratings": 
   - [{"Source": "Internet Movie Database", "Value": "7.5/10"}, 
   - {"Source": "Rotten Tomatoes", "Value": "81%"}, 
   - {"Source": "Metacritic", "Value": "62/100"}]
  - "Metascore": "62", 
  - "imdbRating": "7.5", 
  - "imdbVotes": "98,394", 
  - "imdbID": "tt0453562", 
  - "Type": "movie", 
  - "DVD": "16 Jul 2013", 
  - "BoxOffice": "$95,059,709", 
  - "Production": "N/A", 
  - "Website": "N/A", 
  - "Response": "True", 
  - "Airline": ["AA"]}
