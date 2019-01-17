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

def get_embedding(embed_obj,data):
    print('Generating Embedding ...')
    embedding = embed_obj.fit_transform(data)
    return embedding

def str2bool(value):
    return value.lower() == 'true'

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--method",
        choices = ["umap","pca","tsne"],
        default = 'pca'
    )

    parser.add_argument(
        "--dataset",
        choices = ["mouse","koh","kumar",
                  "simk4easy","simk4hard","simk8hard",
                  "zhengmix4eq","zhengmix8eq"],
        default = 'koh' 
    )

    parser.add_argument(
        "--dims",
        type=int,
        default=50
    )

    parser.add_argument(
        "--processes",
        type=int,
        default=10
    )

    parser.add_argument(
        "--npoints",
        type=int,
        default=250000
    )

    parser.add_argument(
        "--log1p",
        type=str2bool,
        default=False
    )

    args = parser.parse_args()

    
    if args.dataset == 'mouse':
        ds_path = 'data/datasets/GSE93421_brain_aggregate_matrix.hdf5'
        data = E18MouseData(ds_path,
                          nproc=args.processes,
                          selection=list(range(0,args.npoints)),
                          log1p=args.log1p).data
    else:
        ds_path = 'data/datasets/'+args.dataset+'.csv'
        data = DuoBenchmark(ds_path,log1p=args.log1p).data

    if args.method == 'umap':
        embed_obj = umap.UMAP(n_components=args.dims)
    elif args.method == 'pca':
        embed_obj = PCA(n_components=args.dims)
    elif agrs.method == 'tsne':
        embed_obj = TSNE(n_components=args.dims)
    else:
        print("ERROR: Invalid embedding option", file=sys.stderr)
        exit()

    embedded = get_embedding(embed_obj,data)

    #print('saving image')
    #plt.scatter(embedded[:,0],embedded[:,1])
    #plt.savefig('data/plots/'+method+'-250k.pdf')

    print('saving embedding')
    emb_file='data/embeddings/'+args.dataset+'-'+args.method+'-'+str(args.dims)+'-log1p-'+str(args.log1p)+'.pickle'
    obj_file='data/embeddings/'+args.dataset+'-'+args.method+'-'+str(args.dims)+'-log1p-'+str(args.log1p)+'-object.pickle'

    with open(emb_file,'wb') as fh:
        pickle.dump(embedded,fh,protocol=4)

    with open(obj_file,'wb') as fh:
        pickle.dump(embed_obj,fh,protocol=4)

