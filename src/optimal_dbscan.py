#!/usr/bin/python3

import pickle
import sys

import numpy as np

from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score
from sklearn.metrics import calinski_harabaz_score
from sklearn.metrics import adjusted_rand_score
from sklearn.metrics import normalized_mutual_info_score

from svr2019.datasets import *

EPS_CHOICES=[0.05,0.1,0.5,1.0,5.0]
MIN_SAMP_CHOICES=[5,10,25,50]

dset = sys.argv[1]
emb_file = 'data/embeddings/' + dset + '/umap/4-log-False.pickle'
emb = pickle.load(open(emb_file,'rb'))

raw_data = DuoBenchmark('data/datasets/'+dset+'.csv',split_head=False)

true_labels = raw_data.tags

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
        print(','.join([str(x) for x in line]))
