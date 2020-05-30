x <- read.csv('data/results/internal_validation_measures/internal_measures_standardized.csv')

n.datasets <- length(unique(x$dataset))
options(digits=3)


cat('measure,')
cat(paste(names(x)[3:35],collapse=','))
cat('\n')
for(m in unique(x$measure)){
    y <- subset(x,measure==m)
    cat(m)
    cat(',')
    #cat(paste(rank(33-rowSums(apply(y[,3:35],1,rank,na.last=T))/n.datasets),collapse=','))
    cat(paste(round(33-rowSums(apply(y[,3:35],1,rank,na.last=T))/n.datasets,digits=1),collapse=','))
    cat('\n')
}
cat('overall,')
#cat(paste(rank(33-rowSums(apply(x[,3:35],1,rank,na.last=T))/n.datasets),collapse=','))
cat(paste(round(33-rowSums(apply(x[,3:35],1,rank,na.last=T))/(n.datasets*6),digits=1),collapse=','))
cat('\n')
