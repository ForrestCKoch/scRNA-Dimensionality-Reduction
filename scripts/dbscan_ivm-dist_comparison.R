cor <- read.csv('data/results/optimal_dbscan_trials/optimal_dbscan_trials_summarized_correlation_ari.csv')
cos <- read.csv('data/results/optimal_dbscan_trials/optimal_dbscan_trials_summarized_cosine_ari.csv')
euc <- read.csv('data/results/optimal_dbscan_trials/optimal_dbscan_trials_summarized_euclidean_ari.csv')
seu <- read.csv('data/results/optimal_dbscan_trials/optimal_dbscan_trials_summarized_seuclidean_ari.csv')

cor.dbs <- subset(cor,X=='dbs')
cor.vrc <- subset(cor,X=='vrc')
cor.ss <- subset(cor,X=='ss')

cos.dbs <- subset(cos,X=='dbs')
cos.vrc <- subset(cos,X=='vrc')
cos.ss <- subset(cos,X=='ss')

euc.dbs <- subset(euc,X=='dbs')
euc.vrc <- subset(euc,X=='vrc')
euc.ss <- subset(euc,X=='ss')

seu.dbs <- subset(seu,X=='dbs')
seu.vrc <- subset(seu,X=='vrc')
seu.ss <- subset(seu,X=='ss')

# Organize methods by their max ...
# print(pbinom(sum(seu.vrc$ivis>euc.vrc$ivis),55,0.5))

#cor.dbs.best <- c('bd','fa','fica','grp','ipca','isomap','kpca.cos','kpca.pol','kpca.sig','nmf2','nsnmf','pca','pmf','snmf','spca','spectral','srp','vasc','zifa')
#cos.dbs.best <- c('icm','lle','nmf','spca.batch','vpac')
#euc.dbs.best <- c('lda')

#cor.vrc.best <- c('kpca.rbf')
#euc.vrc.best <- c('phate')
#seu.vrc.best <- c('ivis','lsnmf','mctsne','tsvd','umap')


euc.vrc.best <- c('fa','fica','nmf','nmf2','nsnmf','phate','vpac')
seu.vrc.best <- c('ipca','ivis','kpca.pol','lda','lsnmf','mctsne','pca','snmf','spca','spac-batch','tsvd','umap','vasc','zifa')
cos.vrc.best <- c('bd','grp','isomap','kpca.cos','kpca.rbf','srp')
cor.vrc.best <- c('icm','lle')
cos.ss.best <- c('kpca.sig','pmf','spectral')

print('###################################')
print('VRC - EUC')
print('###################################')
for(drm in euc.vrc.best){
    comp <- euc.vrc[drm]<=seu.vrc[drm]
    comp.tot <- length(comp) - sum(is.na(comp))
    comp.lt <- sum(comp,na.rm=T)
    comp.pval <- pbinom(comp.lt,comp.tot,0.5)

    print(paste(drm,': ',comp.lt,' has p.val ',comp.pval,sep=''))
    print(wilcox.test(euc.vrc[,drm],seu.vrc[,drm],paired=T)$p.value)
}

print('###################################')
print('VRC - COS')
print('###################################')
for(drm in cos.vrc.best){
    comp <- cos.vrc[drm]<=seu.vrc[drm]
    comp.tot <- length(comp) - sum(is.na(comp))
    comp.lt <- sum(comp,na.rm=T)
    comp.pval <- pbinom(comp.lt,comp.tot,0.5)

    print(paste(drm,': ',comp.lt,' has p.val ',comp.pval,sep=''))
    print(wilcox.test(cos.vrc[,drm],seu.vrc[,drm],paired=T)$p.value)
}

print('###################################')
print('VRC - COR')
print('###################################')
for(drm in cor.vrc.best){
    comp <- cor.vrc[drm]<=seu.vrc[drm]
    comp.tot <- length(comp) - sum(is.na(comp))
    comp.lt <- sum(comp,na.rm=T)
    comp.pval <- pbinom(comp.lt,comp.tot,0.5)

    print(paste(drm,': ',comp.lt,' has p.val ',comp.pval,sep=''))
    print(wilcox.test(cor.vrc[,drm],seu.vrc[,drm],paired=T)$p.value)
}

print('###################################')
print('SS - COS')
print('###################################')
for(drm in cos.ss.best){
    comp <- cos.ss[drm]<=seu.vrc[drm]
    comp.tot <- length(comp) - sum(is.na(comp))
    comp.lt <- sum(comp,na.rm=T)
    comp.pval <- pbinom(comp.lt,comp.tot,0.5)

    print(paste(drm,': ',comp.lt,' has p.val ',comp.pval,sep=''))
    print(wilcox.test(cos.ss[,drm],seu.vrc[,drm],paired=T)$p.value)
}
