#!/bin/bash
###############################################################################
# download_datasets.sh
# Use this script to download the RDS datasets for benchmarking
###############################################################################

# Keep track of our working directory
workdir=$(pwd)
rds_folder=$workdir/data/datasets/rds
mkdir -p $rds_folder

# Use a temporary directory to initially create our datasets
tmpdir=$(mktemp -d) || { echo "Failed to create temp file"; exit 1; }

cd $tmpdir
git clone https://github.com/ForrestCKoch/scRNA.seq.datasets.git
cd scRNA.seq.datasets/R

for dataset in $(ls |cut -d'.' -f1); do
    bash ../bash/${dataset}.sh
    Rscript ${dataset}.R
    mv *.rds $rds_folder/
done

cd $workdir

rm -rf $tmpdir

