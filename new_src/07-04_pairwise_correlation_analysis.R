library(tidyr)
library(synchrony)

x.tall <- read.csv('data/results/pw_correlations/best_ivm_combined_pw_cor.csv') 

x.ss <- subset(x.tall,opt.type=='ss_euc')
x.dbs <- subset(x.tall,opt.type=='dbs')
x.vrc <- subset(x.tall,opt.type=='vrc')


x.ss.wide <- as.matrix(pivot_wider(x.ss,id_cols=dataset,names_from=method,values_from=r.euc)[,-c(1)])
x.dbs.wide <- as.matrix(pivot_wider(x.dbs,id_cols=dataset,names_from=method,values_from=r.euc)[,-c(1)])
x.vrc.wide <- as.matrix(pivot_wider(x.vrc,id_cols=dataset,names_from=method,values_from=r.euc)[,-c(1)])

x.ss.mean <- apply(x.ss.wide,2,mean,na.rm=T)
x.dbs.mean <- apply(x.dbs.wide,2,mean,na.rm=T)
x.vrc.mean <- apply(x.vrc.wide,2,mean,na.rm=T)

opt_mean <- rbind(rbind(x.ss.mean,x.dbs.mean),x.vrc.mean)
# Get ranks by opt method...
34-apply(opt_mean,1,rank)
