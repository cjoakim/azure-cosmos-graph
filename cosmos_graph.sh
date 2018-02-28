#!/bin/bash

# Chris Joakim, Microsoft, 2018/02/28
# ./cosmos_graph.sh > tmp/cosmos_graph.log

dbname=test
collname=movies
drop_graph=0
drop_and_load=1

if [ $drop_graph -gt 0 ]
then
    echo 'python: drop_graph ...'
    python cosmos_graph.py drop_graph $dbname $collname
fi

if [ $drop_and_load -gt 0 ]
then
    echo 'python: drop_and_load ...'
    python cosmos_graph.py drop_and_load $dbname $collname
fi

echo 'done'
