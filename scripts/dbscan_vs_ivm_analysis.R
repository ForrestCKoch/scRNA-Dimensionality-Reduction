library(reshape)
library(synchrony)
library(tidyr)

dinfo <- read.csv('writeup/spreadsheets/datasets_used.csv')
options(width=140)
options(digits=3)

x <- subset(read.csv('data/results/optimal_dbscan_trials/optimal_dbscan_trials_summarized_seuclidean_ari.csv'),X=='vrc')
x <- subset(x,select=-c(kpca.sig))
x[is.na(x)]<-0
med.rank <- 34-rank(apply(x[,3:34],2,median))
med.rank <- med.rank[order(names(med.rank))]
mean.rank <- 34-rank(apply(x[,3:34],2,mean))
mean.rank <- mean.rank[order(names(mean.rank))]
rank.rank <- 34-rank(rowSums((apply(x[,3:34],1,rank))))
rank.rank <- rank.rank[order(names(rank.rank))]

y <- read.csv('data/results/optimal_dbscan_trials/optimal_dbscan_trials_seuclidean.csv')
y[is.na(y)]<-0
x2 <- data.frame(pivot_wider(subset(y,loss_criteria=='vrc'),id_cols=c('dataset'),names_from=c('method'),values_from=c('ari')))
x2 <- subset(x2,select=-c(kpca.sig))
x2[is.na(x2)]<-0
med.rank2 <- 34-rank(apply(x2[,2:33],2,median))
med.rank2 <- med.rank2[order(names(med.rank2))]
mean.rank2 <- 34-rank(apply(x2[,2:33],2,mean))
mean.rank2 <- mean.rank2[order(names(mean.rank2))]
rank.rank2 <- 34-rank(rowSums((apply(x2[,2:33],1,rank))))
rank.rank2 <- rank.rank2[order(names(rank.rank2))]

#z <- subset(read.csv('data/results/internal_validation_measures/internal_measures_optimal.csv'),method=='ss_seu')
z <- subset(read.csv('data/results/internal_validation_measures/internal_measures_optimal.csv'),method=='vrc')
z[is.na(z)] <- 0
z <- subset(z,select=-c(psmf))
med.rank3 <- 34-rank(apply(z[,3:34],2,median))
med.rank3 <- med.rank3[order(names(med.rank3))]
mean.rank3 <- 34-rank(apply(z[,3:34],2,mean))
mean.rank3 <- mean.rank3[order(names(mean.rank3))]
rank.rank3 <- 34-rank(rowSums((apply(z[,3:34],1,rank))))
rank.rank3 <- rank.rank3[order(names(rank.rank3))]

#print(cor(med.rank2,med.rank3,method='spearman'))
#print(cor(mean.rank2,mean.rank3,method='spearman'))
#print(cor(rank.rank2,med.rank3,method='spearman'))

k <- subset(read.csv('data/results/optimal_kmeans_trials_summarized_ari.csv'),X=='vrc')
k[is.na(k)] <- 0

# Final solution to go with ...
ivm.med.rank <- apply(apply(z[,3:34],1,rank),1,median)
ivm.med.rank<-ivm.med.rank[order(names(ivm.med.rank))]
dbs.med.rank <- apply(apply(x2[,2:33],1,rank),1,median)
dbs.med.rank<-dbs.med.rank[order(names(dbs.med.rank))]
kmean.med.rank <- apply(apply(k[,3:34],1,rank),1,median)
kmean.med.rank<-kmean.med.rank[order(names(kmean.med.rank))]
print(cor.test(ivm.med.rank,dbs.med.rank,method='spearman'))
print(cor.test(ivm.med.rank,dbs.med.rank))
print(cor.test(ivm.med.rank,kmean.med.rank,method='spearman'))
print(cor.test(ivm.med.rank,kmean.med.rank))
print(cor.test(kmean.med.rank,dbs.med.rank,method='spearman'))
print(cor.test(kmean.med.rank,dbs.med.rank))

# excluding 'bd', 'icm', 'vpac' ...
a1 <- ivm.med.rank[!names(ivm.med.rank)%in%c('bd','icm','vpac')]
a2 <- dbs.med.rank[!names(ivm.med.rank)%in%c('bd','icm','vpac')]
a3 <- kmean.med.rank[!names(ivm.med.rank)%in%c('bd','icm','vpac')]

print(cor.test(a1,a2,method='spearman'))
print(cor.test(a1,a2))
print(cor.test(a1,a3,method='spearman'))
print(cor.test(a1,a3))
print(cor.test(a3,a2,method='spearman'))
print(cor.test(a3,a2))

y2 <- read.csv('data/results/optimal_dbscan_trials_seuclidean_tmp.csv')
y2[is.na(y2)]<-0
x3 <- data.frame(pivot_wider(subset(y2,loss_criteria=='vrc'),id_cols=c('dataset'),names_from=c('method'),values_from=c('ari')))
x3 <- subset(x3,select=-c(kpca.sig,psmf,tga))
x3[is.na(x3)]<-0
dbs2.med.rank <- apply(apply(x3[,2:33],1,rank),1,median)
dbs2.med.rank<-dbs2.med.rank[order(names(dbs2.med.rank))]

pdf('writeup/plots/dbscan_vs_ivm/dbscan_vs_ivm_ranks.pdf')
plot(dbs.med.rank,ivm.med.rank,cex=0.01)
abline(0,1,lty=2)
text(dbs.med.rank,ivm.med.rank,names(dbs.med.rank),cex=0.5)
dev.off()
pdf('writeup/plots/dbscan_vs_ivm/kmeans_vs_ivm_ranks.pdf')
plot(kmean.med.rank,ivm.med.rank,cex=0.01)
abline(0,1,lty=2)
#text(kmean.med.rank+2*(runif(32)-0.5),ivm.med.rank+2*(runif(32)-0.5),names(dbs.med.rank),cex=0.5)
text(kmean.med.rank,ivm.med.rank,names(dbs.med.rank),cex=0.5)
dev.off()
pdf('writeup/plots/dbscan_vs_ivm/dbscan_vs_kmeans_ranks.pdf')
plot(dbs.med.rank,kmean.med.rank,cex=0.01)
abline(0,1,lty=2)
text(dbs.med.rank,kmean.med.rank,names(dbs.med.rank),cex=0.5)
dev.off()
