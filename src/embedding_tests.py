from svr2019.datasets import *

import pickle
import sys

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import umap

import argparse

NPROCS=10

def get_embedding(embed_func,ds):
    print('Generating Embedding ...')
    embedding = embed_func(ds.data)
    return embedding

def umap_to_tsne(x):
    semi_embedded = umap.UMAP(n_components=50).fit_transform(x)
    embedded = TNSE(n_components=2,n_jobs=NPROCS).fit_transform(semi_embedded)
    return embedded

def pca_to_tsne(x):
    semi_embedded = PCA(n_components=50).fit_transform(x)
    embedded = TNSE(n_components=2,n_jobs=NPROCS).fit_transform(semi_embedded)
    return embedded

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--method",
        choice = ["umap","pca","tsne"],
        default = 'pca'
    )

    parser.add_argument(
        "--dataset",
        choice = ["mouse","koh","kumar",
                  "simk4easy","simk4hard","simk8hard",
                  "zhengmix4eq","zhengmix8eq"],
        default = 'koh' 
    )

    parser.add_argument(
        "--dims",
        type=int,
        default=50
    )

    parser.parse_args()

    
    if dataset = 'mouse':
        ds = E18MouseData('GSE93421_brain_aggregate_matrix.hdf5',
                          nproc=NPROCS,
                          selection=list(range(0,npoints)))
    else:
        ds_path = 'data/datasets/'+dataset+'.csv'
        ds = DuoBenchmark(ds_path,log1p=True) 

    if method == 'umap':
        embed_func = umap.UMAP(n_components=dims).fit_transform
    elif method == 'pca':
        embed_func = PCA(n_components=dims).fit_transform
    elif method == 'tsne':
        embed_func = TSNE(n_components=dims).fit_transform
    elif method == 'umap-mctsne':
        embed_func = umap_to_tsne
    elif method == 'pca-mctsne':
        embed_func = pca_to_tsne
    else:
        print("ERROR: Invalid embedding option", file=sys.stderr)
        exit()

    embedded = get_embedding(embed_func,ds)

    #print('saving image')
    #plt.scatter(embedded[:,0],embedded[:,1])
    #plt.savefig('data/plots/'+method+'-250k.pdf')

    print('saving embedding')
    with open('data/embeddings/'+dataset+'-'+method+'-'+dims+'.pickle','wb') as fh:
        pickle.dump(embedded,fh,protocol=4)

