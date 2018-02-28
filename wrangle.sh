#!/bin/bash

# Chris Joakim, Microsoft, 2018/02/28

extract_top_ratings=1
extract_movies=1
extract_principals=1
extract_people=0

footloose=tt0087277
prettywoman=tt0100405
kevinbacon=nm0000102
juliaroberts=nm0000210

if [ $extract_top_ratings -gt 0 ]
then
    echo 'python: extract_top_ratings ...'
    python wrangle.py extract_top_ratings
    # inspect the file created above python process
    wc   $IMDB_DATA_DIR/processed/top_ratings.csv
    head $IMDB_DATA_DIR/processed/top_ratings.csv
    cat  $IMDB_DATA_DIR/processed/top_ratings.csv | grep $footloose
    cat  $IMDB_DATA_DIR/processed/top_ratings.csv | grep $prettywoman
fi

if [ $extract_movies -gt 0 ]
then
    echo 'python: extract_movies ...'
    python wrangle.py extract_movies
    # inspect the file created above python process
    wc   $IMDB_DATA_DIR/processed/movies.csv
    head $IMDB_DATA_DIR/processed/movies.csv
    echo 'grep by movie id for footloose and pretty woman'
    cat  $IMDB_DATA_DIR/processed/movies.csv | grep $footloose
    cat  $IMDB_DATA_DIR/processed/movies.csv | grep $prettywoman
    echo 'grep by movie title for Footloose, Pretty, Blade'
    cat  $IMDB_DATA_DIR/processed/movies.csv | grep Footloose
    cat  $IMDB_DATA_DIR/processed/movies.csv | grep Pretty
    cat  $IMDB_DATA_DIR/processed/movies.csv | grep Blade
fi

if [ $extract_principals -gt 0 ]
then
    echo 'python: extract_principals ...'
    python wrangle.py extract_principals
    wc   $IMDB_DATA_DIR/processed/principals.csv
    head $IMDB_DATA_DIR/processed/principals.csv
    echo 'grep for principals in footloose'
    cat  $IMDB_DATA_DIR/processed/principals.csv | grep $footloose
    echo 'grep for principals in prettywoman'
    cat  $IMDB_DATA_DIR/processed/principals.csv | grep $prettywoman
    echo 'grep for kevinbacon'
    cat  $IMDB_DATA_DIR/processed/principals.csv | grep $kevinbacon
    echo 'grep for juliaroberts'
    cat  $IMDB_DATA_DIR/processed/principals.csv | grep $juliaroberts
fi

if [ $extract_people -gt 0 ]
then
    echo 'python: extract_people ...'
    python wrangle.py extract_people
    inspect the file created above python process
    # inspect the file created above python process
    wc   $IMDB_DATA_DIR/processed/people.csv
    head $IMDB_DATA_DIR/processed/people.csv
    cat  $IMDB_DATA_DIR/processed/people.csv | grep tt0100405
fi

echo 'done'

# === Notes ===

# 20000 votes -> 4994 movies           -> 183864 people
# 50000 votes -> 2815 movies -> xxx principals

# cat $IMDB_DATA_DIR/processed/title.ratings.tsv    | grep tt0087277
# tt0087277   6.5 58820

# cat $IMDB_DATA_DIR/processed/title.basics.tsv     | grep tt0087277
# tt0087277   movie   Footloose   Footloose   0   1984    \N  107 Drama,Music,Romance

# cat $IMDB_DATA_DIR/processed/title.basics.tsv     | grep tt0087277
# cat $IMDB_DATA_DIR/processed/title.principals.tsv | grep tt0087277
# cat $IMDB_DATA_DIR/processed/name.basics.tsv      | grep tt0087277  | grep Bacon
# nm0000102   Kevin Bacon 1958    \N  actor,producer,soundtrack   tt0087277,tt0164052,tt0327056,tt0361127


