#!/bin/bash

# Chris Joakim, Microsoft, 2018/02/28

extract_top_ratings=0
extract_movies=0
extract_principals=0
extract_people=0
derive_people_edges=1

footloose=tt0087277
prettywoman=tt0100405
kevinbacon=nm0000102
juliaroberts=nm0000210
richardgere=nm0000152

if [ $extract_top_ratings -gt 0 ]
then
    echo 'python: extract_top_ratings ...'
    python wrangle.py extract_top_ratings
    # inspect the file created in the above python process
    wc   $IMDB_DATA_DIR/processed/top_ratings.csv
    head $IMDB_DATA_DIR/processed/top_ratings.csv
    cat  $IMDB_DATA_DIR/processed/top_ratings.csv | grep $footloose
    cat  $IMDB_DATA_DIR/processed/top_ratings.csv | grep $prettywoman
fi

if [ $extract_movies -gt 0 ]
then
    echo 'python: extract_movies ...'
    python wrangle.py extract_movies
    # inspect the files created in the above python process
    wc   $IMDB_DATA_DIR/processed/movies.csv
    head $IMDB_DATA_DIR/processed/movies.csv
    echo 'grep by movie id for footloose and pretty woman'
    cat  $IMDB_DATA_DIR/processed/movies.csv | grep $footloose
    cat  $IMDB_DATA_DIR/processed/movies.csv | grep $prettywoman
    echo 'grep by movie title for Footloose, Pretty, Blade'
    cat  $IMDB_DATA_DIR/processed/movies.csv | grep Footloose
    cat  $IMDB_DATA_DIR/processed/movies.csv | grep Pretty
    cat  $IMDB_DATA_DIR/processed/movies.csv | grep Blade
    wc   $IMDB_DATA_DIR/processed/movies.csv
fi

if [ $extract_principals -gt 0 ]
then
    echo 'python: extract_principals ...'
    python wrangle.py extract_principals
    # inspect the file created in the above python process
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
    # inspect the files created in the above python process
    wc   $IMDB_DATA_DIR/processed/people.csv
    head $IMDB_DATA_DIR/processed/people.csv
    cat  $IMDB_DATA_DIR/processed/people.csv | grep $kevinbacon
    cat  $IMDB_DATA_DIR/processed/people.csv | grep $juliaroberts
    wc   $IMDB_DATA_DIR/processed/people.json
fi

if [ $derive_people_edges -gt 0 ]
then
    echo 'python: derive_people_edges ...'
    python wrangle.py derive_people_edges
    wc   $IMDB_DATA_DIR/processed/people_edges.json
    cat  $IMDB_DATA_DIR/processed/people_edges.json | grep $juliaroberts | grep $richardgere
fi

echo 'done'
