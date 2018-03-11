#!/bin/bash

# Chris Joakim, Microsoft, 2018/03/11
# ./cosmos_graph.sh > tmp/cosmos_graph.log

dbname=dev
collname=movies
drop_graph=0
create_drop_and_load_queries=1
execute_drop_and_load_queries=0

if [ $drop_graph -gt 0 ]
then
    echo 'python: drop_graph ...'
    python cosmos_graph.py drop_graph $dbname $collname
fi

if [ $create_drop_and_load_queries -gt 0 ]
then
    echo 'python: create_drop_and_load_queries ...'
    python cosmos_graph.py create_drop_and_load_queries $dbname $collname
fi

if [ $execute_drop_and_load_queries -gt 0 ]
then
    echo 'python: execute_drop_and_load_queries ...'
    python cosmos_graph.py execute_drop_and_load_queries $dbname $collname
fi

echo 'done'
