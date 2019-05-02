import pickle
import os

import numpy as np

import matplotlib.pyplot as plt

from sklearn.cluster import DBSCAN
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from umap import UMAP

from svr2019.sumarize import *


table_dict,methods = get_table_dict('results/csvs/internal_metrics_reduced.csv')

ss_res = get_rankings(table_dict,'ss',methods)

n_meth = len(methods)
n_data = len(ss_res.keys())

for dataset in ss_res.keys():
    print(dataset)
    #ds = DuoBenchmark('data/datasets/'+dataset+'.csv',split_head=False)
    #raw_data = ds.data
    first_col=True
    colour = 1
    for i,entry in enumerate(sorted(ss_res[dataset],key = lambda x:x[2])):
        method = entry[2]
        dims = entry[1]
        print('\t'+method)
        if method == 'full':
            continue
        if method == 'sdae':
            emb_file = 'data/embeddings/'+dataset+'/'+method+'/'+dims+'-log-True.pickle'
        else:
            emb_file = 'data/embeddings/'+dataset+'/'+method+'/'+dims+'-log-False.pickle'
        with open(emb_file,'rb') as fh:
            emb_data = pickle.load(fh)

        #plt.subplot(n_data,n_meth+1,count)
        
        if int(dims) > 2:
            for name,func in [ ('umap',UMAP),('tsne',TSNE),('pca',PCA) ]:
                two_dim = func(n_components=2).fit_transform(emb_data)
                plt.scatter(x=two_dim[:,0],y=two_dim[:,1],s=0.5)
                plt.savefig('test_plots/'+dataset+'/'+method+'-'+name+'.png')
                plt.clf()
        else:
            plt.scatter(x=emb_data[:,0],y=emb_data[:,1],s=0.5)
            plt.savefig('test_plots/'+dataset+'/'+method+'.png')
            plt.clf()
