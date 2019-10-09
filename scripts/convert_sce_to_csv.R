#!/usr/bin/env Rscript
###############################################################################
# convert_sce_to_csv.R
#
# Used by convert_datasets.sh to convert an RDS file to a CSV.
# This script hould be called from the top-level directory and passed one
# argument specifying the head of the RDS file to be loaded.
#
# It will output two csvs, (normed) counts + logged counts
###############################################################################
suppressMessages(library(SingleCellExperiment))
suppressMessages(library(scater))

args = commandArgs(trailingOnly=TRUE)

if(length(args) != 1){
    stop('Specify a single file to be loaded')
}

rds_file <- paste(args[1],'rds',sep='.')
rds_fold <- 'data/datasets/rds'

if(! rds_file %in% list.files(rds_fold)){
    stop(paste('Couldn\'t find:',paste(rds_fold,rds_file,sep='/')))
}

sce <- readRDS(paste(rds_fold,rds_file,sep='/'))

# check to make sure cell_type1 exists
if(! 'cell_type1' %in% names(colData(sce))){
    stop('No cell_type1 ...')
}else{
    colnames(sce) <- colData(sce)$cell_type1
}

# check if we are using counts or normcounts
if( 'counts' %in% names(assays(sce))){
    # Use CPM & counts
    cpm <- calculateCPM(sce)
    log_counts <- log1p(cpm)

    gz <- gzfile(paste('data/datasets/csvs/','counts_',args[1],'.csv.gz',sep=''))
    write.csv(t(as.matrix(cpm)),gz)
    gz <- gzfile(paste('data/datasets/csvs/','logcounts_',args[1],'.csv.gz',sep=''))
    write.csv(t(as.matrix(log_counts)),gz)

}else if ('normcounts' %in% names(assays(sce))){
    norm_counts <- normcounts(sce)
    log_counts <- log1p(norm_counts)

    gz <- gzfile(paste('data/datasets/csvs/','normcounts_',args[1],'.csv.gz',sep=''))
    write.csv(t(as.matrix(cpm)),gz)
    gz <- gzfile(paste('data/datasets/csvs/','lognormcounts_',args[1],'.csv.gz',sep=''))
    write.csv(t(as.matrix(log_counts)),gz)

}else{
    stop(paste('Unknown assay types:',names(asssays(sce))))
}
