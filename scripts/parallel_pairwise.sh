#!/bin/sh

dataset=$(echo $1|cut -d'.' -f1)
counts=$(echo $1|cut -d'.' -f3)
metric=$(echo $1|cut -d'.' -f2)
echo $1
python3 scripts/measure_pairwise_distances.py $metric $counts $dataset
