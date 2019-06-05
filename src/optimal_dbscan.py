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
from sklearn.metrics import *

from sklearn.preprocessing import LabelEncoder

from svr2019.datasets import *
from svr2019.metrics import *
from svr2019.clustering import *

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
    #eps_choices = list(np.arange(0.025,25,0.025))
    eps_choices = list()
    e = 50
    while e > 0.001:
        eps_choices.append(e)
        e *= 0.9

    #ms_choices = list(range(2,50))
    ms_choices = list()
    e = 50
    while e > 1:
        ms_choices.append(e)
        e = int(e*0.9)

    for emb_file in os.listdir('data/embeddings/'+dset+'/'+method):
        full_path = 'data/embeddings/'+dset+'/'+method+'/'+emb_file
        emb = pickle.load(open(full_path,'rb'))
        result = dbscan_optimization(emb,true_labels,eps_choices,ms_choices)
        print_optimal_dbscans(dset,method,emb_file,result,header=first)
        first = False
