import sys
import os
import re

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import re

plt.rcParams.update({'font.size': 6})

def get_ranks():
    return pd.read_csv('writeup/spreadsheets/ivm_median_ranks.csv')

def get_pvals(measure):
    return pd.read_csv('writeup/spreadsheets/ivm_sign_tests/ivm_sign_test_'+measure+'.csv').set_index('Unnamed: 0')

def fill_matrix(x):
    return x.fillna(0).values+x.fillna(0).T.values + np.eye(x.values.shape[0]) 

def sort_by_ranks(ranks,pv_matrix,measure):
    idx = np.argsort(ranks[ranks['measure'] == measure].values[0][1:])
    mlist = ranks.columns[1:][idx].tolist()
    return pd.DataFrame(pv_matrix[idx][:,idx],index=mlist,columns=mlist)

if __name__ == '__main__':

    fig, axes = plt.subplots(1,3,figsize=(9,3))#,sharex='col',sharey='row')
    ranks = get_ranks()
    to_replace = {'mctsne':'tsne','nmf2':'nmf-lee','nmf':'nmf-nnsvd'}
    for measure, ax in zip(['vrc','dbs','ss-euc'],axes.flatten()):
        pvals = get_pvals(measure)
        ordered = sort_by_ranks(ranks,pvals.values,measure)
        xlabs = [re.sub('\.','-',i) if i not in to_replace else to_replace[i] for i in ordered.index.tolist()]
        sns.heatmap(ordered,cmap='viridis',xticklabels=xlabs,yticklabels=xlabs,cbar=False,ax=ax,vmin=0,vmax=0.5)
        ax.set_title(measure)
    plt.tight_layout()
    #plt.savefig('writeup/plots/ivm_pvals/ivm_sign_test_all-final.pdf')
    plt.show()
        
