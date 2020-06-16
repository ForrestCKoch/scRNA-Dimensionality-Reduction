import pickle
import sys
from signal import signal, SIGTERM, SIGINT

from time import time
import os

import numpy as np
import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans

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

def run_trial(X, labels, k):
    errors = '"'

    # Run our dbscan
    start = time()
    """
    if metric == 'seuclidean':
        db = KMeans(eps,minPts,metric=metric,metric_params={'V':V})
    else:
        db = kmean(,minPts,metric=metric)
    """
    db = KMeans(k,n_jobs=12)
    pred_labels = db.fit_predict(X)
    elapsed = time() - start

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
        ss_score = ss(X, pred_labels)
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

    errors += '"'

    return [k, elapsed,
            ari_score, nmi_score,
            ss_score, vrc_score,
            dbs_score, errors]


if __name__ == '__main__':
    if (len(sys.argv) != 2):
        print("Usage: {} [data-file]".format(sys.argv[0]))

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

    labels = LabelEncoder().fit_transform(x.cell_type)

    folder = 'data/results/kmeans/'+'/'.join(sys.argv[1].split('/')[0:-1])
    try:
        os.makedirs(folder)
    except:
        pass
    outfile = 'data/results/kmeans/'+sys.argv[1].split('.')[0] + '.csv'
    with open(outfile,'w') as fh:
        for k in range(3,56):
            # Calculate DBSCAN result and write
            km_result = run_trial(X, labels, k)
            print(','.join([str(x) for x in km_result]),file=fh)
