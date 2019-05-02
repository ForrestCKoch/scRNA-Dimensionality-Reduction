#!/usr/bin/python3

from sklearn.metrics import calinski_harabaz_score, silhouette_score
import numpy as np

from svr2019.metrics import davies_bouldin_score, dunn_index
from svr2019.datasets import *

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

    labels = np.array(labels)

    calinski_harabaz = calinski_harabaz_score(points, labels)
    #davies_bouldin = davies_bouldin_score(points, labels)
    davies_bouldin = -1
    #di = dunn_index(points, labels)
    di = -1
    silhouette = silhouette_score(points, labels)

    return {
            'calinski-harabaz':calinski_harabaz,
            'davies-bouldin':davies_bouldin,
            'dunn-index':di,
            'silhouette-score':silhouette,
           }


def print_summaries(path_list):
    head = True
    for path,dataset,labels,exclude in path_list:
        #labels = DuoBenchmark('data/datasets/'+dataset+'.csv').tags 
        with open(path,'rb') as fh:
            embedding = np.load(fh).astype(np.float32)

        embedding = np.delete(embedding,exclude,axis=0)
        labels = np.delete(labels,exclude,axis=0)

        try:
            summary_dict = internal_summary(embedding, labels)
            summary_list = [path]+[str(summary_dict[x]) for x in sorted(summary_dict.keys())]
            if head:
                print(','.join(['path']+sorted(summary_dict.keys())))
                head = False
            print(','.join(summary_list))
        except ValueError:
            pass
            
        

if __name__ == '__main__':
    pass
