#!/usr/bin/env python3
##################################################
# optimal_dbscan.py
##################################################

import pickle
import sys
import os

import numpy as np

from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score
from sklearn.metrics import calinski_harabaz_score
from sklearn.metrics import adjusted_rand_score
from sklearn.metrics import normalized_mutual_info_score

from sklearn.preprocessing import LabelEncoder

from svr2019.datasets import *

def warn(*args, **kwargs):
    """
    hack to stop sklearn from throwing annoying warnings
    """
    pass

if __name__ == '__main__':
    import warnings
    warnings.warn = warn

    EPS_CHOICES=[0.001,0.0025,0.005,0.0075,0.01,0.025,0.05,0.075,0.1,0.25,0.5,0.75,1.0,2.5,5.0]
    MIN_SAMP_CHOICES=[1,2,3,4,5,10,15,20,25,35,50]

    dset = sys.argv[1]
    #emb_file = 'data/embeddings/' + dset + '/umap/4-log-False.pickle'
    #emb_file = sys.argv[2]
    #emb = pickle.load(open(emb_file,'rb'))
    #raw_data = DuoBenchmark('data/datasets/'+dset+'.csv',split_head=False)
    dataset_file = 'data/datasets/'+dset+'.csv'
    with open(dataset_file,'r') as fh:
        cell_types = fh.readline().rstrip('\n').split(',')

    le = LabelEncoder()
    le.fit(cell_types)
    true_labels = le.transform(cell_types)


    for emb_file in os.listdir('data/embeddings/'+dset+'/lda'):
        emb_file = 'data/embeddings/'+dset+'/lda/'+emb_file
        emb = pickle.load(open(emb_file,'rb'))

        for eps in EPS_CHOICES:
            for min_samp in MIN_SAMP_CHOICES:
                db = DBSCAN(eps=eps,min_samples=min_samp).fit(emb)
                labels = db.labels_
                n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
                if n_clusters > 1:
                    vrc = calinski_harabaz_score(emb,labels)
                    ss = silhouette_score(emb,labels)
                    ari = adjusted_rand_score(true_labels,labels)
                    nmi = normalized_mutual_info_score(true_labels,labels)
                else:
                    vrc = -1
                    ss = -1
                    ari = -1
                    nmi = -1

                line = [eps,min_samp,n_clusters,vrc,ss,ari,nmi] 
                print(','.join([emb_file]+[str(x) for x in line]))
                sys.stdout.flush()
