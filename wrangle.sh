#!/bin/bash

# Chris Joakim, Microsoft, 2018/02/27

python wrangle.py extract_top_ratings
# inspect the file created above python process
head /Users/cjoakim/Downloads/imdb/top_ratings.csv
wc   /Users/cjoakim/Downloads/imdb/top_ratings.csv
cat  /Users/cjoakim/Downloads/imdb/top_ratings.csv | grep tt0087277

python wrangle.py extract_top_movies
# inspect the file created above python process
head /Users/cjoakim/Downloads/imdb/top_movies.csv
wc   /Users/cjoakim/Downloads/imdb/top_movies.csv
cat  /Users/cjoakim/Downloads/imdb/top_movies.csv | grep tt0087277
cat  /Users/cjoakim/Downloads/imdb/top_movies.csv | grep Footloose
cat  /Users/cjoakim/Downloads/imdb/top_movies.csv | grep Pretty
cat  /Users/cjoakim/Downloads/imdb/top_movies.csv | grep Blade

python wrangle.py extract_top_principals
head /Users/cjoakim/Downloads/imdb/top_principals.csv
wc   /Users/cjoakim/Downloads/imdb/top_principals.csv

# ===
# python wrangle.py extract_people
# inspect the file created above python process
# # inspect the file created above python process
# wc  /Users/cjoakim/Downloads/imdb/people.csv
# cat /Users/cjoakim/Downloads/imdb/people.csv | grep tt0100405

# tt010040   Pretty Woman
# tt0087277  Footloose

# 20000 votes -> 4994 movies           -> 183864 people
# 50000 votes -> 2815 movies -> xxx principals

# cat /Users/cjoakim/Downloads/imdb/title.ratings.tsv    | grep tt0087277
# tt0087277   6.5 58820

# cat /Users/cjoakim/Downloads/imdb/title.basics.tsv     | grep tt0087277
# tt0087277   movie   Footloose   Footloose   0   1984    \N  107 Drama,Music,Romance

# cat /Users/cjoakim/Downloads/imdb/title.basics.tsv     | grep tt0087277
# cat /Users/cjoakim/Downloads/imdb/title.principals.tsv | grep tt0087277
# cat /Users/cjoakim/Downloads/imdb/name.basics.tsv      | grep tt0087277  | grep Bacon
# nm0000102   Kevin Bacon 1958    \N  actor,producer,soundtrack   tt0087277,tt0164052,tt0327056,tt0361127

echo 'done'
