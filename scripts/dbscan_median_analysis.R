library(reshape)
library(synchrony)

dinfo <- read.csv('writeup/spreadsheets/datasets_used.csv')
options(width=300)
options(digits=3)
options(scipen=999)

results <- c()
test <- c()
for(metric in c('euclidean','seuclidean','cosine','correlation')){
    x <- read.csv(paste0('data/results/optimal_dbscan_trials/optimal_dbscan_trials_summarized_',metric,'_ari.csv'))
    for(measure in c('vrc','ss','dbs')){
        y <- subset(x,X==measure) # extract single measure only
        v <- merge(y,dinfo,by='dataset')
        #print(dim(z))
        #X.prot <- sapply(names(v)[3:35],function(i){aggregate(v[,i],list(v$protocol),mean,na.rm=T)$x})
        #print(34-rank(colMeans(v[,3:35],na.rm=T)))
        #rks <- rowMeans(34-apply(v[,3:35],1,rank,na.last=F),na.rm=T)
        a<-v[,3:35]
        a[is.na(a)] = 0
        #rnks <- 34-rank(colMeans(a))
        results <- rbind(results,apply(a,2,median))
        test <- rbind(test,c(metric,measure))
    }
}

results <- rbind(results,apply(results,2,max))
results <- results[,order(apply(results,2,max),decreasing=T)]
test <- rbind(test,c('max',''))

print(cbind(test,data.frame(results)))
