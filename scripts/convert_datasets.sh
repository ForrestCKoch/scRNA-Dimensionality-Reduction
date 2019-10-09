#!/bin/bash
###############################################################################
# convert_datasets.sh
#
# Call this script from the top-level directory to convert each of the SCE rds
# files to *.csv.gz and pickled pandas format.
###############################################################################

mkdir -p data/datasets/csvs/
for sce in $(ls data/datasets/rds|cut -d'.' -f1); do
    Rscript scripts/convert_sce_to_csv.R $sce
done
