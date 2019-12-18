import pickle
import sys
from signal import signal, SIGTERM, SIGINT

from time import time

import numpy as np
import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import DBSCAN

from sklearn.metrics import adjusted_rand_score as ari
from sklearn.metrics import normalized_mutual_info_score as nmi
from sklearn.metrics import silhouette_score as ss
from sklearn.metrics import calinski_harabasz_score as vrc
from sklearn.metrics import davies_bouldin_score as dbs

EXCLUDED_TYPES = ["alpha.contaminated", "beta.contaminated", "delta.contaminated", "Excluded", "gamma.contaminated", "miss", "NA", "not applicable", "unclassified", "unknown", "Unknown", "zothers"]

"""
def _sig_handle(*kwargs):
    global q
    global queue_file
    write_queue(queue_file,q)
    exit()
"""

def load_queue(filename):
    with open(filename,'r') as fh:
        q = [line.rstrip('\n').split(',') for line in fh]
    return q

def write_queue(filename,q):
    lines = [','.join(line) for line in q]
    text = '\n'.join(lines)
    with open(filename,'w') as fh:
        #for line in q:
        #    print(','.join(line),file=fh)
        fh.write(text)


def run_trial(X, labels, eps, minPts, metric):
    errors = '"'
    
    # In case of metric == 'seuclidean', need to precompute variance
    if metric == 'seuclidean':
        V = np.var(X,axis=0,ddof=1,dtype=np.double)
    else:
        V = None

    # Run our dbscan
    start = time()
    if metric == 'seuclidean':
        db = DBSCAN(eps,minPts,metric=metric,metric_params={'V':V})
    else:
        db = DBSCAN(eps,minPts,metric=metric)
    pred_labels = db.fit_predict(X)
    elapsed = time() - start
    perc_noise = np.sum(pred_labels==-1)/len(pred_labels)
    n_clust = pred_labels.max()

    # Remove noisy points 
    clean_idx = np.where(pred_labels != -1)
    nn_preds = pred_labels[clean_idx]
    nn_labels = labels[clean_idx]
    nn_X = X[clean_idx]

    try:
        ari_score = ari(pred_labels, labels)
    except Exception as e:
        errors += str(e) + '; '
        ari_score = np.nan
    try:
        nmi_score = nmi(pred_labels, labels, average_method='arithmetic')
    except Exception as e:
        errors += str(e) + '; '
        nmi_score = np.nan
    try:
        if metric == 'seuclidean':
            ss_score = ss(X, pred_labels, metric=metric, V=V)
        else:
            ss_score = ss(X, pred_labels, metric=metric)
    except Exception as e:
        errors += str(e) + '; '
        ss_score = np.nan
    try:
        vrc_score = vrc(X, pred_labels)
    except Exception as e:
        errors += str(e) + '; '
        vrc_score = np.nan
    try:
        dbs_score = dbs(X,pred_labels)
    except Exception as e:
        errors += str(e) + '; '
        dbs_score = np.nan

    try:
        nn_ari_score = ari(nn_preds, nn_labels)
    except Exception as e:
        errors += str(e) + '; '
        nn_ari_score = np.nan
    try:
        nn_nmi_score = nmi(nn_preds, nn_labels, average_method='arithmetic')
    except Exception as e:
        errors += str(e) + '; '
        nn_nmi_score = np.nan
    try:
        if metric == 'seuclidean':
            nn_ss_score = ss(nn_X, nn_preds, metric=metric, V=V)
        else:
            nn_ss_score = ss(nn_X, nn_preds, metric=metric)
    except Exception as e:
        errors += str(e) + '; '
        nn_ss_score = np.nan
    try:
        nn_vrc_score = vrc(nn_X, nn_preds)
    except Exception as e:
        errors += str(e) + '; '
        nn_vrc_score = np.nan
    try:
        nn_dbs_score = dbs(nn_X,nn_preds)
    except Exception as e:
        errors += str(e) + '; '
        nn_dbs_score = np.nan

    errors += '"'

    return [metric, eps, minPts, n_clust, perc_noise, elapsed,
            ari_score, nn_ari_score, nmi_score, nn_nmi_score,
            ss_score, nn_ss_score, vrc_score, nn_vrc_score,
            dbs_score, nn_dbs_score, errors]


if __name__ == '__main__':
    if (len(sys.argv) != 3):
        print("Usage: {} [data-file] [queue-file]".format(sys.argv[0]))

    # If we just re-write our queue after every iteration,
    # Then we don't need to bother with catching interrupts
    #signal(SIGINT,_sig_handle)
    #signal(SIGTERM,_sig_handle)

    #global q
    #global queue_file
    queue_file = sys.argv[2]
    q = load_queue(queue_file)

    with open(sys.argv[1],'rb') as fh:    
        #print('x')
        x = pickle.load(fh)    
        cell_types = x.cell_type              
        to_remove = []                                  
        for i in range(len(cell_types)):    
            if cell_types[i] in EXCLUDED_TYPES:    
                to_remove.append(i)    
        x.drop(index=to_remove,inplace=True)    
        X = x.drop('cell_type',axis=1).values

    q = load_queue(sys.argv[2])    
    labels = LabelEncoder().fit_transform(x.cell_type)

    t1 = time()
    while len(q):
        #print('x')
        trial = q[-1]
        metric = trial[0]
        minPts = int(trial[1])
        eps = np.float(trial[2])
        db_result = run_trial(X, labels, eps, minPts, metric)
        print(','.join([str(x) for x in db_result]))
        q.pop()
        write_queue(queue_file,q) # just rewrite the file after each iteration ...
        #t2 = time()
        #print(t2-t1)
        #t1=t2

    # if we finish, write an empty file
    write_queue(queue_file,q)
