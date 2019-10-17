#!/usr/bin/env python3
#################################################
# generate_embedding.py
#
# Create a low dimensional embedding of a dataset
# with a specific DR method
#################################################
from sc_dr.datasets import *

import pickle
import sys
import os

from sklearn.manifold import TSNE, Isomap, LocallyLinearEmbedding,\
                             SpectralEmbedding, MDS
from sklearn.decomposition import PCA, FactorAnalysis, FastICA,\
                                  LatentDirichletAllocation, NMF
from sklearn.preprocessing import scale

import time

import pandas as pd

try:
    import umap
    UMAP_AVAILABLE=True
except ImportError:
    UMAP_AVAILABLE=False
    
from MulticoreTSNE import MulticoreTSNE as MCTSNE

try:
    import scscope
    SCSCOPE_AVAILABLE=True
except ImportError:
    SCSCOPE_AVAILABLE=False

try:
    from ZIFA import block_ZIFA
    ZIFA_AVAILABLE=True
except ImportError:
    ZIFA_AVAILABLE=False

try:
    from phate import PHATE
    PHATE_AVAILABLE=True
except ImportError:
    PHATE_AVAILABLE=False

import argparse

class ZIFA_Wrapper():

    def __init__(self,k):
        self.k = k

    def fit_transform(self,data):
        embedding, model = block_ZIFA.fitModel(data,self.k)
        self.model = model
        return embedding

class ScaledPCA():

    def __init__(self,k):
        self.k = k

    def fit_transform(self,data):
        model = PCA(n_components=args.dims)
        self.model = model
        embedding = self.model.fit_transform(scale(data))
        return embedding

class ScScope():
    """
    Wrapper class for the scscope package
    """

    def __init__(self,k):
        self.k = k

    def fit_transform(self,data):
        self.model = scscope.train(
                        data,
                        self.k,
                        use_mask=True,
                        batch_size=128,
                        max_epoch=500,
                        epoch_per_check=10,
                        T=2,
                        exp_batch_idx_input=[],
                        encoder_layers=[1000,500,200,500],
                        decoder_layers=[200,500,1000],
                        learning_rate=0.001,
                        beta1=0.5,
                        num_gpus=1)

        embedding,_,_ = scscope.predict(data,self.model,batch_effect=[])
        return embedding

def get_embedding(model,data,to_scale=False):
    """
    Wrapper function around the `fit_transform` function
    
    :param model: the model object to be used for dimension reduciton
    :param data: the data which the model should be fit to
    :return: The data is returned as a matrix of 32 bit floats
    """
    print('Generating Embedding ...')
    if to_scale:
        embedding = model.fit_transform(scale(data))
    else:
        embedding = model.fit_transform(data)

    return embedding.astype(np.float32)

def get_parser():
    """
    Build `ArgumentParser` for commandline argument interpretation

    :return: `ArgumentParser` object
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--method",
        choices = ["umap","pca","pca-scaled","tsne",
                   "mctsne", "isomap", "lle",
                   "nmf","lda","zifa",
                   "spectral", "mds","phate",
                   "fa","fica","scscope","rpca"],
        default = 'pca',
        help="method for dimension reduction"
    )

    """
    choices = ["mouse","koh","kumar",
              "simk4easy","simk4hard","simk8hard",
              "zhengmix4eq","zhengmix8eq","chen",
              "baron-human","campbell","macosko",
              "marques","shekhar"],
    """
    # Originally we only allowed specific datasets.  Now that a new 
    # structure is being assumed
    parser.add_argument(
        "--dataset",
        required=True,
        help="dataset to be used -- Should be stored in data/datasets/pddf/.  Do not include the .pkl extension"
    )

    parser.add_argument(
        "--outdir",        
        required=True,
        help='path to desired output directory.  Will create if it does not exist'
    )

    parser.add_argument(
        "--trial-name",
        required=True,
        help='Used to name the resulting embedding'
    )

    parser.add_argument(
        "--dims",
        type=int,
        default=2,
        help="number of dimensions to reduce to"
    )

    """
    parser.add_argument(
        "--npoints",
        type=int,
        default=250000,
        help="number of points to load from mouse dataset ("
    )
    """

    parser.add_argument(
        "--njobs",
        type=int,
        default=1,
        help="number of jobs to run if applicable to DR algorithm"
    )

    """
    parser.add_argument(
        "--log1p",
        action='store_true',
        help="whether to apply log(1+x) transform"
    )

    parser.add_argument(
        "--log",
        action='store_true',
        help="whether to apply log transform"
    )
    """

    parser.add_argument(
        "--scale",
        action='store_true',
        help="whether to scale data (does not center)"
    )

    return parser

def get_model(args):
    """
    Get the base model class for the dimension reduction
    requested in the arguments

    :param args: output of ArgumentParser().parse_args()
    :return: model to be used for dimension reduction
    """
    if args.method == 'umap' and UMAP_AVAILABLE:
        model = umap.UMAP(n_components=args.dims)
    elif args.method == 'pca':
        model = PCA(n_components=args.dims)
    elif args.method == 'pca-scaled':
        model = ScaledPCA(args.dims)
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
    elif args.method == 'zifa' and ZIFA_AVAILABLE:
        model = ZIFA_Wrapper(args.dims)
    elif args.method == 'lda':
        model = LatentDirichletAllocation(args.dims)
    elif args.method == 'nmf':
        model = NMF(args.dims)
    elif args.method == 'scscope' and SCSCOPE_AVAILABLE:
        model = ScScope(args.dims)
    elif args.method == 'phate' and PHATE_AVAILABLE:
        model = PHATE(args.dims)
    else:
        print("ERROR: Invalid embedding option", file=sys.stderr)
        exit()
    return model

def write_results(embedded,labels,args):
    """
    Write the embedding and model to a pickled file

    :param embedded: the low dimensional embedding of the data
    :param args: the output of `ArgumentParser.parse_args` from `get_parser`
    """
    # make our directories if we have to
    embed_dir = args.outdir
    if not os.path.exists(embed_dir):
        os.makedirs(embed_dir)

    print('saving embedding')
    filename  = args.trial_name + '.pkl'

    """
    with open(os.path.join(embed_dir,filename),'wb') as fh:
        pickle.dump(embedded,fh,protocol=4)
    """

    pd_df = pd.DataFrame(embedded)
    pd_df.insert(0,'cell_type',labels)
    pd_df.to_pickle(os.path.join(embed_dir,filename))

def get_data(args):
    """
    Get the dataset requested by the commandline arguments

    :param args: the result of `parse_args` from the `ArgumentParser` returned by `get_parser`
    """
    data = FromPickledPanda('data/datasets/pddf/'+args.dataset+'.pkl')
    if args.scale:
        # Shrink data to be between 0 and 1
        data.data /= np.max(data.data)
    return data

if __name__ == '__main__':

    print('Running ...')

    parser = get_parser()
    args = parser.parse_args()
    data = get_data(args)
    model = get_model(args)
    start = time.time()
    embedded = get_embedding(model,data.data,to_scale=args.scale)
    end = time.time()
    print("Completed empedding in {} seconds".format(end-start))
    write_results(embedded,data.labels,args)
