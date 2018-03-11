#!/bin/bash

# Chris Joakim, Microsoft, 2018/03/11
# ./check_drop_and_load_queries.sh > tmp/check_drop_and_load_queries.txt

footloose=tt0087277
pretty_woman=tt0100405
kevin_bacon=nm0000102
lori_singer=nm0001742
julia_roberts=nm0000210
richard_gere=nm0000152
diane_lane=nm0000178

infile=data/processed/drop_and_load_queries.txt

echo '---'
echo 'grepping for footloose ...'
cat $infile | grep $footloose

echo '---'
echo 'grepping for kevin_bacon ...'
cat $infile | grep $kevin_bacon

echo '---'
echo 'grepping for lori_singer ...'
cat $infile | grep $lori_singer

echo '---'
echo 'grepping for julia_roberts ...'
cat $infile | grep $julia_roberts

echo '---'
echo 'grepping for richard_gere ...'
cat $infile | grep $richard_gere

echo '---'
echo 'grepping for diane_lane ...'
cat $infile | grep $diane_lane

echo 'done'
