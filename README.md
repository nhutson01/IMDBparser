# IMDBparser
IMDB web scraper using Python and the Beautiful Soup library for extracting data.
Retrieves information on movie title, genres, age rating, director, stars, description, Metascore rating, IMDB rating, and storyline. 
Features include ability to search for movie by title or keywords, create custom movie lists, save them to a file, import movie lists, 
obtain list of movies currently in theaters, obtain list of movies by month/year they were released, 
and ability to produce graphs of the Metascore ratings of any list and optionally save those graphs to a file.

While I realize that IMDB has datasets that are available to download at https://datasets.imdbws.com/, I wanted to learn
more about web scraping, and I like movies so I made a web scraper for IMDB.

Dependencies: Beautiful Soup 4, requests, Pandas, Numpy, Matplotlib, re, unidecode, warnings
