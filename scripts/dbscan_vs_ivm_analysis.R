library(reshape)
library(synchrony)
library(tidyr)

dinfo <- read.csv('writeup/spreadsheets/datasets_used.csv')
options(width=140)
options(digits=3)

x <- subset(read.csv('data/results/optimal_dbscan_trials/optimal_dbscan_trials_summarized_seuclidean_ari.csv'),X=='vrc')
x[is.na(x)]<-0
med.rank <- 34-rank(apply(x[,3:35],2,median))
mean.rank <- 34-rank(apply(x[,3:35],2,mean))
rank.rank <- 34-rank(rowSums((apply(x[,3:35],1,rank))))

y <- read.csv('data/results/optimal_dbscan_trials/optimal_dbscan_trials_seuclidean.csv')
y[is.na(y)]<-0
x2 <- data.frame(pivot_wider(subset(y,loss_criteria=='vrc'),id_cols=c('dataset'),names_from=c('method'),values_from=c('ari')))
x2[is.na(x2)]<-0
med.rank2 <- 34-rank(apply(x2[,2:34],2,median))
mean.rank2 <- 34-rank(apply(x2[,2:34],2,mean))
rank.rank2 <- 34-rank(rowSums((apply(x2[,2:34],1,rank))))

#z <- subset(read.csv('data/results/internal_validation_measures/internal_measures_optimal.csv'),method=='ss_seu')
z <- subset(read.csv('data/results/internal_validation_measures/internal_measures_optimal.csv'),method=='vrc')
z[is.na(z)] <- 0
med.rank3 <- 34-rank(apply(z[,3:35],2,median))
mean.rank3 <- 34-rank(apply(z[,3:35],2,mean))
rank.rank3 <- 34-rank(rowSums((apply(z[,3:35],1,rank))))

print(cor(med.rank2,med.rank3))
print(cor(mean.rank2,mean.rank3))
print(cor(rank.rank2,med.rank3))
