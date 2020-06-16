library('synchrony')
library('reshape')
x <- read.csv('data/results/internal_validation_measures/internal_measures_standardized.csv')
measures <- unique(x$measure)

cat('\n')
cat('##########################################\n')
cat('Concordance between IVM:\n')
cat('##########################################\n')
# Get the average by column
X <- colMeans(subset(x,measure=='ss_euc')[,-c(1,2)],na.rm=T)
#for(i in measures[-c(1)]){
for(i in c('vrc','dbs')){
    X<-rbind(X,colMeans(subset(x,measure==i)[,-c(1,2)],na.rm=T))
}
# to regenerate data/results/internal_measures_standardized_grouped_means.csv
# uncomment the following lines
# and calculate the total mean for the last column
#y<-data.frame(X)
#y$measure<-measure
#write.csv(y,'data/results/internal_measures_standardized_grouped_means.csv')

# Measure aggrement of different IVMs
kw<-kendall.w(t(X),nrands=1000,quiet=T)
print(kw)
cat('\n')
cat('\n')

cat('##########################################\n')
cat('Concordance between metrics for silhouette score:\n')
cat('##########################################\n')
# Get the average by column
X <- colMeans(subset(x,measure=='ss_cor')[,-c(1,2)],na.rm=T)
for(i in c('ss_cos','ss_euc','ss_seu','vrc')){
    X<-rbind(X,colMeans(subset(x,measure==i)[,-c(1,2)],na.rm=T))
}
# to regenerate data/results/internal_measures_standardized_grouped_means.csv
# uncomment the following lines
# and calculate the total mean for the last column
#y<-data.frame(X)
#y$measure<-measure
#write.csv(y,'data/results/internal_measures_standardized_grouped_means.csv')

# Measure aggrement of different IVMs
kw<-kendall.w(t(X),nrands=1000,quiet=T)
print(kw)
cat('\n')
cat('\n')

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

# My results were:
# Kendall's W p-value (one-tailed test [greater]): 0.000999> kendall.w(t(X),nrands=1000000)
#  |======================================================================| 100%
# Kendall's W (uncorrected for ties): 0.8708
# Kendall's W (corrected for ties): 0.8708
# Spearman's ranked correlation: 0.845

# To conduct a pairwise t test ...
# Note that an assumption of independence is being broken here
# may be worth considering validity ...
pwt<-pairwise.t.test(as.vector(X),rep(measures,ea=6))
#write.csv('data/results/ivm_pairwisetest.csv')
