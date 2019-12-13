import sys

import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt


if __name__ == '__main__':
    x = pd.read_csv(sys.argv[1]).dropna()
    grouped = x.groupby(['dataset','method'])

    # Used to isolate "best" measures
    mdict = {'ss_euc':'max','ss_seu':'max','ss_cor':'max','ss_cos':'max','vrc':'max','dbs':'min'}
    aggrd = grouped.agg(mdict)

    # Used to transform the "best" measures, so they can be sensibly scaled
    fdict = {'ss_euc':lambda x : x,'ss_seu':lambda x : x,'ss_cor':lambda x : x,'ss_cos':lambda x : x,'vrc':lambda x: np.log(x),'dbs':lambda x: 1/x if x > 0 else np.nan}
    trans = aggrd.transform(fdict) # apply transform
    trans_mins = trans.groupby('dataset').agg(np.nanmin) # calculate minimums by group
    trans_maxs = trans.groupby('dataset').agg(np.nanmax) # calculate maximums by group
    scaled = (trans - trans_mins) / (trans_maxs - trans_mins) # apply the scaling
    
    # Reshape into the form needed for the heatmap
    stacked = scaled.stack() 
    stacked.index.rename(['dataset','method','measure'],inplace=True)
    # Finally, our final dataframe!
    X = pd.DataFrame(stacked).pivot_table(index=['measure','dataset'],columns=['method'])

    ylabs = list(X.index.levels[0][X.index.codes[0]])
    curr = ylabs[0]
    sep_lines = []
    for i in range(1,len(ylabs)):
        if ylabs[i] == curr:
            ylabs[i] = None
        else:
            curr = ylabs[i]
            sep_lines.append(i)

    xlabs = list(X.columns.levels[1])

    ax = sns.heatmap(X,cmap='viridis',xticklabels=xlabs,yticklabels=ylabs)
    ax.hlines(sep_lines, colors='r', linestyles='dotted', *ax.get_xlim())
    plt.show()

