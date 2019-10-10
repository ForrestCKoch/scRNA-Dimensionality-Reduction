#!/usr/bin/env python3
##################################################
# plot_heatmap.py
##################################################

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sc_dm.sumarize import *

if __name__ == '__main__':
    methods = ['fa','fica','isomap','lda','lle','mctsne','nmf','pca','sdae','umap']
    plot_optimal_heatmap(sys.argv[1], 'results/csvs/internal_metrics_reduced.csv',methods)
