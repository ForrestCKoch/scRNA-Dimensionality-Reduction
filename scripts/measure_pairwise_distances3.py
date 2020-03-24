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
    X = data[np.isfinite(data)]
    lwr = np.percentile(X,lperc)
    upr = np.percentile(X,uperc)
    hist = np.histogram(X,bins,(lwr,upr),density=True)
    
    try:
        os.makedirs(folder)
    except FileExistsError:
        pass
    with open(os.path.join(folder,name+'.pkl'),'wb') as fh:
        pickle.dump(hist,fh)

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Usage: {} metric count_type dataset '.format(sys.argv[0]))
        exit()
    dataset = sys.argv[3]
    metric = sys.argv[1]
    count = sys.argv[2]

    if dataset not in os.listdir('data/embeddings'):
        print('Couldn\'t find dataset: {}'.format(dataset))
        exit()
    if metric not in ['euclidean','seuclidean','correlation','cosine']:
        print('Invalid distance measure...')
        exit()
    if count not in os.listdir(os.path.join('data/embeddings',dataset)):
        print('Invalid count type')
        exit()

    dists_full_ds = get_dists(os.path.join('data/datasets/pddf',count+'_'+dataset+'.pkl'),metric)

    hist_folder = os.path.join('data/results/histograms',dataset,count)
    write_histogram(dists_full_ds,hist_folder,'full')

    with open(os.path.join('data/results/pairwise_distances/',metric,count+'_'+dataset+'.csv'),'a') as fh:
        print('metric,dataset,count,method,dimensions,rho',file=fh)
        for method in os.listdir(os.path.join('data/embeddings',dataset,count)):
            for pkl in glob.glob(os.path.join('data/embeddings',dataset,count,method,'*.pkl')):
                ndims = pkl.split('/')[-1].split('.')[0]
                try:
                    dists_emb = get_dists(pkl,metric)
                    x,_ = scor(dists_full_ds,dists_emb)
                    print('{},{},{},{},{},{}'.format(metric,dataset,count,method,ndims,x),file=fh)
                    fh.flush()
                    hist_folder = os.path.join('data/results/histograms',dataset,count,method)
                    write_histogram(dists_emb,hist_folder,ndims)
                except:
                    continue
                


