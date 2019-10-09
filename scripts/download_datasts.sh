#!/bin/bash
###############################################################################
# download_datasets.sh
# Use this script to download the RDS datasets for benchmarking
###############################################################################

# Keep track of our working directory
workdir=$(pwd)
rds_folder=$workdir/data/datasets/rds
mkdir -p $rds_folder
mkdir -p $workdir/logs/download_datasets

# Use a temporary directory to initially create our datasets
tmpdir=$(mktemp -d) || { echo "Failed to create temp file"; exit 1; }

cd $tmpdir
git clone https://github.com/ForrestCKoch/scRNA.seq.datasets.git
cd scRNA.seq.datasets
mkdir downloads
cd downloads

for dataset in $(ls $tmpdir/scRNA.seq.datasets/R|cut -d'.' -f1); do
    echo "$dataset ..."
    logfile=$workdir/logs/download_datasets/${dataset}.log
    bash ../bash/${dataset}.sh >> $logfile 2>&1
    Rscript ../R/${dataset}.R >> $logfile 2>&1
    mv *.rds $rds_folder/

    # Cycle through and delete each file/folder but don't delete `downloads`
    # Probably inefficient but whatever ...
    for f in $(ls $tmpdir/scRNA.seq.datasets/downloads/); do
        if [ -d $f ]; then
            rm -r $f
        else
            rm $f
        fi
    done
    
done

cd $workdir

rm -rf $tmpdir

