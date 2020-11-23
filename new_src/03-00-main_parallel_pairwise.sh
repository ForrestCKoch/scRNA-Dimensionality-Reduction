#!/bin/sh

# this script should be called as:
#   cat new_src/03-00-b_parallel_pairwise_args.txt | xargs -n 1 bash new_src/03-00-main_parallel_pairwise.sh 
dataset=$(echo $1|cut -d'.' -f1)
counts=$(echo $1|cut -d'.' -f3)
metric=$(echo $1|cut -d'.' -f2)
#echo $1
#python3 scripts/measure_pairwise_distances.py $metric $counts $dataset
python3 new_src/03-00-a_measure_pairwise_distances.py $metric $counts $dataset
