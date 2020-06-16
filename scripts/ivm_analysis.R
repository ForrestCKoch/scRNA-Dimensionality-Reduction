library('synchrony')
x <- read.csv('data/results/internal_measures_standardized.csv')
measures <- unique(x$measure)
# Get the average by column
X <- colMeans(subset(x,measure==measures[1])[,-c(1,2)],na.rm=T)
for(i in measures[-c(1)]){
    X<-rbind(X,colMeans(subset(x,measure==i)[,-c(1,2)],na.rm=T))
}
# to regenerate data/results/internal_measures_standardized_grouped_means.csv
# uncomment the following lines
# and calculate the total mean for the last column
#y<-data.frame(X)
#y$measure<-measure
#write.csv(y,'data/results/internal_measures_standardized_grouped_means.csv')

# Measure aggrement of different IVMs
kw<-kendall.w(t(X),nrands=10000)
print(kw)

# My results were:
# Kendall's W p-value (one-tailed test [greater]): 0.000999> kendall.w(t(X),nrands=10000)
#  |======================================================================| 100%
# Kendall's W (uncorrected for ties): 0.8708
# Kendall's W (corrected for ties): 0.8708
# Spearman's ranked correlation: 0.845

# To conduct a pairwise t test ...
# Note that an assumption of independence is being broken here
# may be worth considering validity ...
pwt<-pairwise.t.test(as.vector(X),rep(measures,ea=6))
#write.csv('data/results/ivm_pairwisetest.csv')
