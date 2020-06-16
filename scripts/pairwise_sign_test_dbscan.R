x<-read.csv('writeup/spreadsheets/dbscan_metric_averages.csv')
cat(paste(x[,1],x[,2],sep='.',collapse=','))
cat('\n')
y<-t(x[,3:35])
for(i in c(1:11)){
    cat(paste(x[,1],x[,2],sep='.')[i])
    cat(',')
    for(j in c(1:i)){
            cat('NA,')
    }
    for(j in c((i+1):12)){
        gt <- sum(y[,i]>y[,j])
        if(gt > 16){
            cat(pbinom(gt,33,0.5,lower.tail=FALSE))
        }else{
            cat(pbinom(gt,33,0.5,lower.tail=TRUE))
        }
        cat(',')
    }
    cat('\n')
}

