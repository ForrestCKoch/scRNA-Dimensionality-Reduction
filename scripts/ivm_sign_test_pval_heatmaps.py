import sys
import os
import re

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
plt.rcParams.update({'font.size': 6})

def get_ranks():
    return pd.read_csv('writeup/spreadsheets/ivm_ranks.csv')

def get_pvals(measure):
    return pd.read_csv('writeup/spreadsheets/ivm_sign_tests/ivm_sign_test_'+measure+'.csv').set_index('X')

def fill_matrix(x):
    return x.fillna(0).values+x.fillna(0).T.values+np.eye(x.values.shape[0])

def sort_by_ranks(ranks,pv_matrix,measure):
    #print(ranks[ranks['measure'] == measure].values)
    idx = np.argsort(ranks[ranks['measure'] == measure].values[0][1:])
    mlist = ranks.columns[1:][idx].tolist()
    return pd.DataFrame(pv_matrix[idx][:,idx],index=mlist,columns=mlist)

if __name__ == '__main__':
    """
    if len(sys.argv) != 2:
        print("Bad args ...")
        exit()
    measure = sys.argv[1]
    """
    fig, axes = plt.subplots(3,2)
    fig.set_figheight(9)
    fig.set_figwidth(6)
    axes = axes.flatten()
    count = 0
    to_replace = {'MCTSNE':'TSNE','NMF2':'NMF-LEE','NMF':'NMF-NNSVD'}
    for measure in ['vrc','dbs','ss-cor','ss-cos','ss-euc','ss-seu']:
        ranks = get_ranks()
        pvals = get_pvals(measure)
        pval_mat = fill_matrix(pvals)
        ordered = sort_by_ranks(ranks,pval_mat,measure)
        xlabs = [i.upper() for i in ordered.index.tolist()]
        xlabs = [i if i not in to_replace else to_replace[i] for i in xlabs]
        sns.heatmap(ordered,
                cmap='viridis',
                vmin=0,
                vmax=0.5,
                xticklabels=xlabs,
                yticklabels=xlabs,
                ax=axes[count],
                cbar=False)
        axes[count].set_title(re.sub('-',' ',measure.upper()))
        count += 1
    plt.tight_layout()
    plt.savefig('writeup/plots/ivm_pvals/ivm_sign_test_all-final.pdf')
    #plt.savefig('writeup/plots/ivm_pvals/ivm_sign_test_'+measure+'.pdf')
    #plt.savefig('writeup/plots/ivm_pvals/ivm_sign_test_'+measure+'_transparent.pdf',transparent=True)
