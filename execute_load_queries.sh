#!/bin/bash

# Chris Joakim, Microsoft, 2018/03/11
# ./execute_load_queries.sh

dbname=dev
collname=movies

python cosmos_graph.py execute_load_queries $dbname $collname

echo 'done'