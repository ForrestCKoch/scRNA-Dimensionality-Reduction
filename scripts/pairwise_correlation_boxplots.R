library(ggplot2)

data <- read.csv('data/results/pw_correlations/pw_correlations_by_best_ivm.csv')

p <- ggplot(data,aes(reorder(method,ss_euc,FUN=median,na.rm=T),ss_euc)) + geom_boxplot(outlier.shape=19) + theme(axis.text.x = element_text(angle = 90)) + xlab('Dimensionality Reduction Method') + ylab('Pairwise Distance Correlation') + ggtitle("'Best' embedding chosen by Silhouette Score") + coord_polar()

ggsave('writeup/plots/pw_correlations_boxplot_ss-euc_polar.pdf',p)

p <- ggplot(data,aes(reorder(method,dbs,FUN=median,na.rm=T),dbs)) + geom_boxplot(outlier.shape=19) + theme(axis.text.x = element_text(angle = 90))+ ylab('Pairwise Distance Correlation') + ggtitle("'Best' embedding chosen by Davies Bouldin Score") + xlab('Dimensionality Reduction Method') + coord_polar()

ggsave('writeup/plots/pw_correlations_boxplot_dbs_polar.pdf',p)

p <- ggplot(data,aes(reorder(method,vrc,FUN=median,na.rm=T),vrc)) + geom_boxplot(outlier.shape=19) + theme(axis.text.x = element_text(angle = 90))+ ylab('Pairwise Distance Correlation') + ggtitle("'Best' embedding chosen by Variance Ratio Criterion") + xlab('Dimensionality Reduction Method') + coord_polar()

ggsave('writeup/plots/pw_correlations_boxplot_vrc_polar.pdf',p)
