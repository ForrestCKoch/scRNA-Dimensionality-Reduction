#!/usr/bin/env python3
##################################################
# clustering.py
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

def dbscan_trial(data,pairwise,true_labels,eps,min_samp):
    """
    Perfoms DBSCAN with the given parameters and returns:
        - number of clusters
        - variance ratio criterion
        - silhouette score
        - davies bouldin index
        - adjusted rand index
        - normalized mutual information

    :param data: data to be clustered
    :param true_labels: true labels for the data (for ari & nmi)
    :param eps: choice of epsilon for DBSCAN
    :param min_samp: choice of min_samples for DBSCAN
    :return: dictionary in form:
        {'clusters','epsilon','min_samples','vrc','ss','db','ari','nmi'}
    """
    #labels = DBSCAN(eps=eps,min_samples=min_samp,metric='precomputed').fit(pairwise).labels_
    labels = DBSCAN(eps=eps,min_samples=min_samp).fit(data).labels_
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    if n_clusters > 1:
        try:
            vrc = calinski_harabaz_score(data,labels)
            #ss = silhouette_score(pairwise,labels,metric='precomputed')
            ss = silhouette_score(data,labels)
            db = davies_bouldin_score(data,labels)
            di = dunn_index(data,labels)
            ari = adjusted_rand_score(true_labels,labels)
            nmi = normalized_mutual_info_score(true_labels,labels)
        except Exception as exc:
            print(exc,file=sys.stderr)
            vrc,ss,db,di,ari,nmi = [np.nan]*6
    else:
        vrc,ss,db,di,ari,nmi = [np.nan]*6
    return {'clusters':n_clusters,
            'epsilon':eps,
            'min_samples':min_samp,
            'vrc':vrc,
            'ss':ss,
            'db':db,
            'di':di,
            'ari':ari,
            'nmi':nmi}


def dbscan_optimization(data,true_labels,eps_choices,ms_choices):
    """
    Performs brute force grid search optimization for each of our
    considered metrics.  It returns a dictionary where keys are
    the metrics (vrc, nmi, ari, ...), and each entry is 
    the return for the optimal result of `dbscan_trial` for that metric.

    :param data: data to perform optimization on
    :param true_labels: true labels for the data
    :param eps_choices: list of epsilon choices for grid search
    :param ms_choices: list of minimum sample choices for grid search
    :return: dictionary in form {'vrc','ss','db','di','ari','nmi'}
    """
    def isBetter(x,y,m):
        if not y[m]:
            return True
        if m == 'db': # special case for davies bouldin
            return x[m]<y[m][m]
        else:
            return x[m]>y[m][m]
    
    optimal_results = {'vrc':False,
                       'ss':False,
                       'db':False,
                       'di':False,
                       'ari':False,
                       'nmi':False}
    #pairwise = pairwise_distances(data)
    pairwise = None
    for eps,ms in itertools.product(eps_choices,ms_choices):
        print((eps,ms))
        outcome = dbscan_trial(data,pairwise,true_labels,eps,ms)
        if outcome['clusters'] < 2:
            continue
        for metric in optimal_results.keys():
            if isBetter(outcome,optimal_results,metric):
                optimal_results[metric] = outcome 
    return optimal_results 

def print_optimal_dbscans(ds,m,f,d,header=False):
    """
    Print out the results of `optimize_dbscan`

    :param ds: name of dataset
    :param m: name of method
    :param f: name of pickle file
    :param d: results dictionary
    """
    if not d['vrc']:
        return
    if header:
        print('dataset,method,file,opt_res,'+','.join(d['vrc'].keys()))
     
    for key in d.keys():
        if not d[key]:
            continue
        print(','.join([ds,m,f,key]+[str(d[key][x]) for x in d[key].keys()]))
