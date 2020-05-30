invisible(library(synchrony))
invisible(library(matrixStats))
invisible(library(reshape))
x <- read.csv('data/results/pw_correlations/pw_correlations_by_best_ivm.csv')
mean.cor <- c()
pwt.pv <- c()
for( m in unique(x$method)){
    y <- subset(x,method==m)
    #cat('#####################\n')
    #cat(m,'\n')
    #cat('#####################\n')
    #print(kendall.w(t(y[,4:6])))
    #cat('\n')
    #print(rank(rowMeans(apply(y[,4:6],1,rank))))
    #cat('\n')
    invisible(z <- melt(y[,4:9]))
    pwt <- melt(pairwise.wilcox.test(z$value,z$variable,p.adj='none')$p.value)
    #mean.cor<-rbind(mean.cor,cbind(c(m),t(colMeans(y[,4:6],na.rm=T))))
    mean.cor<-rbind(mean.cor,t(colMeans(y[,4:9],na.rm=T)))
    pwt.pv<-rbind(pwt.pv,cbind(c(m),t(pwt$value)))
    #print(colMeans(y[,4:6],na.rm=T))
    #print(pairwise.wilcox.test(z$value,z$variable,p.adj='fdr'))
    #print(pairwise.t.test(y[,4:6]))
    #print(t.test(y$ss_euc,y$vrc)$p.value)
    #print(t.test(y$ss_euc,y$dbs)$p.value)
    #print(t.test(y$vrc,y$dbs)$p.value)
    #cat('\n')
}
pwt.pv <- cbind(pwt.pv[,1],data.frame(matrix(p.adjust(pwt.pv[,c(2,3,5)],method='BY'),ncol=3)))
#colnames(pwt.pv) <- c('method','vrc.ss','ss.dbs','vrc.dbs')
#colnames(mean.cor)[1] <- 'method'
#mean.cor <- data.frame(mean.cor)
# true for the best correlation
cor.best <- t(apply(mean.cor[,2:7],1,rank)==3)
# Get significant tests
h.sig <- pwt.pv[,2:7] < 0.05

pairwise.wilcox.test(melt(mean.cor)$value,melt(mean.cor)$X2)$p.value < 0.05
# test for differences between mean correlations when using each heuristic I go:
#         dbs ss_cor ss_cos ss_euc ss_seu
# ss_cor FALSE     NA     NA     NA     NA
# ss_cos FALSE  FALSE     NA     NA     NA
# ss_euc FALSE   TRUE   TRUE     NA     NA
# ss_seu  TRUE   TRUE   TRUE   TRUE     NA
# vrc    FALSE   TRUE   TRUE  FALSE   TRUE

kendall.w(mean.cor[,c(1,5,6)])
# test concordance between 'top' heuristics 
