#!/bin/bash

# Execute several queries of the CosmosDB/GraphDB and capture their output
# to several txt files in the queries/ directory.
#
# Run with:
#   ./queries.sh
#
# Chris Joakim, Microsoft, 2018/03/11

dbname=dev
collname=movies

echo 'using database:   '$dbname
echo 'using collection: '$collname

echo 'removing the output files ...'
rm queries/*.txt

###

echo 'querying countv ...'
python cosmos_graph.py query $dbname $collname countv > queries/countv.txt

###

echo 'querying movie footloose ...'
python cosmos_graph.py query $dbname $collname movie footloose > queries/movie_footloose.txt

echo 'querying movie pretty_woman ...'
python cosmos_graph.py query $dbname $collname movie pretty_woman > queries/movie_pretty_woman.txt

###

echo 'querying person kevin_bacon ...'
python cosmos_graph.py query dev movies person   kevin_bacon > queries/person_kevin_bacon.txt

echo 'querying person richard_gere ...'
python cosmos_graph.py query dev movies person   richard_gere > queries/person_richard_gere.txt

echo 'querying person julia_roberts ...'
python cosmos_graph.py query dev movies person   julia_roberts > queries/person_julia_roberts.txt

echo 'querying person nm0001742 (Lori Singer) ...'
python cosmos_graph.py query dev movies person   nm0001742 > queries/person_nm0001742.txt

###

echo 'querying movies that kevin_bacon was in ...'
python cosmos_graph.py query dev movies in kevin_bacon > queries/kevin_bacon_in.txt

echo 'querying movies that julia_roberts was in ...'
python cosmos_graph.py query dev movies in julia_roberts > queries/julia_roberts_in.txt

echo 'querying movies that richard_gere was in ...'
python cosmos_graph.py query dev movies in richard_gere > queries/richard_gere_in.txt

echo 'querying movies that diane_lane was in ...'
python cosmos_graph.py query dev movies in diane_lane > queries/diane_lane_in.txt

echo 'querying movies that lori_singer was in ...'
python cosmos_graph.py query dev movies in lori_singer > queries/lori_singer_in.txt

###

echo 'querying people that kevin_bacon knows ...'
python cosmos_graph.py query dev movies knows kevin_bacon > queries/kevin_bacon_knows.txt

echo 'querying people that julia_roberts knows ...'
python cosmos_graph.py query dev movies knows julia_roberts > queries/julia_roberts_knows.txt

echo 'querying people that richard_gere knows ...'
python cosmos_graph.py query dev movies knows richard_gere > queries/richard_gere_knows.txt

echo 'querying people that lori_singer knows ...'
python cosmos_graph.py query dev movies knows lori_singer > queries/lori_singer_knows.txt

echo 'querying people that diane_lane knows ...'
python cosmos_graph.py query dev movies knows diane_lane > queries/diane_lane_knows.txt

###

echo 'querying path from richard_gere to julia_roberts ...'
python cosmos_graph.py query dev movies path richard_gere julia_roberts > queries/path_richard_gere_to_julia_roberts.txt

echo 'querying path from richard_gere to kevin_bacon ...'
python cosmos_graph.py query dev movies path richard_gere kevin_bacon > queries/path_richard_gere_to_kevin_bacon.txt

echo 'querying path from richard_gere to lori_singer ...'
python cosmos_graph.py query dev movies path richard_gere lori_singer > queries/path_richard_gere_to_lori_singer.txt

echo 'done'
