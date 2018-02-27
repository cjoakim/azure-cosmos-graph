#!/bin/bash

# Chris Joakim, Microsoft, 2018/02/27

python wrangle.py extract_top_ratings

head /Users/cjoakim/Downloads/imdb/top_ratings.csv
wc   /Users/cjoakim/Downloads/imdb/top_ratings.csv

# python wrangle.py extract_top_movies

# wc /Users/cjoakim/Downloads/imdb/top_movies.csv

echo 'done'
