#!/bin/sh
#$ -q tmp.q
#$ -cwd
#$ -pe mpi 2

module load python/3.6.6

python3 -u src/optimal_dbscan.py $dataset $method
