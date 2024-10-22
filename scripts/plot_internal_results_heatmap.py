import sys
import re

import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 6})


if __name__ == '__main__':
    filename='data/results/internal_validation_measures/internal_measures_reduced.csv'
    x = pd.read_csv(filename).dropna()
    #x = x[x['method'] != 'saucie']
    #y = pd.read_csv('data/results/dataset_info.csv')
    # alter the following line to change the dataset ordering
    #x['dataset'] = pd.Categorical(x['dataset'],y.sort_values('protocol',ascending=False)['dataset'].values) 
    #x['dataset'] = pd.Categorical(x['dataset'],y.sort_values('n_classes',ascending=False)['dataset'].values) 
    grouped = x.groupby(['dataset','method'])

    # Used to isolate "best" measures
    mdict = {'ss_euc':'max','ss_seu':'max','ss_cor':'max','ss_cos':'max','vrc':'max','dbs':'min'}
    aggrd = grouped.agg(mdict)

    # Used to transform the "best" measures, so they can be sensibly scaled
    fdict = {'ss_euc':lambda x : x,'ss_seu':lambda x : x,'ss_cor':lambda x : x,'ss_cos':lambda x : x,'vrc':lambda x: np.log(x),'dbs':lambda x: 1/x if x > 0 else np.nan}
    trans = aggrd.transform(fdict) # apply transform

    # NOTE: the minimum is calculated as the 2nd worst performer in order to improve contrast
    trans_mins = trans.groupby('dataset').agg(lambda z: np.partition(z,2,axis=None)[1]) # calculate minimums by group
    trans_maxs = trans.groupby('dataset').agg(np.nanmax) # calculate maximums by group
    scaled = (trans - trans_mins) / (trans_maxs - trans_mins) # apply the scaling
    #scaled = aggrd
    
    # Reshape into the form needed for the heatmap
    stacked = scaled.stack() 
    stacked.index.rename(['dataset','method','measure'],inplace=True)
    # Finally, our final dataframe!
    X = pd.DataFrame(stacked).pivot_table(index=['measure','dataset'],columns=['method'])
    X.to_csv('test.csv')

    # write our dataframe
    X.to_csv('data/results/internal_measures_standardized.csv')

    ylabs = list(X.index.levels[0][X.index.codes[0]])
    curr = ylabs[0]
    ylabs[0] = re.sub('_',' ',ylabs[0])
    sep_lines = []
    for i in range(1,len(ylabs)):
        if ylabs[i] == curr:
            ylabs[i] = None
        else:
            curr = ylabs[i]
            if curr == 'dbs':
                ylabs[i] = 'dbi'
            elif curr == 'ss_seu':
                ylabs[i] = 'ss seu'
            elif curr == 'ss_euc':
                ylabs[i] = 'ss euc'
            elif curr == 'ss_cor':
                ylabs[i] = 'ss cor'
            elif curr == 'ss_cos':
                ylabs[i] = 'ss cos'
            else:
                ylabs[i] = 'vrc'
            sep_lines.append(i)


    xlabs = list(X.columns.levels[1])

    ylabs = [i.upper() if i is not None else None for i in ylabs]
    xlabs = [i.upper() for i in xlabs]

    #Make some adjustments to names
    to_replace = {'MCTSNE':'TSNE','NMF2':'NMF-LEE','NMF':'NMF-NNSVD'}
    xlabs = [i if i not in to_replace else to_replace[i] for i in xlabs]

    X[np.isnan(X)] = 0
    X_col_med = np.median(X,axis=0)
    col_order = np.flip(np.argsort(X_col_med))

    ax = sns.heatmap(X.values[:,col_order],0,1,cmap='viridis',yticklabels=ylabs,xticklabels=[xlabs[i] for i in col_order])
    ax.hlines(sep_lines, colors='r', linestyles='dotted', *ax.get_xlim())
    #plt.show()
    plt.tick_params(axis='y',which='both',left=False)
    plt.tight_layout()
    plt.savefig('writeup/plots/internal_measures_new.pdf', transparent=True)
    #plt.show()

