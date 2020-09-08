# Calculate pairwise tests of method performance and output csv of pvalues
library(reshape)

#seu <- read.csv('data/results/optimal_dbscan_trials/optimal_dbscan_trials_summarized_seuclidean_ari.csv')
#seu.vrc <- subset(seu,X=='vrc')
seu.vrc <- read.csv('data/results/optimal_dbscan_trials/optimal_dbscan_trials_summarized_seuclidean_vrc_ari.csv')
seu.vrc[is.na(seu.vrc)] <- 0
# uncomment the following lines to "filter" out poor performing datasets
#good.datsets <- apply(seu.vrc[,3:35],1,max)>0.5
#seu.vrc <- seu.vrc[good.datsets,]

seu.vrc.flat <- melt(seu.vrc) 

method.order <- order(aggregate(seu.vrc.flat$value,by=list(seu.vrc.flat$variable),FUN=median)$x,decreasing=T)
ordered.method.names <- unique(seu.vrc.flat$variable)[method.order]

# Calculate pairwise wilcox results
wilcox.pvalues <- pairwise.wilcox.test(seu.vrc.flat$value,seu.vrc.flat$variable,p.adjust='none',paired=T)$p.value
wilcox.pvalues[is.na(wilcox.pvalues)] <- 0
# Turn into a symmetric matrix
wilcox.pvalues <- cbind(wilcox.pvalues,rep(0,32))
wilcox.pvalues <- rbind(rep(0,33),wilcox.pvalues)
wilcox.pvalues <- wilcox.pvalues + t(wilcox.pvalues)
# Reorder columns/rows & assign names
wilcox.pvalues <- wilcox.pvalues[method.order,method.order]
# Set the diagonal to 1
wilcox.pvalues <- wilcox.pvalues + diag(33)
rownames(wilcox.pvalues) <- ordered.method.names
colnames(wilcox.pvalues) <- ordered.method.names

#print(wilcox.pvalues)
#write.csv(wilcox.pvalues,'writeup/spreadsheets/dbscan_vrc-seu_wilcox-test-by-methods_filtered.csv')
write.csv(wilcox.pvalues,'writeup/spreadsheets/dbscan_vrc-seu_wilcox-test-by-methods.csv')

sign.pvalues <- matrix(0,33,33)
rownames(sign.pvalues) <- ordered.method.names
colnames(sign.pvalues) <- ordered.method.names


n.dats <- dim(seu.vrc)[1]

for(i in c(1:33)){
    for(j in c(1:33)){
        if(i == j){
            sign.pvalues[i,j] = 1
        }else{
            i.name <- as.character(ordered.method.names[i])
            j.name <- as.character(ordered.method.names[j])
            gt <- sum(seu.vrc[,i.name]>seu.vrc[,j.name])
            eq <- sum(seu.vrc[,i.name]==seu.vrc[,j.name])
            sign.pvalues[i.name,j.name]<-pbinom(gt,n.dats+1-eq,0.5,lower.tail=gt<((n.dats+1-eq)/2))
        }
    }
}

#write.csv(sign.pvalues,'writeup/spreadsheets/dbscan_vrc-seu_sign-test-by-methods_filtered.csv')
write.csv(sign.pvalues,'writeup/spreadsheets/dbscan_vrc-seu_sign-test-by-methods.csv')
