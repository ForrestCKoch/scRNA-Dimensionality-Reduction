#!/usr/bin/env python3

import os
import sys
import glob
import pickle

import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist
from scipy.sparse import issparse
from scipy.stats import spearmanr as scor


def get_dists(filename,metric,exclude=True):
    EXCLUDED_TYPES = ["alpha.contaminated", "beta.contaminated", "delta.contaminated", "Excluded", "gamma.contaminated", "miss", "NA", "not applicable", "unclassified", "unknown", "Unknown", "zothers"]
    with open(filename,'rb') as fh:
        x = pickle.load(fh)
        if exclude:
            to_remove = []
            for i in range(len(x.cell_type)):
                if x.cell_type[i] in EXCLUDED_TYPES:
                    to_remove.append(i)
            x.drop(index=to_remove,inplace=True)
        X = x.drop('cell_type',axis=1).values
        del x
        if issparse(X[0][0]):
            X = np.array(np.concatenate([i[0].todense() for i in X]))
    return pdist(X,metric)
    
def write_histogram(data,folder,name,lperc=2.5,uperc=97.5,bins=100):
    lwr = np.percentile(data,lperc)
    upr = np.percentile(data,uperc)
    hist = np.histogram(data,bins,(lwr,upr),density=True)
    
    try:
        os.makedirs(folder)
    except FileExistsError:
        pass
    with open(os.path.join(folder,name+'.pkl'),'wb') as fh:
        pickle.dump(hist,fh)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {} pkl metric'.format(sys.argv[0]))
        exit()
    pkl = sys.argv[1]
    metric = sys.argv[2]

    _,_,dataset,count,method,_ = pkl.split('/')

    if metric not in ['euclidean','seuclidean','correlation','cosine']:
        print('Invalid distance measure...')
        exit()

    dists_full_ds = get_dists(os.path.join('data/datasets/pddf',count+'_'+dataset+'.pkl'),metric)

    hist_folder = os.path.join('data/results/histograms',dataset,count)
    write_histogram(dists_full_ds,hist_folder,'full')

    ndims = pkl.split('/')[-1].split('.')[0]
    dists_emb = get_dists(pkl,metric)
    x,_ = scor(dists_full_ds,dists_emb)
    print('{},{},{},{},{},{}'.format(metric,dataset,count,method,ndims,x))
    hist_folder = os.path.join('data/results/histograms',dataset,count,method)
    write_histogram(dists_emb,hist_folder,ndims)
                


