#!/usr/bin/Rscript
library(ggplot2)
# This script is used to generate a plot of Dimensions Vs Score for the
# provided results csv 

# Call this script from the base directory -- Rscript scripts/plot_internal_results.R

results_csv = 'results/csvs/internal_stats_new2.csv'
plots_dir = 'results/plots/internal_metrics'

data <- read.table(results,sep=',',header=TRUE)
metrics <- c("variance.ratio.criterion","davies.bouldin",
             "dunn.index","silhouette.score")

for( ds in unique(data$dataset)){
    for( metric in metrics){
#        for( l in c(0,1) ){
        set_data <- subset(data,(dataset==ds)  &
                           (dimensions < 10000) & (dimensions >= 10)) 
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
        ggsave(paste(plots_dir,metric,paste(ds,'pdf',sep='.'),sep='/'),device='pdf')
#        }
    }
}
