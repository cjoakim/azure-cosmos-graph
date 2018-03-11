#!/bin/bash

# Chris Joakim, Microsoft, 2018/03/11
# ./create_drop_and_load_queries.sh

dbname=dev
collname=movies
outfile=data/processed/load_queries.txt

rm $outfile

python cosmos_graph.py create_load_queries $dbname $collname

wc  $outfile

echo 'done'
