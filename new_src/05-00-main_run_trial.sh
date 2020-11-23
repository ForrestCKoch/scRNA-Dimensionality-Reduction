#!/bin/sh
#
# Runs one of the the queues prepared by Step 04.

queuefile=$1
dims=$(echo $1|rev|cut -d'/' -f1|rev|cut -d'.' -f1)
method=$(echo $1|cut -d'/' -f5)
metric=$(echo $1|cut -d'/' -f6)
count=$(echo $1|cut -d'/' -f4)
dataset=$(echo $1|cut -d'/' -f3)

pkl="data/embeddings/$dataset/$count/$method/${dims}.pkl"
logdir=data/results/dbscan/${dataset}/$count/$method/$metric
mkdir -p $logdir

#echo $queuefile
python3 -u src/run_dbscan_trials.py $pkl $queuefile >> $logdir/${dims}.csv
