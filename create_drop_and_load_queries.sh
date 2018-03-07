#!/bin/bash

# Chris Joakim, Microsoft, 2018/03/07
# ./create_drop_and_load_queries.sh

dbname=test
collname=movies
outfile=/Users/cjoakim/github/cj_data/imdb/processed/drop_and_load_queries.txt

rm $outfile

python cosmos_graph.py create_drop_and_load_queries $dbname $collname

wc  $outfile

echo 'movie count'  ; cat $outfile | grep movie | wc -l
echo 'person count' ; cat $outfile | grep person | wc -l
echo 'knows count'  ; cat $outfile | grep knows | wc -l
echo 'julia count'  ; cat $outfile | grep nm0000210 | wc -l

echo 'done'
