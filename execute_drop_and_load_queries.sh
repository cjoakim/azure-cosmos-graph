#!/bin/bash

# Chris Joakim, Microsoft, 2018/03/07
# ./execute_drop_and_load_queries.sh

dbname=test
collname=movies

python cosmos_graph.py execute_drop_and_load_queries $dbname $collname

echo 'done'
