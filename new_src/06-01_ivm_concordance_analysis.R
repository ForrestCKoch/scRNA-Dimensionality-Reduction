# Statistical Tests of Concordance:
#   1. Test concordance between IVMs regarding ranking of methods
#   2. Test concordance between distance metrics (via silhouette score) regarding rankings of methods.
#   3. Calculate the concordance between datasets regarding rankings of methods for each IVM.
library('synchrony')
library('reshape')
x <- read.csv('data/results/internal_validation_measures/internal_measures_standardized.csv')
measures <- unique(x$measure)

#####
# 1.
#####
x[is.na(x)] <- 0
cat('\n')
cat('##########################################\n')
cat('Concordance between IVM:\n')
cat('##########################################\n')
# Get the average by column
X <- apply(apply(subset(x,measure=='ss_euc')[,-c(1,2)],1,rank,na.last=F),1,median,na.rm=T)
print(X)
#for(i in measures[-c(1)]){
for(i in c('vrc','dbs')){
    X<-rbind(X,apply(apply(subset(x,measure==i)[,-c(1,2)],1,rank,na.last=F),1,median,na.rm=T))
}
print(X)

# Measure aggrement of different IVMs
kw<-kendall.w(t(X),nrands=1000,quiet=T)
print(kw)
cat('\n')
cat('\n')

#####
# 2.
#####
cat('##########################################\n')
cat('Concordance between metrics for silhouette score:\n')
cat('##########################################\n')
# Get the average by column
X <- apply(subset(x,measure=='ss_cor')[,-c(1,2)],2,median,na.rm=T)
for(i in c('ss_cos','ss_euc','ss_seu')){
    X<-rbind(X,apply(subset(x,measure==i)[,-c(1,2)],2,median,na.rm=T))
}

# Measure aggrement of different IVMs
kw<-kendall.w(t(X),nrands=1000,quiet=T)
print(kw)
cat('\n')
cat('\n')

#####
# 3.
#####
cat('##########################################\n')
cat('Concordance between datasets:\n')
cat('##########################################\n')
for(i in measures){
    cat(paste(i,':\n'))
    kw<-kendall.w(t(subset(x,measure==i)),nrands=1000,quiet=T)
    print(kw)
    cat('\n')
    cat('\n')
}
