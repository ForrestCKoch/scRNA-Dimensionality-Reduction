import sys

import pandas as pd
import numpy as np

#import seaborn as sns
#import matplotlib.pyplot as plt


if __name__ == '__main__':
    z = pd.read_csv('data/results/internal_validation_measures/internal_measures_reduced.csv').dropna()
    y = pd.read_csv('data/results/pairwise_distances/pairwise_correlations_all.csv')
    x = z.merge(y)
    grouped = x.groupby(['dataset','method'])

    for ivm in ['ss_euc','ss_seu','ss_cor','ss_cos','vrc','dbs']:
        d = {'dataset':[],'method':[],'r.euc':[],'r.seu':[],'r.cor':[], 'r.cos':[]}#,acc:[]}
        for group in grouped.groups.keys():
            pass
            #print(group)
            data = pd.DataFrame(grouped.get_group(group))
            d['dataset'].append(group[0])
            d['method'].append(group[1])
            if ivm == 'dbs':
                best_idx = np.argmin(data[ivm])
            else:
                best_idx = np.argmax(data[ivm])

            d['r.euc'].append(data['rho.euclidean'].iloc[best_idx])
            d['r.seu'].append(data['rho.seuclidean'].iloc[best_idx])
            d['r.cor'].append(data['rho.correlation'].iloc[best_idx])
            d['r.cos'].append(data['rho.cosine'].iloc[best_idx])
            #ari = np.max(data[acc])

        X = pd.DataFrame(d).groupby('method').mean()

        ylabs = list(X.index.values)

        xlabs = list(X.columns.values)

        #ax = sns.heatmap(X,cmap='viridis',xticklabels=xlabs,yticklabels=ylabs)
        #plt.show()
        #plt.savefig("test.pdf")
        #plt.savefig('writeup/plots/pw_correlations-'+ivm+'.pdf')
        #plt.clf()
        X.to_csv('data/results/pw_correlations/pw_correlations-'+ivm+'.csv')

    d = {'dataset':[],'method':[],'ss_euc':[],'ss_seu':[],'ss_cor':[],'ss_cos':[],'vrc':[],'dbs':[]}#,acc:[]}
    for group in grouped.groups.keys():
        data = pd.DataFrame(grouped.get_group(group))
        d['dataset'].append(group[0])
        d['method'].append(group[1])
        best_idx = np.argmax(data[ivm])
        d['ss_euc'].append(data['rho.euclidean'].iloc[np.argmax(data['ss_euc'])])
        d['ss_seu'].append(data['rho.seuclidean'].iloc[np.argmax(data['ss_seu'])])
        d['ss_cor'].append(data['rho.correlation'].iloc[np.argmax(data['ss_cor'])])
        d['ss_cos'].append(data['rho.cosine'].iloc[np.argmax(data['ss_cos'])])
        d['vrc'].append(data['rho.euclidean'].iloc[np.argmax(data['vrc'])])
        d['dbs'].append(data['rho.euclidean'].iloc[np.argmin(data['dbs'])])
        #ari = np.max(data[acc])

    X = pd.DataFrame(d).groupby('method').mean()
    pd.DataFrame(d).to_csv('data/results/pw_correlations/pw_correlations_by_best_ivm.csv')

    ylabs = list(X.index.values)

    xlabs = list(X.columns.values)

    #ax = sns.heatmap(X,cmap='viridis',xticklabels=xlabs,yticklabels=ylabs)
    #plt.show()
    #plt.savefig("test.pdf")
    #plt.savefig('writeup/plots/pw_correlations.pdf')
    #plt.clf()
    #X.to_csv('data/results/pw_correlations.csv')

