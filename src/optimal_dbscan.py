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
from svr2019.metrics import davies_bouldin_score
from svr2019.metrics import dunn_index

def warn(*args, **kwargs):
    """
    hack to stop sklearn from throwing annoying warnings
    """
    pass

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
        # TODO: add Davies Bouldin and Dunn Index
        vrc = calinski_harabaz_score(data,labels)
        #ss = silhouette_score(pairwise,labels,metric='precomputed')
        ss = silhouette_score(data,labels)
        db = davies_bouldin_score(data,labels)
        di = dunn_index(data,labels,metric)
        ari = adjusted_rand_score(true_labels,labels)
        nmi = normalized_mutual_info_score(true_labels,labels)
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
        if m == 'di': # special case for dunn index
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
