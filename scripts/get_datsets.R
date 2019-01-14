#!/usr/bin/Rscript

library(SingleCellExperiment)
library(DuoClustering2018)

zheng8 <- sce_full_Zhengmix8eq()
write.table(counts(zheng8),file='zhengmix8eq.csv',sep=',',row.names=FALSE)

zheng4 <- sce_full_Zhengmix4eq()
write.table(counts(zheng4),file='zhengmix4eq.csv',sep=',',row.names=FALSE)

simk4easy <- sce_full_SimKumar4easy()
df <- data.frame(counts(simk4easy))
names(df)<-paste(simk4easy$Cell,'-',simk4easy$Group)
write.csv(df,file='simk4easy.csv',row.names=FALSE,sep=',')

simk4hard <- sce_full_SimKumar4hard()
df <- data.frame(counts(simk4hard))
names(df)<-paste(simk4hard$Cell,'-',simk4hard$Group)
write.csv(df,file='simk4hard.csv',row.names=FALSE,sep=',')

simk8hard <- sce_full_SimKumar8hard()
df <- data.frame(counts(simk8easy))
names(df)<-paste(simk8easy$Cell,'-',simk8easy$Group)
write.csv(df,file='simk8easy.csv',row.names=FALSE,sep=',')




