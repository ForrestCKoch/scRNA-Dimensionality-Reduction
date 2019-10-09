#!/bin/bash
###############################################################################
# run_all.sh
#
# Intended as a demo/to aid in reproducing results.
# This script should be called from the top-level directory.
###############################################################################

# Download each of the RDS datasets
bash scripts/download_sce_datasets.sh

# Convert datasets to csv * pickle formats
bash convert_datasets.sh


