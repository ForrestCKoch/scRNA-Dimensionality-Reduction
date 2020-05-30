x <- read.csv('data/results/internal_validation_measures/internal_measures_standardized.csv')

n.datasets <- length(unique(x$dataset))
options(digits=3)

methods <- names(x)[3:35]
n.methods <- length(methods)
n.datasets <- length(unique(x$dataset))
#for(m in unique(x$measure)){
for(m in c('vrc')){
    y <- subset(x,measure==m)
    y[is.na(y)] <- 0 # Autofail ... 
    cat('\n######################################\n')
    cat('# ')
    cat(m)
    cat('\n')
    cat('######################################\n\n')
    cat('X,')
    cat(paste(methods,collapse=','))
    cat('\n')
    for(i in c(1:(n.methods-1))){
        method.i <- y[,methods[i]]
        #cat(methods[i])
        for(j in c(1:i)){
            # cat(',NA')
        }
        for(j in c((i+1):n.methods)){
            method.j <- y[,methods[j]] 
            n.gt <- sum(method.i>method.j)
            #cat(',')
            #cat(pbinom(n.gt,n.datasets,0.5,n.gt<n.datasets/2))
            cat(paste(methods[i],methods[j],n.gt,n.datasets,n.gt<n.datasets/2,pbinom(n.gt,n.datasets,0.5,n.gt<n.datasets/2),'\n'))
        }
        cat('\n')
    }
}
