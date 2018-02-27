#!/bin/bash

# Chris Joakim, Microsoft, 2018/02/27

python wrangle.py extract_top_ratings
# inspect the file created above python process
head /Users/cjoakim/Downloads/imdb/top_ratings.csv
wc   /Users/cjoakim/Downloads/imdb/top_ratings.csv

python wrangle.py extract_top_movies
# inspect the file created above python process
head /Users/cjoakim/Downloads/imdb/top_movies.csv
wc   /Users/cjoakim/Downloads/imdb/top_movies.csv
cat  /Users/cjoakim/Downloads/imdb/top_movies.csv | grep Footloose
cat  /Users/cjoakim/Downloads/imdb/top_movies.csv | grep Pretty
cat  /Users/cjoakim/Downloads/imdb/top_movies.csv | grep Blade

python wrangle.py extract_people
# inspect the file created above python process
wc  /Users/cjoakim/Downloads/imdb/people.csv
cat /Users/cjoakim/Downloads/imdb/people.csv | grep tt0100405

# tt0100405": "Pretty Woman"

# 20000 votes -> 4994 movies -> 183864 people
# 30000 votes -> xxx movies  -> xxx people

echo 'done'
