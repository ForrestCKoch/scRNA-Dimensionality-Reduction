full.dat <- read.csv('data/results/pw_correlations/best_ivm_combined_pw_cor.csv')

cor.types <- c('r.euc','r.seu','r.cos','r.cor')
for(m in unique(x$opt.type)){
    ivm.dat <- subset(full.dat,opt.type==m)

    # creates a matrix of correlations with cor.types as columns and
    # methods as rows
    ivm.cor  <- t(do.call(rbind,
        lapply(cor.types,
            function(Y) do.call(rbind,
                list(by(ivm.dat,ivm.dat$method, 
                    function(X) cor(X[,Y],X$opt.value,
                        method='spearman',use='complete.obs')
                    ))
            )
        )
    ))

    colnames(ivm.cor) <- cor.types
    write.csv(ivm.cor,paste0('data/results/pw_correlations/ivm_correlations_',m,'.csv'))

    # same as above, but pvalues from cor.test ...
    ivm.pv  <- t(do.call(rbind,
        lapply(cor.types,
            function(Y) do.call(rbind,
                list(by(ivm.dat,ivm.dat$method, 
                    function(X) cor.test(X[,Y],X$opt.value,
                        method='spearman',use='complete.obs')$p.value
                    ))
            )
        )
    ))

    colnames(ivm.pv) <- cor.types

    write.csv(ivm.pv,paste0('data/results/pw_correlations/ivm_correlations_',m,'_pvalues.csv'))
}
