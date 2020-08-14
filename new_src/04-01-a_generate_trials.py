import sys
import pickle

import pandas as pd
import numpy as np
import scipy

from scipy.stats import truncexpon as texp
from sklearn.neighbors import NearestNeighbors as NN

MAX_MINPTS_PROP = 0.15
N_TRIALS=2000
#N_TRIALS=1000

EXCLUDED_TYPES = ["alpha.contaminated", "beta.contaminated", "delta.contaminated", "Excluded", "gamma.contaminated", "miss", "NA", "not applicable", "unclassified", "unknown", "Unknown", "zothers"]

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: {} [path_to_embedding] [maxEps] [metric]".format(sys.argv[0]),file=sys.stderr)
        exit()
    elif sys.argv[3] not in ['euclidean','seuclidean','correlation','cosine']:
        print("Error: metric must be one of ['euclidean','seuclidean','correlation','cosine']",file=sys.stderr)
        exit()

    # Load in our data
    with open(sys.argv[1],'rb') as fh:
        x = pickle.load(fh)
        cell_types = x.cell_type
        to_remove = []
        for i in range(len(cell_types)):
            if cell_types[i] in EXCLUDED_TYPES:
                to_remove.append(i)
        x.drop(index=to_remove,inplace=True)
        X = x.drop('cell_type',axis=1).values
        if scipy.sparse.issparse(X[0][0]):
            X = np.array(np.concatenate([i[0].todense() for i in X]))


    # And grab our metric should be one of 'euclidean', 'seuclidean', 'correlation', or 'cosine'
    metric = sys.argv[3]

    # Get our Eps and minPts bounds
    maxEps = float(sys.argv[2])
    maxMinPts = int(np.floor(X.shape[0]*MAX_MINPTS_PROP))

    if metric == 'seuclidean':
        knn,_ = NN(maxMinPts+1, metric=metric, metric_params={
            'V':np.var(X,axis=0,ddof=1,dtype=np.double)
            }).fit(X).kneighbors(X)
    else:
        knn,_ = NN(maxMinPts+1, metric=metric).fit(X).kneighbors(X)

    minEpsArry = np.array([knn[:,(i+1)].min() for i in range(0,maxMinPts)])
#    print(minEpsArry)

    # Generate our Random Numbers
    base=10
    runif = np.random.uniform(np.log(5)/np.log(base),np.log(maxMinPts)/np.log(base),size=N_TRIALS)
    minPtsSamples = np.floor(np.power(base,runif)).astype(np.int32)
    a=5
    rtexp = texp(a,0).ppf(np.random.uniform(size=N_TRIALS))/a
    minEpsSamples = minEpsArry[minPtsSamples]
    epsSamples = rtexp*(maxEps-minEpsSamples) + minEpsSamples
    for i in range(N_TRIALS):
        print('{},{},{}'.format(metric,str(minPtsSamples[i]),str(epsSamples[i])))
