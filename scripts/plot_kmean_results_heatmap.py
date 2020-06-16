import sys

import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt


if __name__ == '__main__':
    acc = sys.argv[1]
    x = pd.read_csv('data/results/optimal_kmeans_trials.csv').dropna()
    grouped = x.groupby(['dataset','method'])

    d = {'dataset':[],'method':[],'ss':[],'vrc':[],'dbs':[]}#,acc:[]}
    for group in grouped.groups.keys():
        pass
        #print(group)
        data = pd.DataFrame(grouped.get_group(group))
        d['dataset'].append(group[0])
        d['method'].append(group[1])
        d['ss'].append(data[acc].iloc[np.argmax(data['ss'])])
        d['vrc'].append(data[acc].iloc[np.argmax(data['vrc'])])
        d['dbs'].append(data[acc].iloc[np.argmin(data['dbs'])])
        #ari = np.max(data[acc])

    X = pd.DataFrame(d).set_index('method').pivot_table(index=['method'],columns=['dataset']).T

    ylabs = list(X.index.levels[0][X.index.codes[0]])
    curr = ylabs[0]
    sep_lines = []
    for i in range(1,len(ylabs)):
        if ylabs[i] == curr:
            ylabs[i] = None
        else:
            curr = ylabs[i]
            sep_lines.append(i)

    xlabs = list(X.columns.values)

    ax = sns.heatmap(X,cmap='viridis',xticklabels=xlabs,yticklabels=ylabs)
    ax.hlines(sep_lines, colors='r', linestyles='dotted', *ax.get_xlim())
    #plt.show()
    plt.savefig('writeup/plots/kmeans_'+acc+'.pdf')
    X.to_csv('data/results/optimal_kmeans_trials_summarized_'+acc+'.csv')

