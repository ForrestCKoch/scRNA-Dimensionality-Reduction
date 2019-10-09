#!/usr/bin/Rscript
library(ggplot2)
# This script is used to generate a plot of Dimensions Vs Score for the
# provided results csv 

data <- read.table('results/csvs/internal_metrics_reduced.csv',sep=',',header=TRUE)
#data <- read.table('results/csvs/baron_rare.txt',sep=',',header=TRUE)
#metrics <- c("variance.ratio.criterion","davies.bouldin",
#             "dunn.index","silhouette.score")
metrics <- c("silhouette.score")

for( ds in unique(data$dataset)){
    for( metric in metrics){
#        for( l in c(0,1) ){
        set_data <- subset(data,(dataset==ds)  &
                           (dimensions < 120) & (dimensions >= 2)) 
        hbar <- subset(data,(dataset==ds) & (method=="full"))[metric]
        if(metric == "silhouette.score" | 
           metric == "dunn.index"){
            ggplot(data=set_data,aes(x=dimensions,y=get(metric),
               group=method,color=factor(method))) +
                scale_fill_brewer(palette="Set3") +
               geom_smooth(se=FALSE)+scale_x_log10()+
               geom_hline(yintercept=hbar[1,])+
               ggtitle(paste(ds,'dimensions vs', metric)) +
               ylab(metric) + theme(plot.title = element_text(hjust = 0.5)) + 
               theme(legend.title = element_blank())
        }else{
            ggplot(data=set_data,aes(x=dimensions,y=get(metric),
               group=method,color=factor(method))) +
               geom_smooth(se=FALSE)+scale_x_log10()+
               scale_y_log10()+
               geom_hline(yintercept=hbar[1,])+
               ggtitle(paste(ds,'dimensions vs', metric)) +
               ylab(metric) + theme(plot.title = element_text(hjust = 0.5)) +
               theme(legend.title = element_blank()) +
                scale_fill_brewer(palette="Set2")
        }
        ggsave(paste('results/plots/internal_metrics',metric,paste(ds,'png',sep='-rare.'),sep='/'),device='png')
#        }
    }
}
