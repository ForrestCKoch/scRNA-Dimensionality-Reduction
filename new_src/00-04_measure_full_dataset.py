import os
import pickle
from itertools import product

import pandas as pd
import numpy as np
from sklearn.metrics import calinski_harabasz_score as vrc
from sklearn.metrics import silhouette_score as ss

EXCLUDED_TYPES = ["alpha.contaminated", "beta.contaminated", "delta.contaminated", "Excluded", "gamma.contaminated", "miss", "NA", "not applicable", "unclassified", "unknown", "Unknown", "zothers",'nan']

def f1(x):
    m = x.groupby('cell_type').mean()
    s = x.groupby('cell_type').std()
    ftot = 0
    for i in range(m.shape[0]):
        fmin = None
        for j in range(m.shape[0]):
            if i == j:
                continue
            f = ((m.iloc[i]-m.iloc[j])**2/(s.iloc[i]**2+s.iloc[j]**2)).max()
            fmin = min(fmin,f) if fmin is not None else f
        ftot += fmin
    return ftot/m.shape[0]
    pass

if __name__ == '__main__':
    for pkl in os.listdir('data/datasets/pddf'):
        try:
            x = pickle.load(open('data/datasets/pddf/'+pkl,'rb'))
            to_remove = []
            for i in range(len(x.cell_type)):
                if x.cell_type[i] in EXCLUDED_TYPES or pd.isna(x.cell_type[i]):
                    to_remove.append(i)
            x.drop(index=to_remove,inplace=True)
            dat = x.drop('cell_type',axis=1)
            lab = x.cell_type
            print('{},{},{},{}'.format(pkl,vrc(dat,lab),ss(dat,lab),f1(x)))
        except Exception as e:
            #print(e)
            #print(set(x.cell_type))
            print('{},{},{},{}'.format(pkl,np.nan,np.nan,np.nan))
