#!/bin/sh

# This script is used to submit jobs to an SGE queue where each job
# is a different permuation of the settings we're exploring


#for dataset in koh kumar simk4easy simk4hard simk8hard zhengmix8eq zhengmix4eq; do
for dims in 2 3 4 5 8 10 15 25 30 35 40 45 50 60 70 80 90 100 125 150 175 200 225 250 300 350 400 450 500 600 700 800 900 1000 1250 1500 1750 2000 2250 2500; do
for dataset in "baron-human" campbell chen macosko marques shekhar; do
for meth in umap pca isomap lle spectral mds fa fica nmf lda mctsne; do 
for log in ' ' '--log1p'; do
    if [ "$log" == "--log1p" ]; then
        flag='true'
        x='True'
    else
        flag='false'
        x='False'
    fi

    logfile="logs/$dataset/${meth}_log-${flag}_dims-${dims}.log"
    if [ ! -f data/model/$dataset/$meth/${dims}-log-${x}.pickle ]; then
        qsub -o $logfile -j y -N $dataset-$meth-$dims-log-$flag run.sh --dataset $dataset --dims $dims --njobs 12 --method $meth $log
    fi
done
done
done
done
