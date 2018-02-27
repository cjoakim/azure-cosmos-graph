#!/bin/bash

# Chris Joakim, Microsoft, 2018/02/27

python wrangle.py extract_top_ratings
head /Users/cjoakim/Downloads/imdb/top_ratings.csv
wc   /Users/cjoakim/Downloads/imdb/top_ratings.csv

python wrangle.py extract_top_movies
head /Users/cjoakim/Downloads/imdb/top_movies.csv
wc   /Users/cjoakim/Downloads/imdb/top_movies.csv

cat /Users/cjoakim/Downloads/imdb/top_movies.csv | grep Footloose
cat /Users/cjoakim/Downloads/imdb/top_movies.csv | grep Pretty
cat /Users/cjoakim/Downloads/imdb/top_movies.csv | grep Blade

echo 'done'
