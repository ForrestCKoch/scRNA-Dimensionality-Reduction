#!/bin/sh
###############################################################################
# generate_all_embeddings.sh
#
# Submission script for generating each of the embeddings
###############################################################################

#for m in pca umap mctsne lda lle isomap fa fica nmf spectral zifa; do  # methods
for m in vasc; do
for d in $(ls data/datasets/pddf|cut -d'.' -f1); do # datasets
for e in 2 4 8 16 32 48 96; do # dimensions
    ds=$(echo $d|cut -d'_' -f2-) # extract dataset name from file
    c=$(echo $d|cut -d'_' -f1)   # extract count type (normcounts, logcounts, etc ...) 
    o="data/embeddings/$ds/$c/$m" # output directory
    mkdir -p $o/logs
    logfile="$o/logs/${e}.log"
    echo -e "$m\t\t$d\t\t$e"
    /usr/bin/time -v python3.6 src/generate_embedding.py --dataset $d --method $m --outdir $o --trial-name $e --dims $e > $logfile 2>&1
done
done
done
