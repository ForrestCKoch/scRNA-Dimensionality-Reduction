#!/usr/bin/env python3
##################################################
# optimal_dbscan.py
##################################################

import pickle
import sys
import os
import itertools

import numpy as np

from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score
from sklearn.metrics import calinski_harabaz_score
from sklearn.metrics import adjusted_rand_score
from sklearn.metrics import normalized_mutual_info_score

from sklearn.preprocessing import LabelEncoder

from svr2019.datasets import *
from svr2019.metrics import davies_bouldin_score
from svr2019.metrics import dunn_index

def warn(*args, **kwargs):
    """
    hack to stop sklearn from throwing annoying warnings
    """
    pass

if __name__ == '__main__':
    import warnings
    warnings.warn = warn

    dset = sys.argv[1]
    method = sys.argv[2]
    # This method of extracting labels won't work for older datasets
    dataset_file = 'data/headers/'+dset+'.csv'
    with open(dataset_file,'r') as fh:
        cell_types = fh.readline().rstrip('\n').split(',')

    le = LabelEncoder()
    true_labels = le.fit_transform(cell_types)

    # Extract following code into function which takes:
    # - true labels
    # - pickle file to load 
    first = True
    eps_choices = list(np.arange(0.025,0.5,0.025))
    ms_choices = list(range(2,15))
    for emb_file in os.listdir('data/embeddings/'+dset+'/'+method):
        full_path = 'data/embeddings/'+dset+'/'+method+'/'+emb_file
        emb = pickle.load(open(full_path,'rb'))
        result = dbscan_optimization(emb,true_labels,eps_choices,ms_choices)
        print_optimal_dbscans(dset,method,emb_file,result,header=first)
        first = False


