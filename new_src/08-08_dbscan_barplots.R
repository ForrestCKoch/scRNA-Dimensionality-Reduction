library(ggplot2)

dinfo <- read.csv('writeup/spreadsheets/datasets_used.csv')
for( metric in c('correlation','cosine','euclidean','seuclidean')){
    x <- read.csv(paste0('data/results/optimal_dbscan_trials/optimal_dbscan_trials_summarized_',metric,'_ari.csv'))
    y <- merge(x,dinfo,by='dataset')
    for(measure in c('vrc')){
        for(var in c('n_classes','n_samples','min_class_perc','max_class_perc','protocol')){
            z <- subset(y,X==measure)
            p <- ggplot(data.frame(y=as.vector(apply(z[,c(3:35)],2,cor,y=z[var],use='complete.obs',method='spearman')),x=names(z)[c(3:35)]),aes(x=reorder(x,-y),y=y))+geom_bar(stat='identity')
            ggsave(paste0('writeup/plots/dbscan_barplot_',metric,'_',measure,'_',var,'.pdf'),p,width=14)
        }
    }
}
