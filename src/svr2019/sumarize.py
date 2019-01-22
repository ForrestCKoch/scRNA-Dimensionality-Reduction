#!/usr/bin/python3

import sklearn.metrics as metrics
import numpy as np
from scipy.spatial.distance import pdist, euclidean
from sklearn.utils import safe_indexing

def internal_summary(points, labels):
    """
    Generate a summary of internal validation measures.
    Returns a dictionary containing elements:
        - 'calinski-harabaz'
        - 'davies-bouldin'
        - 'dunn-index'
        - 'silhouette-score'
    
    :param points: a numpy array of data points
    :param labels: a numpy array of labels for each point
    """
    calinski_harabaz = metrics.calinski_harabaz_score(points, labels)
    davies_bouldin = davies_bouldin_score(points, labels)
    di = dunn_index(points, labels)
    silhouette_score = metrics.silhouette_score(points, labels)

    return {
            'calinski-harabaz':calinski_harabaz,
            'davies-bouldin':davies_bouldin,
#            'dunn-index':dunn_index,
            'silhouette-score':silhouette_score,
           }


def print_summaries(path_list,labels):
    for path in path_list:
        with open(path,'rb') as fh:
            embedding = np.load(fh).astype(np.float32)
        summary_dict = internal_summary(embedding, labels)
        summary_list = [path]+[summary_dict[x] for x in sorted(summary_dict.keys())]
        print(','.join(summary_list))
        

if __name__ == '__main__':
    pass
