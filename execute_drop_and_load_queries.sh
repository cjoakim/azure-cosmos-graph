#!/bin/bash

# Chris Joakim, Microsoft, 2018/03/11
# ./execute_drop_and_load_queries.sh

dbname=dev
collname=movies2

python cosmos_graph.py execute_drop_and_load_queries $dbname $collname

echo 'done'
