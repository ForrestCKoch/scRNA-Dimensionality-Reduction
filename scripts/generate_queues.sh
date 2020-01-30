#!/bin/sh
# This script is intended to take a single line of the '.csv' produced by
# get_eps_bounds.py and will output a queue file for each of the 4 metrics
# 
# Suggested usage is 'cat data/results/eps_upperbounds.csv | head -n+2 | xargs -n1 -P 8 -I {} bash scripts/generate_queues.sh {}'

line="$1"

fn=$(echo $line|cut -d',' -f1)
euc=$(echo $line|cut -d',' -f2)
cor=$(echo $line|cut -d',' -f3)
cos=$(echo $line|cut -d',' -f4)
seu=$(echo $line|cut -d',' -f5)

dims=$(echo $fn|rev|cut -d'/' -f1|rev|cut -d'.' -f1)
queue_folder=$(echo $fn|rev|cut -d'/' -f2-|rev|sed 's/embeddings/queues/')

echo $fn

mkdir -p $queue_folder/euclidean
mkdir -p $queue_folder/seuclidean
mkdir -p $queue_folder/correlation
mkdir -p $queue_folder/cosine

python3 scripts/generate_trials.py $fn $euc euclidean > $queue_folder/euclidean/${dims}.queue
python3 scripts/generate_trials.py $fn $seu seuclidean > $queue_folder/seuclidean/${dims}.queue
python3 scripts/generate_trials.py $fn $cor correlation > $queue_folder/correlation/${dims}.queue
python3 scripts/generate_trials.py $fn $cos cosine > $queue_folder/cosine/${dims}.queue
