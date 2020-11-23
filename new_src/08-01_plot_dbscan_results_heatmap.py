"""
    
"""
import sys
import re
import pprint

import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt


if __name__ == '__main__':
    metric = sys.argv[1]
    acc = sys.argv[2]
    opt = sys.argv[3]

    x = pd.read_csv('data/results/optimal_dbscan_trials/optimal_dbscan_trials_'+sys.argv[1]+'.csv').dropna()
    grouped = x.groupby(['dataset','method'])

    d = {'dataset':[],'method':[],opt:[]}#,acc:[]}
    for group in grouped.groups.keys():
        pass
        data = pd.DataFrame(grouped.get_group(group))
        d['dataset'].append(group[0])
        d['method'].append(group[1])
        if opt == 'dbs':
            d[opt].append(data[acc].iloc[np.argmin(data[opt])])
        else:
            d[opt].append(data[acc].iloc[np.argmax(data[opt])])

    X = pd.DataFrame(d).pivot_table(index=['method'],columns=['dataset']).T

    v = X.values
    v[np.isnan(v)] = 0
    
    # get labs and sort by median
    ylabs = np.array([re.sub('TabulaMuris_','',i[1]) for i in X.index.values])
    xlabs = np.array(X.columns.values)
    ylabs = ylabs[np.argsort(np.median(v,1))]
    pprint.PrettyPrinter(depth=6).pprint(dict(zip(xlabs,np.mean(v,0))))
    xlabs = xlabs[np.flip(np.argsort(np.mean(v,0)))]
    to_replace = {'mctsne':'tsne','nmf2':'nmf-lee','nmf':'nmf-nnsvd'}
    xlabs = [i if i not in to_replace else to_replace[i] for i in xlabs]

    # sort columns and rows by median
    v = v[np.argsort(np.median(v,1)),:][:,np.flip(np.argsort(np.mean(v,0)))]

    plt.rcParams.update({'font.size': 8})
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2,figsize=(10,8),sharex='col',sharey='row',gridspec_kw={"height_ratios": (.15, .85),"width_ratios":(0.85,0.15)})
    # Boxplots
    ax4.boxplot(v,vert=False,positions=np.array(range(33))+0.5)
    ax4.get_yaxis().set_ticklabels([])
    ax4.tick_params(labelbottom=False)
    ax1.boxplot(v.T,positions=np.array(range(55))+0.5)
    ax1.get_xaxis().set_ticklabels([])
    
    w = v[np.where(v.max(1)>0.5)[0],:]

    # Heatmap
    ax = sns.heatmap(v.T,cmap='viridis',xticklabels=ylabs,yticklabels=[i.lower() for i in xlabs], ax=ax3,vmin=0,vmax=1,cbar=False)
    plt.rcParams.update({'axes.labelsize':'x-small'})
    plt.tight_layout()
    #plt.savefig('writeup/plots/dbscan_new_heatmaps/dbscan_'+metric+'_'+opt+'_'+acc+'_transparent.pdf',transparent=True)
    #X.to_csv('data/results/optimal_dbscan_trials/optimal_dbscan_trials_summarized_'+metric+'_'+opt+'_'+acc+'.csv')
    plt.show()
