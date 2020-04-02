library(ggplot2)

data <- read.csv('data/results/pw_correlations/pw_correlations_by_best_ivm.csv')

p <- ggplot(data,aes(method,ss_euc)) + geom_boxplot() + theme(axis.text.x = element_text(angle = 90))

ggsave('writeup/plots/pw_correlations_boxplot.pdf',p)
