library(ggplot2)
library(reshape)

data <- read.csv('data/results/pw_correlations/pw_correlations_by_best_ivm.csv')

p <- ggplot(data,aes(reorder(method,ss_euc,FUN=median,na.rm=T),ss_euc)) + geom_boxplot(outlier.shape=19) + theme(axis.text.x = element_text(angle = 90)) + xlab('Dimensionality Reduction Method') + ylab('Pairwise Distance Correlation') + ggtitle("'Best' embedding chosen by Silhouette Score") + coord_polar()

ggsave('writeup/plots/pw_correlations/pw_correlations_boxplot_ss-euc_polar.pdf',p)

p <- ggplot(data,aes(reorder(method,dbs,FUN=median,na.rm=T),dbs)) + geom_boxplot(outlier.shape=19) + theme(axis.text.x = element_text(angle = 90))+ ylab('Pairwise Distance Correlation') + ggtitle("'Best' embedding chosen by Davies Bouldin Score") + xlab('Dimensionality Reduction Method') + coord_polar()

ggsave('writeup/plots/pw_correlations/pw_correlations_boxplot_dbs_polar.pdf',p)

p <- ggplot(data,aes(reorder(method,vrc,FUN=median,na.rm=T),vrc)) + geom_boxplot(outlier.shape=19) + theme(axis.text.x = element_text(angle = 90))+ ylab('Pairwise Distance Correlation') + ggtitle("'Best' embedding chosen by Variance Ratio Criterion") + xlab('Dimensionality Reduction Method') + coord_polar()

ggsave('writeup/plots/pw_correlations/pw_correlations_boxplot_vrc_polar.pdf',p)

data2 <- melt(subset(data,select=-c(X)))
data2 <- subset(data2,variable!='ss_seu')
data2 <- subset(data2,variable!='ss_cos')
p <- ggplot(data2, aes(reorder(method,value,FUN=median,na.rm=T),value,fill=variable))+geom_boxplot()+ylab('Pairwise Distance Correlation') + ggtitle("") + xlab('Dimensionality Reduction Method') + theme(axis.text.x = element_text(angle = 90))

ggsave('writeup/plots/pw_correlations/pw_correlations_all_boxplot.pdf',width=16,height=9)
