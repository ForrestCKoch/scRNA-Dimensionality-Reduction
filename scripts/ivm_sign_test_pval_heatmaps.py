import sys
import os

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def get_ranks():
    return pd.read_csv('writeup/spreadsheets/ivm_ranks.csv')

def get_pvals(measure):
    return pd.read_csv('writeup/spreadsheets/ivm_sign_tests/ivm_sign_test_'+measure+'.csv').set_index('X')

def fill_matrix(x):
    return x.fillna(0).values+x.fillna(0).T.values

def sort_by_ranks(ranks,pv_matrix,measure):
    #print(ranks[ranks['measure'] == measure].values)
    idx = np.argsort(ranks[ranks['measure'] == measure].values[0][1:])
    mlist = ranks.columns[1:][idx].tolist()
    return pd.DataFrame(pv_matrix[idx][:,idx],index=mlist,columns=mlist)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Bad args ...")
        exit()
    measure = sys.argv[1]
    ranks = get_ranks()
    pvals = get_pvals(measure)
    pval_mat = fill_matrix(pvals)
    ordered = sort_by_ranks(ranks,pval_mat,measure)
    sns.heatmap(ordered,cmap='viridis',xticklabels=ordered.index.tolist(),yticklabels=ordered.index.tolist())
    plt.tight_layout()
    plt.savefig('writeup/plots/ivm_pvals/ivm_sign_test_'+measure+'.pdf')
