#!/usr/bin/env python3
import sys
import pickle

import numpy as np
import pandas as pd

from sklearn.metrics import silhouette_score as ss
from sklearn.metrics import calinski_harabasz_score as vrc
from sklearn.metrics import davies_bouldin_score as dbs

from sklearn.preprocessing import LabelEncoder

EXCLUDED_TYPES = ["alpha.contaminated", "beta.contaminated", "delta.contaminated", "Excluded", "gamma.contaminated", "miss", "NA", "not applicable", "unclassified", "unknown", "Unknown", "zothers"]

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: {} [path_to_embedding]".format(sys.argv[0]),file=sys.stderr)
        exit()

    with open(sys.argv[1],'rb') as fh:
        x = pickle.load(fh)
        to_remove = []
        for i in range(len(x.cell_type)):
            if x.cell_type[i] in EXCLUDED_TYPES:
                to_remove.append(i)
        x.drop(index=to_remove,inplace=True)
        X = x.drop('cell_type',axis=1).values

    labels = LabelEncoder().fit_transform(x.cell_type)

    try:
        ss_euc = str(ss(X,labels,metric='euclidean'))
    except Exception as e:
        print(e)
        ss_euc = str(np.nan)

    try:
        ss_seu = str(ss(X,labels,metric='seuclidean',V=np.var(X,axis=0,ddof=1,dtype=np.double)))
    except Exception as e:
        print(e)
        ss_seu = str(np.nan)

    try:
        ss_cor = str(ss(X,labels,metric='correlation'))
    except Exception as e:
        print(e)
        ss_cor = str(np.nan)

    try:
        ss_cos = str(ss(X,labels,metric='cosine'))
    except Exception as e:
        print(e)
        ss_cos = str(np.nan)

    try:
        vrc_score = str(vrc(X,labels))
    except Exception as e:
        print(e)
        vrc_score = str(np.nan)

    try:
        dbs_score = str(dbs(X,labels))
    except Exception as e:
        print(e)
        dbs_score = str(np.nan)

    print(','.join([sys.argv[1],ss_euc,ss_seu,ss_cor,ss_cos,vrc_score,dbs_score]))

