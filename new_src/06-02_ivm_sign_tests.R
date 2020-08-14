x <- read.csv('data/results/internal_validation_measures/internal_measures_standardized.csv')

n.datasets <- length(unique(x$dataset))
options(digits=3)

methods <- names(x)[3:35]
n.methods <- length(methods)
n.datasets <- length(unique(x$dataset))

for(m in unique(x$measure)){
    # setup a fresh  matrix
    sign.test.results <- matrix(0,n.methods,n.methods)
    rownames(sign.test.results) <- methods
    colnames(sign.test.results) <- methods
#for(m in c('vrc')){
    y <- subset(x,measure==m)
    y[is.na(y)] <- 0 # Autofail ... 
    for(i in c(1:n.methods)){
        method.i <- y[,methods[i]]
        for(j in 1:n.methods){
            if(i == j){
                sign.test.results[i,j] <- 1
            }else{
                method.j <- y[,methods[j]] 
                n.gt <- sum(method.i>method.j)
                n.eq <- sum(method.i==method.j)
                sign.test.results[methods[i],methods[j]] <- pbinom(n.gt,n.datasets-n.eq+1,0.5,n.gt<(n.datasets-n.eq+1)/2)
            }
            #cat(',')
            #cat(pbinom(n.gt,n.datasets,0.5,n.gt<n.datasets/2))
            #cat(paste(methods[i],methods[j],n.gt,n.datasets,n.gt<n.datasets/2,pbinom(n.gt,n.datasets,0.5,n.gt<n.datasets/2),'\n'))
        }
        #cat('\n')
    }
    write.csv(sign.test.results,paste0('writeup/spreadsheets/ivm_sign_tests/ivm_sign_test_',sub('_','-',m),'.csv'))
}
