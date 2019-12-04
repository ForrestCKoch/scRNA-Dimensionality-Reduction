from sklearn.neighbors import NearestNeighbors as NN
from sklearn.metrics import pairwise_distances
from heapq import heappush, heappop
import numpy as np

def get_connecting_eps(X,metric='euclidean'):
    """
    Return the maximum jump requried for BFS to visit all nodes.
    """
    pwise_dist = pairwise_distances(X,metric=metric)

    """
    # Initialize the heap
    sidx = 0
    h = []
    heappush(h,(0,sidx))

    # Keep track of unvisited indices and max eps
    todo = set(range(0,X.shape[0]))
    max_eps = 0

    while(len(todo)):
        eps, idx = heappop(h) 
        #print(idx)
        if idx in todo: # otherwise we have already visited
            todo.remove(idx)
            max_eps = max(max_eps,eps)
            for nidx in todo:
                heappush(h,(pwise_dist[idx,nidx],nidx)) 
    """
    #todo = set(range(1,X.shape[0]))
    max_eps = 0
    ddict = {i:pwise_dist[0,i] for i in range(1,len(X))}
    while(len(ddict)):
        mkey = min(ddict,key=ddict.get)
        max_eps = max(ddict.pop(mkey),max_eps)
            
        #todo.remove(mkey)
        for i in ddict:
            ddict[i] = min(ddict[i],pwise_dist[mkey,i])
         
    return max_eps 

def get_minimum_eps(X,metric='euclidean'):
    """
    Return the maximum value that should be used for minimum samples -- floor(0.15*len(X))
    Return the minimum value such that at least 1 point has K neighbors for K = 1 .. floor(0.15*len(X)) 
    """
    minPts = int(np.floor(0.15*len(X)))
    nn = NN(minPts+1)
    nn.fit(X)
    knn,idx = nn.kneighbors(X) 
    minEps = [knn[:,i].min() for i in range(1,minPts+1)]
    return (minPts,minEps)
    
if __name__ == '__main__':
    import pickle
    import sys
    #x = np.concatenate([np.random.normal(0,.1,size=(100,2)),np.random.normal(1,.1,size=(100,2))])
    x = pickle.load(open(sys.argv[1],'rb')).drop('cell_type',axis=1).values
    e1 = get_connecting_eps(x)
    e2 = get_connecting_eps(x,'correlation')
    e3 = get_connecting_eps(x,'cosine')
    minPts,minEps = get_minimum_eps(x)
    #print('{},{},{},{}'.format(sys.argv[1],str(e),str(minPts),str(minEps)))
    print('{},{},{},{}'.format(sys.argv[1],str(e1),str(e2),str(e3)))
