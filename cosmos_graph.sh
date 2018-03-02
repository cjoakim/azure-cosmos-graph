#!/bin/bash

# Chris Joakim, Microsoft, 2018/03/02
# ./cosmos_graph.sh > tmp/cosmos_graph.log

dbname=test
collname=movies2
drop_graph=0
drop_and_load=1
count_query=0
query2=0
query3=0

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

if [ $count_query -gt 0 ]
then
    echo 'python: count_query ...'
    python cosmos_graph.py count_query $dbname $collname
fi

if [ $query2 -gt 0 ]
then
    echo 'python: query2 ...'
    python cosmos_graph.py query2 $dbname $collname
fi

if [ $query3 -gt 0 ]
then
    echo 'python: query3 ...'
    python cosmos_graph.py query3 $dbname $collname
fi

echo 'done'
