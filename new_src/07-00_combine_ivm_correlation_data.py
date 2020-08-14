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

    d = {'dataset':[],'method':[],'r.euc':[],'r.seu':[],'r.cor':[], 'r.cos':[], 'opt.type':[], 'opt.value':[]}#,acc:[]}
    for ivm in ['ss_euc','ss_seu','ss_cor','ss_cos','vrc','dbs']:
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
            d['opt.value'].append(data[ivm].iloc[best_idx])
            d['opt.type'].append(ivm)
            #ari = np.max(data[acc])

    pd.DataFrame(d).to_csv('data/results/pw_correlations/best_ivm_combined_pw_cor.csv',index=False)
