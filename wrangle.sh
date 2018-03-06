#!/bin/bash

# Chris Joakim, Microsoft, 2018/03/06

identify_candidate_movies=1
extract_top_ratings=0        # now obsolete in favor of identify_candidate_movies
extract_movies=1
extract_principals=1
extract_people=1
derive_people_edges=1

footloose=tt0087277
pretty_woman=tt0100405
bladerunner=tt0083658

kevin_bacon=nm0000102
julia_roberts=nm0000210
richard_gere=nm0000152
john_lithgow=nm0001475
tom_hanks=nm0000158
lori_singer=nm0001742
john_malkovich=nm0000518
dustin_hoffman=nm0000163
kevin_costner=nm0000126
holly_hunter=nm0000456
keanu_reeves=nm0000206
hilary_swank=nm0005476
charlize_theron=nm0000234
harrison_ford=nm0000148

if [ $identify_candidate_movies -gt 0 ]
then
    echo 'python: identify_candidate_movies ...'
    python wrangle.py identify_candidate_movies
    # inspect the file created in the above python process
    wc   $IMDB_DATA_DIR/processed/required_movies.csv
    head $IMDB_DATA_DIR/processed/required_movies.csv
fi

if [ $extract_top_ratings -gt 0 ]
then
    echo 'python: extract_top_ratings ...'
    python wrangle.py extract_top_ratings
    # inspect the file created in the above python process
    wc   $IMDB_DATA_DIR/processed/top_ratings.json
    head $IMDB_DATA_DIR/processed/top_ratings.json
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
    cat  $IMDB_DATA_DIR/processed/movies.csv | grep $pretty_woman
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
    echo 'grep for principals in pretty_woman'
    cat  $IMDB_DATA_DIR/processed/principals.csv | grep $pretty_woman
    echo 'grep for kevinbacon'
    cat  $IMDB_DATA_DIR/processed/principals.csv | grep $kevin_bacon
    echo 'grep for juliaroberts'
    cat  $IMDB_DATA_DIR/processed/principals.csv | grep $julia_roberts
fi

if [ $extract_people -gt 0 ]
then
    echo 'python: extract_people ...'
    python wrangle.py extract_people
    # inspect the files created in the above python process
    wc   $IMDB_DATA_DIR/processed/people.csv
    head $IMDB_DATA_DIR/processed/people.csv
    cat  $IMDB_DATA_DIR/processed/people.csv | grep $kevin_bacon
    cat  $IMDB_DATA_DIR/processed/people.csv | grep $julia_roberts
    wc   $IMDB_DATA_DIR/processed/people.json
fi

if [ $derive_people_edges -gt 0 ]
then
    echo 'python: derive_people_edges ...'
    python wrangle.py derive_people_edges
    wc   $IMDB_DATA_DIR/processed/people_edges.json
    echo 'juliaroberts entries:'
    cat  $IMDB_DATA_DIR/processed/people_edges.json | grep $julia_roberts
    echo 'juliaroberts and richardgere entries:'
    cat  $IMDB_DATA_DIR/processed/people_edges.json | grep $julia_roberts | grep $richard_gere
fi

echo 'done'
