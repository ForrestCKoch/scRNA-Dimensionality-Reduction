#!/bin/sh
###############################################################################
# generate_all_embeddings.sh
#
# Submission script for generating each of the embeddings
###############################################################################

#for m in pca umap mctsne lda lle isomap fa fica nmf spectral zifa; do  # methods
for m in phate; do  # methods
#for m in zifa; do 
for d in $(ls data/datasets/pddf|cut -d'.' -f1); do # datasets
for e in 2 4 8 16 32 48 96; do # dimensions
    ds=$(echo $d|cut -d'_' -f2-) # extract dataset name from file
    c=$(echo $d|cut -d'_' -f1)   # extract count type (normcounts, logcounts, etc ...) 
    o="data/embeddings/$ds/$c/$m" # output directory
    mkdir -p $o/logs
    logfile="$o/logs/${e}.log"
    qsub -cwd -pe mpi 4 -q long.q -N run -o $logfile -j y -v dataset=$d,method=$m,dims=$e,name=$e,outdir=$o,njobs=4 scripts/run_generate_embedding.sh
    #qsub -cwd -pe mpi 8 -q bigmem.q -N run -o $logfile -j y -v dataset=$d,method=$m,dims=$e,name=$e,outdir=$o,njobs=8 scripts/run_generate_embedding.sh
done
done
done
