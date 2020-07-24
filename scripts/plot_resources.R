library(ggplot2)
x <- read.csv('data/results/resources-new.csv')
y <- read.csv('writeup/spreadsheets/datasets_used.csv')
z.full <- merge(x,y,by='dataset')
z <- z.full[z.full$method %in% c('phate','vasc','fica','zifa','umap','pca','lda','nmf','fa','ivis','vpac'),]
z.all <- z.full[!(z.full$method  %in% c('tga','lfnmf','sepnmf')),]


for(d in unique(z$dimension)){
    sec.plot <- ggplot(subset(z,dimensions==d),aes(x=n_samples,y=seconds,group=method,color=factor(method),))+
        geom_smooth()+scale_y_continuous(trans='log10')+scale_x_continuous(trans='log10')
    ggsave(paste0('writeup/plots/resource_plots/time-against-n_samples-',d,'_dimensions.pdf'),sec.plot)
    mem.plot <- ggplot(subset(z,dimensions==d),aes(x=n_samples,y=memory,group=method,color=factor(method),))+
        geom_smooth()+scale_y_continuous(trans='log10')+scale_x_continuous(trans='log10')
    ggsave(paste0('writeup/plots/resource_plots/memory-against-n_samples-',d,'_dimensions.pdf'),mem.plot)

    sec.plot <- ggplot(subset(z.all,dimensions==d),aes(x=n_samples,y=seconds,group=method,color=factor(method),))+
        geom_smooth()+scale_y_continuous(trans='log10')+scale_x_continuous(trans='log10')
    ggsave(paste0('writeup/plots/resource_plots/all-time-against-n_samples-',d,'_dimensions.pdf'),sec.plot)
    mem.plot <- ggplot(subset(z.all,dimensions==d),aes(x=n_samples,y=memory,group=method,color=factor(method),))+
        geom_smooth()+scale_y_continuous(trans='log10')+scale_x_continuous(trans='log10')
    ggsave(paste0('writeup/plots/resource_plots/all-memory-against-n_samples-',d,'_dimensions.pdf'),mem.plot)
}
