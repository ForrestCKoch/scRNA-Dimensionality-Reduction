#!/usr/bin/Rscript

library(SingleCellExperiment)
library(DuoClustering2018)

if(!file.exists('data/datasets/zhengmix8eq.csv')){
    cat('Generating zhengmix8eq.csv\n')
    zheng8 <- sce_full_Zhengmix8eq()
    df <- data.frame(counts(zheng8))
    names(df) <- paste(names(df),'-',colData(zheng8)$phenoid)
    write.table(df,file='data/datasets/zhengmix8eq.csv',sep=',',row.names=FALSE)
}

if(!file.exists('data/datasets/zhengmix4eq.csv')){
    cat('Generating zhengmix4eq.csv\n')
    zheng4 <- sce_full_Zhengmix4eq()
    df <- data.frame(counts(zheng4))
    names(df) <- paste(names(df),'-',colData(zheng4)$phenoid)
    write.table(df,file='data/datasets/zhengmix4eq.csv',sep=',',row.names=FALSE)
}

if(!file.exists('data/datasets/simk4easy.csv')){
    cat('Generating simk4easy.csv\n')
    simk4easy <- sce_full_SimKumar4easy()
    df <- data.frame(counts(simk4easy))
    names(df)<-paste(simk4easy$Cell,'-',simk4easy$Group)
    write.table(df,file='data/datasets/simk4easy.csv',row.names=FALSE,sep=',')
}

if(!file.exists('data/datasets/simk4hard.csv')){
    cat('Generating simk4hard.csv\n')
    simk4hard <- sce_full_SimKumar4hard()
    df <- data.frame(counts(simk4hard))
    names(df)<-paste(simk4hard$Cell,'-',simk4hard$Group)
    write.table(df,file='data/datasets/simk4hard.csv',row.names=FALSE,sep=',')
}

if(!file.exists('data/datasets/simk8hard.csv')){
    cat('Generating simk8hard.csv\n')
    simk8hard <- sce_full_SimKumar8hard()
    df <- data.frame(counts(simk8hard))
    names(df)<-paste(simk8hard$Cell,'-',simk8hard$Group)
    write.table(df,file='data/datasets/simk8hard.csv',row.names=FALSE,sep=',')
}

if(!file.exists('data/datasets/koh.csv')){
    cat('Generating koh.csv\n')
    koh <- sce_full_Koh()
    df <- data.frame(counts(koh))
    names(df)<-paste(names(df),'-',colData(koh)$phenoid)
    write.table(df,file='data/datasets/koh.csv',row.names=FALSE,sep=',')
}

if(!file.exists('data/datasets/kumar.csv')){
    cat('Generating kumar.csv\n')
    kumar <- sce_full_Kumar()
    df <- data.frame(counts(kumar))
    names(df)<-paste(names(df),'-',colData(kumar)$phenoid)
    write.table(df,file='data/datasets/kumar.csv',row.names=FALSE,sep=',')
}

