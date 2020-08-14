library(reshape)
library(synchrony)

dinfo <- read.csv('writeup/spreadsheets/datasets_used.csv')
options(width=140)
options(digits=3)

for(metric in c('euclidean','seuclidean','cosine','correlation')){
    x <- read.csv(paste0('data/results/optimal_dbscan_trials/optimal_dbscan_trials_summarized_',metric,'_ari.csv'))
    for(measure in c('vrc','ss','dbs')){
    #for(measure in c('ss')){
        y <- subset(x,X==measure) # extract single measure only
        z <- y[apply(y[,-c(1,2)],1,max,na.rm=T)>0.5,] # exclude datasets with very poor performance
        v <- merge(z,dinfo,by='dataset')
        #print(dim(z))
        #X.prot <- sapply(names(v)[3:35],function(i){aggregate(v[,i],list(v$protocol),mean,na.rm=T)$x})
        #print(34-rank(colMeans(v[,3:35],na.rm=T)))
        #rks <- rowMeans(34-apply(v[,3:35],1,rank,na.last=F),na.rm=T)
        a<-v[,3:35]
        a[is.na(a)] = 0
        rnks <- 34-rank(colMeans(a))
        print(paste(metric,measure,paste(dim(a),collapse=',')))
        #print(rnks)
        print(colMeans(a)[order(colMeans(a),decreasing=T)])
        #print(paste(metric,measure))
        #print(rank(rks))

        #max.names <- names(v)[which.max(cm)]
        #print(paste(max.names,max(cm)))
        #print(paste(metric,measure,max.names))
    }
}

x <- read.csv(paste0('data/results/optimal_dbscan_trials/optimal_dbscan_trials_summarized_overall_ari.csv'))
for(measure in c('vrc','ss','dbs')){
    y <- subset(x,criterion==measure) # extract single measure only
    z <- y[apply(y[,-c(1,2)],1,max,na.rm=T)>0.5,] # exclude datasets with very poor performance
    v <- merge(z,dinfo,by='dataset')
    #print(dim(z))
    #X.prot <- sapply(names(v)[3:35],function(i){aggregate(v[,i],list(v$protocol),mean,na.rm=T)$x})
    #print(paste(metric,measure))
    #print(34-rank(colMeans(v[,3:35],na.rm=T)))
    #print(colMeans(v[,3:35],na.rm=T))
    #rks <- rowMeans(34-apply(v[,3:35],1,rank,na.last=F),na.rm=T)
    #print(paste(metric,measure))
    #print(rank(rks))

    #max.names <- names(v)[which.max(cm)]
    #print(paste(max.names,max(cm)))
    #print(paste(metric,measure,max.names))
}
