#!/bin/sh

if [ ! -f $1 ];then
    echo "Couldn't find $1"
    exit 1
fi

for line in $(cat $1); do
    dataset=$(echo $line|cut -d'/' -f1)
    counts=$(echo $line|cut -d'/' -f2)
    method=$(echo $line|cut -d'/' -f3)
    dims=$(echo $line|cut -d'.' -f1|rev|cut -d'/' -f1|rev)
    full_ds=${counts}_${dataset}
    old_log=$(echo $line|sed 's/log$/old_log/')
    mv data/embeddings/$line data/embeddings/$old_log
    qsub -cwd -pe mpi 12 -binding linear:4 -q tmp.q -N run -o "data/embeddings/$line" -j y -v dataset=$full_ds,method=$method,dims=$dims,name=$dims,outdir="data/embeddings/$(echo $line|cut -d'/' -f1-3)",njobs=4 scripts/run_generate_embedding.sh
done 
