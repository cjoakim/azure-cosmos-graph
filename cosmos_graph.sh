#!/bin/bash

# Chris Joakim, Microsoft, 2018/02/28

drop_graph=1

if [ $drop_graph -gt 0 ]
then
    echo 'python: drop_graph ...'
    python cosmos_graph.py drop_graph test movies
fi

echo 'done'
