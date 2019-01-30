from svr2019.datasets import *

import pickle
import sys
import os

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

from sklearn.manifold import TSNE, Isomap, LocallyLinearEmbedding,\
                             SpectralEmbedding, MDS
from sklearn.decomposition import PCA, FactorAnalysis, FastICA

import umap
from MulticoreTSNE import MulticoreTSNE as MCTSNE

import argparse

def get_embedding(model,data):
    print('Generating Embedding ...')
    embedding = model.fit_transform(data)
    return embedding.astype(np.float32)

def str2bool(value):
    return value.lower() == 'true'

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--method",
        choices = ["umap","pca","tsne",
                   "mctsne", "isomap", "lle",
                   "rpca",
                   "spectral", "mds",
                   "fa","fica"],
        default = 'pca',
        help="method for dimension reduction"
    )

    parser.add_argument(
        "--dataset",
        choices = ["mouse","koh","kumar",
                  "simk4easy","simk4hard","simk8hard",
                  "zhengmix4eq","zhengmix8eq"],
        default = 'koh',
        help="dataset to be used"
    )

    parser.add_argument(
        "--dims",
        type=int,
        default=50,
        help="number of dimensions to reduce to"
    )

    parser.add_argument(
        "--npoints",
        type=int,
        default=250000,
        help="number of points to load from mouse dataset"
    )

    parser.add_argument(
        "--njobs",
        type=int,
        default=1,
        help="number of jobs to run"
    )

    parser.add_argument(
        "--log1p",
        type=str2bool,
        default=False,
        help="whether to apply log(1+x) transform"
    )

    parser.add_argument(
        "--log-trans",
        type=str2bool,
        default=False,
        help="whether to apply log transform"
    )
    
    return parser

def get_model(args):
    if args.method == 'umap':
        model = umap.UMAP(n_components=args.dims)
    elif args.method == 'pca':
        model = PCA(n_components=args.dims)
    elif args.method == 'rpca':
        model = RandomizedPCA(n_components=args.dims)
    elif args.method == 'tsne':
        model = TSNE(n_components=args.dims)
    elif args.method == 'mctsne':
        model = MCTSNE(n_components=args.dims,n_jobs=args.njobs)
    elif args.method == 'spectral':
        model = SpectralEmbedding(n_components=args.dims,n_jobs=args.njobs)
    elif args.method == 'lle':
        model = LocallyLinearEmbedding(n_components=args.dims,n_jobs=args.njobs)
    elif args.method == 'isomap':
        model = Isomap(n_components=args.dims,n_jobs=args.njobs)
    elif args.method == 'mds':
        model = MDS(n_components=args.dims,n_jobs=args.njobs)
    elif args.method == 'fa':
        model = FactorAnalysis(n_components=args.dims)
    elif args.method == 'fica':
        model = FastICA(n_components=args.dims)
    else:
        print("ERROR: Invalid embedding option", file=sys.stderr)
        exit()
    return model

def write_results(model,embedded,args):
    # make our directories if we have to
    embed_dir = os.path.join('data','embeddings',args.dataset,args.method)
    model_dir = os.path.join('data','model',args.dataset,args.method)
    if not os.path.exists(embed_dir):
        os.makedirs(embed_dir)
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    print('saving embedding')
    log_flag = str(args.log1p or args.log_trans)
    filename  = str(args.dims)+'-log-'+log_flag+'.pickle'

    with open(os.path.join(embed_dir,filename),'wb') as fh:
        pickle.dump(embedded,fh,protocol=4)

    with open(os.path.join(model_dir,filename),'wb') as fh:
        pickle.dump(model,fh,protocol=4)

def get_data(args):
    if args.npoints == -1:
        selection = None
    else:   
        selection = list(range(0,args.npoints))

    # early exit ...

    if args.method == 'tsne' and args.dims > 4:
        exit()
    elif args.method == 'mctsne' and args.dims > 10:
        exit()

    if args.dataset == 'mouse':
        ds_path = 'data/datasets/GSE93421_brain_aggregate_matrix.hdf5'
        data = E18MouseData(ds_path,
                          nproc=args.njobs,
                          selection=selection,
                          log1p=args.log1p).data
    else:
        ds_path = 'data/datasets/'+args.dataset+'.csv'
        data = DuoBenchmark(ds_path,log_trans=args.log_trans,log1p=args.log1p).data
    return data

if __name__ == '__main__':

    parser = get_parser()
    args = parser.parse_args()
    data = get_data(args)
    model = get_model(args)
    embedded = get_embedding(model,data)
    write_results(model,embedded,args)
