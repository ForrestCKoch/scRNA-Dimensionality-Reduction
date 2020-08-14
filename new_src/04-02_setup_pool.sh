#!/bin/sh

for metric in seuclidean correlation cosine; do

    mkdir -p data/${metric}-spool/
    cluster-pool.sh -i -w data/${metric}-spool
    #find data/smallq -type f | xargs -n 1 -I{} cluster-pool.sh -w data/spool -a "bash scripts/run_trial.sh {}" $(echo {}|sed 's/\//-/g')

    for line in $(find data/queues -type f|grep "/${metric}/"); do
        cluster-pool.sh -w data/${metric}-spool -a "bash scripts/run_trial.sh $line" $(echo $line| sed 's/\//-/g')
    done
done

