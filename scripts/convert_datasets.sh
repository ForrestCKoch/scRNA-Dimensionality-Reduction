#!/bin/bash
###############################################################################
# convert_datasets.sh
#
# Call this script from the top-level directory to convert each of the SCE rds
# files to *.csv.gz and pickled pandas format.
###############################################################################

# We should probably use a more precise method of checking whether a dataset has been processed

echo "Converting to csvs ..."
mkdir -p data/datasets/csvs/
for sce in $(ls data/datasets/rds|cut -d'.' -f1); do
    if [ ! "$(ls data/datasets/csvs|grep $sce)" ]; then
        echo $sce ...
        Rscript scripts/convert_sce_to_csv.R $sce
    fi
done

echo "Converting to pickled pandas ..."
mkdir -p data/datasets/pddf/
for sce in $(ls data/datasets/csvs|cut -d'.' -f1); do
    if [ ! "$(ls data/datasets/pddf|grep ^${sce}.pkl)" ]; then
        echo $sce ...
        python3 scripts/convert_csv_to_pd.py $sce
    fi
done
