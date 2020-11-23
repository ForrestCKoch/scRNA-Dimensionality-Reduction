x <- read.csv('data/results/optimal_dbscan_trials/optimal_dbscan_trials_summarized_seuclidean_vrc_ari.csv')
cat('#########################################\n')
cat('Testing tabula vs non-tabula\n')
cat('#########################################\n')
cat('\n')
x$istabula<-grepl('Tabula',x$dataset)
tab <- subset(x,istabula==T)
notab <- subset(x,istabula==F)
for(i in c(3:35)){
    w <- wilcox.test(tab[,i],notab[,i])
    cat(paste0(names(tab)[i],',',w$p.value,'\n'))
}
# kpca.sig, lle, vasc had p < 0.05
cat('#########################################\n\n')

gjs <- read.csv('tmp/datasets_used_GJS.csv')
cat('#########################################\n')
cat('Testing reads vs umis\n')
cat('#########################################\n')
cat('\n')
y <- merge(x,gjs,by='dataset')
reads <- subset(y,read.type=='Reads')
umis <- subset(y,read.type=='UMIs')
for(i in c(3:35)){
    w <- wilcox.test(reads[,i],umis[,i])
    cat(paste0(names(reads)[i],',',w$p.value,'\n'))
}
# kpca.sig, lle, vasc had p < 0.05
cat('#########################################\n\n')
