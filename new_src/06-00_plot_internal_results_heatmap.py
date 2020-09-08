import sys
import re

import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler as scaler
plt.rcParams.update({'font.size': 6})


# if __name__ == '__main__':
if True:
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
    fdict = {'ss_euc':lambda x : x,'ss_seu':lambda x : x,'ss_cor':lambda x : x,'ss_cos':lambda x : x,'vrc':lambda x: np.log(x),'dbs':lambda x: 1/x if x > 0 else 0}
    #fdict = {'ss_euc':lambda x : (x+1)/2,'ss_seu':lambda x : x,'ss_cor':lambda x : x,'ss_cos':lambda x : x,'vrc':lambda x: np.log(x)/10,'dbs':lambda x: 1/(1.5*x) if x > 0 else np.nan}
    trans = aggrd.transform(fdict) # apply transform

    # NOTE: the minimum is calculated as the 2nd worst performer in order to improve contrast
    trans_mins = trans.groupby('dataset').agg(lambda z: np.partition(z,2,axis=None)[1]) # calculate minimums by group
    trans_maxs = trans.groupby('dataset').agg(np.nanmax) # calculate maximums by group
    #trans_mins = trans.agg(lambda z: np.partition(z,2,axis=None)[1]) # calculate minimums by group
    #trans_maxs = trans.agg(lambda z: np.partition(z,-2,axis=None)[-2]) # calculate maximums by group
    scaled = (trans - trans_mins) / (trans_maxs - trans_mins) # apply the scaling
    #scaled = trans
    #scaled = aggrd
    #scaled = trans
    #scaled[:] = scaler().fit_transform(scaled)
    
    # Reshape into the form needed for the heatmap
    stacked = scaled.stack() 
    stacked.index.rename(['dataset','method','measure'],inplace=True)
    # Finally, our final dataframe!
    X = pd.DataFrame(stacked).pivot_table(index=['measure','dataset'],columns=['method'])
    # write our dataframe
    X.to_csv('data/results/internal_measures_standardized.csv')

    # remove non-euclidean options ...
    X.drop(index='ss_cos',inplace=True)
    X.drop(index='ss_cor',inplace=True)
    X.drop(index='ss_seu',inplace=True)

    t = pd.read_csv('writeup/spreadsheets/dataset_complexity2.csv')
    u = pd.read_csv('tmp/datasets_used_GJS.csv')
    t = t.merge(u,on='dataset')
    #t['complexity'] =  t['complexity'] + (t['read.type'] == 'Reads')
    #t['f1'] =  t['f1'] + (t['read.type'] == 'Reads')
    #print(t)
    tdict = dict(zip(t['dataset'],t['full_ss']))
    #tdict = dict(zip(t['dataset'],t['f1']))
    tdict['vrc'] = 2
    tdict['dbs'] = 0
    tdict['ss_euc'] = 1
    #print(tdict.keys())

    #print(X.sort_index(key=lambda x: [tdict[i] for i in x.values],inplace=True))
    X.sort_index(key=lambda x: [tdict[i] for i in x.values],inplace=True)
    #print(X.sort_index(inplace=True))

    ylabs = list(X.index.levels[0][X.index.codes[0]])
    curr = ylabs[0]
    ylabs[0] = re.sub('_euc','',ylabs[0])
    sep_lines = []
    ylabs_copy = ylabs.copy()
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
                ylabs[i] = 'ss'
            elif curr == 'ss_cor':
                ylabs[i] = 'ss cor'
            elif curr == 'ss_cos':
                ylabs[i] = 'ss cos'
            else:
                ylabs[i] = 'vrc'
            sep_lines.append(i)


    xlabs = list(X.columns.levels[1])

    ylabs = [i.upper() if i is not None else None for i in ylabs]
    # no uppercase methods ...
    #xlabs = [i.upper() for i in xlabs]

    #Make some adjustments to names
    to_replace = {'mctsne':'tsne','nmf2':'nmf-lee','nmf':'nmf-nnsvd'}
    xlabs = [i if i not in to_replace else to_replace[i] for i in xlabs]

    X[np.isnan(X)] = 0
    X_col_med = np.median(X,axis=0)
    col_order = np.flip(np.argsort(X_col_med))

    fig, axes = plt.subplots(3,1,sharex='col')
    #print(ylabs_copy)
    x = X.iloc[np.array(ylabs_copy) == 'dbs',:]
    sns.heatmap(x.values[:,col_order],0,1,cmap='viridis',yticklabels=['dbs'],xticklabels=[],ax=axes.flatten()[0])
    x = X.iloc[np.array(ylabs_copy) == 'vrc',:]
    sns.heatmap(x.values[:,col_order],0,1,cmap='viridis',yticklabels=['vrc'],xticklabels=[],ax=axes.flatten()[1])
    x = X.iloc[np.array(ylabs_copy) == 'ss_euc',:]
    sns.heatmap(x.values[:,col_order],0,1,cmap='viridis',yticklabels=['ss'],xticklabels=[xlabs[i] for i in col_order],ax=axes.flatten()[2])
    """
    #ax = sns.heatmap(X.values[:,col_order],0,1,cmap='viridis',yticklabels=ylabs,xticklabels=[xlabs[i] for i in col_order])
    ax = sns.heatmap(X.values[:,col_order],0,1,cmap='viridis',yticklabels=ylabs,xticklabels=[xlabs[i] for i in col_order])
    ax.hlines(sep_lines, colors='r', linestyles='dotted', *ax.get_xlim())
    """
    #plt.show()
    for i in axes.flatten():
        i.tick_params(axis='y',which='both',left=False)
        i.tick_params(axis='x',which='both',bottom=False)
    plt.tight_layout()
    plt.savefig('writeup/plots/internal_measures_final.pdf', transparent=True)
    #plt.show()

