#!/bin/sh

module load python/3.6.6
for meth in umap pca fa lda mctsne fica lle isomap scscope; do 
for npoints in 1000 5000 10000 50000 100000 500000 1000000; do

    echo $meth $npoints
    timeout 12h python3 src/generate_embedding.py --method $meth --dataset mouse --dims 10 --njobs 24 > logs/mouse_timings/${meth}-${npoints}.log 2>&1

done
done
