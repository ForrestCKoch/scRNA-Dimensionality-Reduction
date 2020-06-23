import sys
import re
import os
import pickle
import re

import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import DBSCAN
plt.rcParams.update({'font.size': 8})

EXCLUDED_TYPES = ["alpha.contaminated", "beta.contaminated", "delta.contaminated", "Excluded", "gamma.contaminated", "miss", "NA", "not applicable", "unclassified", "unknown", "Unknown", "zothers"]

opt='vrc'
acc='ari'
methods = ['phate','vasc','fica','umap']
#datsets = ['TabulaMuris_Mammary_10X', 'deng-rpkms','li','TabulaMuris_Heart_10X','chen']
datsets = ['TabulaMuris_Mammary_10X','li','chen']

euc = pd.read_csv('data/results/optimal_dbscan_trials/optimal_dbscan_trials_euclidean.csv').dropna()

fig, axes = plt.subplots(3,4,figsize=(12,9))
axes = axes.flatten()
idx = 0

for d in datsets:
    for m in methods:
        row = euc[(euc.dataset==d).values & (euc.method == m).values & (euc.loss_criteria == 'vrc').values]
        count_type = row.count_type.values[0]
        eps = row.eps.values[0]
        minpts = row.minpts.values[0]
        dims = row.dimensions.values[0]
        file_to_cluster =  os.path.join('data/embeddings',d,count_type,m,str(dims)+'.pkl')
        file_to_show =  os.path.join('data/embeddings',d,count_type,m,'2.pkl')
        cluster_dat = pickle.load(open(file_to_cluster,'rb'))
        show_dat = pickle.load(open(file_to_show,'rb'))

        to_remove = []
        for i in range(len(cluster_dat.cell_type)):    
            if cluster_dat.cell_type[i] in EXCLUDED_TYPES:    
                to_remove.append(i) 

        cluster_dat.drop(index=to_remove,inplace=True)    
        show_dat.drop(index=to_remove,inplace=True)    
        curr_idx = int(((2*idx)%12)+np.floor(idx/6))
        axes[idx].scatter(show_dat.values[:,1],show_dat.values[:,2],c=LabelEncoder().fit_transform(show_dat.values[:,0]),s=3)
        axes[idx].set_title(re.sub(r'TabulaMuris','TM',d)+' '+m)
        idx += 1

plt.tight_layout()
#plt.show()
plt.savefig('writeup/plots/scatterplots_from_best_dbscan.pdf')
