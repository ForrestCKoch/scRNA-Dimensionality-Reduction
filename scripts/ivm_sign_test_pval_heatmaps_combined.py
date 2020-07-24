import sys
import os

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

plt.rcParams.update({'font.size': 6})

def get_ranks():
    return pd.read_csv('writeup/spreadsheets/ivm_median_ranks.csv')

def get_pvals(measure):
    return pd.read_csv('writeup/spreadsheets/ivm_sign_tests/ivm_sign_test_'+measure+'.csv').set_index('Unnamed: 0')

def fill_matrix(x):
    return x.fillna(0).values+x.fillna(0).T.values + np.eye(x.values.shape[0]) 

def sort_by_ranks(ranks,pv_matrix,measure):
    #print(ranks[ranks['measure'] == measure].values)
    print(ranks)
    print(pv_matrix)
    print(measure)
    idx = np.argsort(ranks[ranks['measure'] == measure].values[0][1:])
    mlist = ranks.columns[1:][idx].tolist()
    return pd.DataFrame(pv_matrix[idx][:,idx],index=mlist,columns=mlist)

if __name__ == '__main__':

    fig, axes = plt.subplots(3,2,figsize=(6,9))#,sharex='col',sharey='row')
    ranks = get_ranks()
    for measure, ax in zip(['vrc','dbs','ss-euc','ss-seu','ss-cor','ss-cos'],axes.flatten()):
        pvals = get_pvals(measure)
        #pval_mat = fill_matrix(pvals)
        ordered = sort_by_ranks(ranks,pvals.values,measure)
        sns.heatmap(ordered,cmap='viridis',xticklabels=ordered.index.tolist(),yticklabels=ordered.index.tolist(),cbar=False,ax=ax,vmin=0,vmax=0.5)
        ax.set_title(measure)
    plt.tight_layout()
    plt.savefig('writeup/plots/ivm_pvals/ivm_sign_test_all.pdf')
    #plt.show()
        
