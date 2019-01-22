#!/usr/bin/python3

import sklearn.metrics as metrics
import numpy as np
from scipy.spatial.distance import pdist, euclidean
from sklearn.utils import safe_indexing

import sklearn.metrics as metrics

def davies_bouldin_score(X, labels):
    """
    Taken from:
    https://github.com/scikit-learn/scikit-learn/pull/12760
    to avoid errors
    """
    n_samples, _ = X.shape
    n_labels =max(labels)+1

    intra_dists = np.zeros(n_labels)
    centroids = np.zeros((n_labels, len(X[0])), dtype=np.float)
    for k in range(n_labels):
        cluster_k = safe_indexing(X, labels == k)
        centroid = cluster_k.mean(axis=0)
        centroids[k] = centroid
        intra_dists[k] = np.average(metrics.pairwise_distances(
            cluster_k, [centroid]))

    centroid_distances = metrics.pairwise_distances(centroids)

    if np.allclose(intra_dists, 0) or np.allclose(centroid_distances, 0):
        return 0.0

    centroid_distances[centroid_distances == 0] = np.inf
    combined_intra_dists = intra_dists[:, None] + intra_dists
    scores = np.amax(combined_intra_dists / centroid_distances, axis=1)

    return np.mean(scores)

def dunn_index(X, labels, metric = 'euclidean'):
    """
    Calculate the Dunn Index for the provided clustering

    :param points: a numpy array of data points
    :param labels: a numpy array of labels for each point
    :param metric: metric to be used for distance measures
        valid values are from scipy.spatial.distance
    """

    # TODO: implement I am currently concerned about
    #       runtime for larger datasets, so I am
    #       leaving this until later ...    
    n_labels = max(labels)+1

    intra_dists = np.zeros(n_labels)
    centroids = np.zeros((n_labels, len(X[0])), dtype=np.float)
    for k in range(n_labels):
        cluster_k = safe_indexing(X, labels == k)
        centroid = cluster_k.mean(axis=0)
        centroids[k] = centroid
        intra_dists[k] = np.average(metrics.pairwise_distances(
            cluster_k, [centroid]))

    centroid_distances = metrics.pairwise_distances(centroids)
    for i in range(0,len(centroid_distances)):
        centroid_distances[i][i] = np.inf
    
    return min([min(x) for x in centroid_distances])/max(intra_dists)
    #return min([min(x) for x in centroid_distances]),max(intra_dists)


if __name__ == '__main__':
    pass
