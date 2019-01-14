#!/bin/sh

# This script should be called from the root/head directory
# of the project.  It will download the necessary datasets
# and set up the necessary file structure

mkdir -p data/datasets
mkdir -p data/models
mkdir -p data/plots
mkdir -p data/embeddings

wget "ftp://ftp.ncbi.nlm.nih.gov/geo/series/GSE93nnn/GSE93421/suppl/GSE93421_brain_aggregate_matrix.hdf5" -P "data/datasets/"
Rscript scripts/get_datasets.R

