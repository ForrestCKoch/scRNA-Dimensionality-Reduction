import sys
import re

import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt


if __name__ == '__main__':
    metric = sys.argv[1]
    acc = sys.argv[2]
    opt = sys.argv[3]
    #x = pd.read_csv('data/results/'+sys.argv[1]+'_optimal_dbscan_trials_reduced.csv').dropna()
    x = pd.read_csv('data/results/optimal_dbscan_trials/optimal_dbscan_trials_'+sys.argv[1]+'.csv').dropna()
    grouped = x.groupby(['dataset','method'])

    #d = {'dataset':[],'method':[],'ss':[],'vrc':[],'dbs':[]}#,acc:[]}
    d = {'dataset':[],'method':[],opt:[]}#,acc:[]}
    for group in grouped.groups.keys():
        pass
        #print(group)
        data = pd.DataFrame(grouped.get_group(group))
        d['dataset'].append(group[0])
        d['method'].append(group[1])
        #d['ss'].append(data[acc].iloc[np.argmax(data['ss'])])
        if opt == 'dbs':
            d[opt].append(data[acc].iloc[np.argmin(data[opt])])
        else:
            d[opt].append(data[acc].iloc[np.argmax(data[opt])])
        #d['dbs'].append(data[acc].iloc[np.argmin(data['dbs'])])
        #ari = np.max(data[acc])

    #X = pd.DataFrame(d).set_index('method').pivot_table(index=['method'],columns=['dataset']).T
    X = pd.DataFrame(d).pivot_table(index=['method'],columns=['dataset']).T
    #X.droplevel(1)
    #print(X.mean())

    """
    meds = X.median(1,numeric_only=True)
    meds.sort_values(ascending=False,inplace=True)
    #X = X[:,meds.index]
    X.boxplot()
    print(meds.index[1:])
    ylabs = list(X.index.levels[0][X.index.codes[0]])
    curr = ylabs[0]
    #sep_lines = []
    for i in range(1,len(ylabs)):
        if ylabs[i] == curr:
            ylabs[i] = None
        else:
            curr = ylabs[i]
            #sep_lines.append(i)
    """
    v = X.values
    v[np.isnan(v)] = 0
    
    # get labs and sort by median
    ylabs = np.array([re.sub('TabulaMuris_','',i[1]) for i in X.index.values])
    xlabs = np.array(X.columns.values)
    ylabs = ylabs[np.argsort(np.median(v,1))]
    xlabs = xlabs[np.flip(np.argsort(np.median(v,0)))]

    # sort columns and rows by median
    v = v[np.argsort(np.median(v,1)),:][:,np.flip(np.argsort(np.median(v,0)))]

    plt.rcParams.update({'font.size': 8})
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2,figsize=(10,8),sharex='col',sharey='row',gridspec_kw={"height_ratios": (.15, .85),"width_ratios":(0.85,0.15)})
    # Boxplots
    #sns.boxplot(y=np.repeat(xlabs,55),x=v.flatten('F'),ax=ax4,orient='h')
    #sns.boxplot(x=np.repeat(ylabs,33),y=v.flatten(),ax=ax1)
    ax4.boxplot(v,vert=False,positions=np.array(range(33))+0.5)
    ax4.get_yaxis().set_ticklabels([])
    ax4.tick_params(labelbottom=False)
    ax1.boxplot(v.T,positions=np.array(range(55))+0.5)
    ax1.get_xaxis().set_ticklabels([])
    
    #print(','.join([str(i) for i in (np.concatenate(np.mean(v,0)[np.argsort(xlabs)],[np.mean(v)]))]))
    #print(v.shape) 
    w = v[np.where(v.max(1)>0.5)[0],:]
    #print(w.shape)
    #print(','.join([opt,metric]+[str(i) for i in np.mean(v,0)[np.argsort(xlabs)]]+[str(np.mean(v))]))
    print(','.join([opt,metric]+[str(i) for i in np.mean(w,0)[np.argsort(xlabs)]]+[str(np.mean(w))]))
    #print(','.join(['measure,metric']+list(np.sort(xlabs))+['overall']))

    # Heatmap
    ax = sns.heatmap(v.T,cmap='viridis',xticklabels=ylabs,yticklabels=[i.upper() for i in xlabs], ax=ax3,vmin=0,vmax=1,cbar=False)
    plt.rcParams.update({'axes.labelsize':'x-small'})
    plt.tight_layout()
    #plt.show()
    plt.savefig('writeup/plots/dbscan_new_heatmaps/dbscan_'+metric+'_'+opt+'_'+acc+'_transparent.pdf',transparent=True)
    #X.to_csv('data/results/optimal_dbscan_trials/optimal_dbscan_trials_summarized_'+metric+'_'+opt+'_'+acc+'.csv')
