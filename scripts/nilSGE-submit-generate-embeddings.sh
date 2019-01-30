#dataset=zhengmix4eq
#for dataset in koh kumar simk4easy simk4hard simk8hard zhengmix8eq zhengmix4eq; do
for dataset in simk4hard; do
for dims in 5 10 25 50 100 250 500 1000 2500 5000 10000 15000; do
for meth in umap pca isomap lle spectral mds fa fica; do 
for log in ' '; do
    if [ "$log"==' ' ]; then
        flag='true'
    else
        flag='false'
    fi

    logfile="logs/$dataset/${meth}_log-${flag}_dims-${dims}.log"
    qsub -o $logfile -j y -N $dataset-$meth-$dims-log-$flag run.sh --dataset $dataset --dims $dims --njobs 12 --method $meth $log
done
done
done
done
