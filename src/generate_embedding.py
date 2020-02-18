#!/usr/bin/env python3
#################################################
# generate_embedding.py
#
# Create a low dimensional embedding of a dataset
# with a specific DR method
# usage: generate_embedding.py [-h]
#                              [--method {snmf,nmf,scscope,fica,ipca,bd,kpca-cos,pca,vasc,zifa,saucie,lda,kpca-pol,kpca-rbf,spca,mctsne,pmf,spectral,spca-batch,umap,phate,tsne,psmf,lle,lfnmf,srp,fa,tga,icm,sepnmf,nsnmf,grp,kpca-sig,lsnmf,tsvd,nmf2,ivis,isomap,mds,vpac}]
#                              --dataset DATASET --outdir OUTDIR --trial-name
#                              TRIAL_NAME [--dims DIMS] [--njobs NJOBS]
#                              [--scale]
# 
# optional arguments:
#   -h, --help            show this help message and exit
#   --method {snmf,nmf,scscope,fica,ipca,bd,kpca-cos,pca,vasc,zifa,saucie,lda,kpca-pol,kpca-rbf,spca,mctsne,pmf,spectral,spca-batch,umap,phate,tsne,psmf,lle,lfnmf,srp,fa,tga,icm,sepnmf,nsnmf,grp,kpca-sig,lsnmf,tsvd,nmf2,ivis,isomap,mds,vpac}
#                         method for dimension reduction
#   --dataset DATASET     dataset to be used -- Should be stored in
#                         data/datasets/pddf/. Do not include the .pkl extension
#   --outdir OUTDIR       path to desired output directory. Will create if it
#                         does not exist
#   --trial-name TRIAL_NAME
#                         Used to name the resulting embedding
#   --dims DIMS           number of dimensions to reduce to
#   --njobs NJOBS         number of jobs to run if applicable to DR algorithm
#   --scale               whether to scale data (does not center)
#################################################
from sc_dr.datasets import *

import pickle
import sys
import os
import argparse
import time
import tempfile


import numpy as np

from sklearn.manifold import TSNE, Isomap, LocallyLinearEmbedding,\
                             SpectralEmbedding, MDS
from sklearn.decomposition import PCA, FactorAnalysis, FastICA,\
                                  LatentDirichletAllocation, NMF,\
                                  KernelPCA, IncrementalPCA, SparsePCA,\
                                  MiniBatchSparsePCA, TruncatedSVD
from sklearn.preprocessing import scale
from sklearn.random_projection import GaussianRandomProjection, SparseRandomProjection

import nimfa
try:
    from ivis import Ivis
    IVIS_AVAILABLE=True
except ImportError:
    IVIS_AVAILABLE=False

import pandas as pd

try:
    import umap
    UMAP_AVAILABLE=True
except ImportError:
    UMAP_AVAILABLE=False
    
from MulticoreTSNE import MulticoreTSNE as MCTSNE

try:
    from saucie import SAUCIE, Loader
    SAUCIE_AVAILABLE=True
except ImportError:
    SAUCIE_AVAILABLE=False

try:
    import scscope
    SCSCOPE_AVAILABLE=True
except ImportError:
    SCSCOPE_AVAILABLE=False

try:
    from phate import PHATE
    PHATE_AVAILABLE=True
except ImportError:
    PHATE_AVAILABLE=False

try:
    from tga import TGA
    TGA_AVAILABLE=True
except ImportError:
    TGA_AVAILABLE=False

try:
    from vpac import VPAC
    VPAC_AVAILABLE=True
except ImportError:
    VPAC_AVAILABLE=False

try:
    from vasc import vasc
    VASC_AVAILABLE=True
except ImportError:
    VASC_AVAILABLE=False

try:
    from ZIFA import block_ZIFA
    ZIFA_AVAILABLE=True
except ImportError:
    ZIFA_AVAILABLE=False


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

class NimfaWrapper():
    """
    Wrapper calss for nimfa functions to be applied like sklearn functions
    """

    def __init__(self,func,k):
        self.k = k
        self.func = func

    def fit_transform(self,data):
        self.model = self.func(np.transpose(data),rank=self.k)
        self.model_fit = self.model()
        return self.model_fit.coef().T

class SaucieWrapper():
    def __init__(self,k):
        self.k = k
        pass

    def fit_transform(self,data):
        self.model = SAUCIE(data.shape[1],layers=[512,256,128,self.k])
        loadtrain = Loader(data,shuffle=True)
        # Keep training until loss stabilizes
        losses = list()
        max_epochs=500
        not_converged = True
        while(not_converged):
            self.model.train(loadtrain,steps=int(np.floor(data.shape[0]/256)))
            losses.append(float(self.model.get_loss(loadtrain)))
            if len(losses) < 100: # keep training
                continue
            if loadtrain.epoch >= max_epochs: # give up
                not_converged = False
            
            mloss = np.mean(losses[-10:-5])
            nloss = np.mean(losses[-5:])
            perc_change = np.abs((nloss-mloss)/mloss)
            if perc_change < 0.0001:
                not_converged = False

        if(loadtrain.epoch >= max_epochs):
            print("Failed to converge in {} epochs".format(max_epochs))
        else:
            print("Finished training saucie model in {} epochs".format(loadtrain.epoch))
        return self.model.get_embedding(loadtrain)

class VascWrapper():
    def __init__(self,k):
        self.k = k

    def fit_transform(self,data):
        return vasc(data,epoch=500,latent=self.k)

class VpacWrapper():
    def __init__(self,k):
        self.k = k

    def fit_transform(self,data):
        self.model = VPAC(np.transpose(data),latent_dim=self.k,n_components=self.k)
        self.model.fit()
        return np.transpose(self.model.transform(np.transpose(data)))

class IvisWrapper():
    def __init__(self,dims):
        self.k = dims

    def fit_transform(self,data):
        self.model = Ivis(embedding_dims=self.k, k=8)
        x = self.model.fit_transform(data)
        os.remove(self.model.annoy_index_path) # necessary cleanup
        return x
    
def _embedding_error(*args):
    print("ERROR: invalid emedding method",file=sys.stderr)
    exit()

model_dict = {
    'bd': lambda args: NimfaWrapper(nimfa.Bd,args.dims),
    'fa':lambda args: FactorAnalysis(n_components=args.dims),
    'fica':lambda args: FastICA(n_components=args.dims),
    'grp':lambda args: GaussianRandomProjection(n_components=args.dims),
    'icm': lambda args: NimfaWrapper(nimfa.Icm,args.dims),
    'ipca':lambda args: IncrementalPCA(n_components=args.dims), 
    'ivis':lambda args: IvisWrapper(args.dims) if IVIS_AVAILABLE else _embedding_error(),
    'isomap':lambda args: Isomap(n_components=args.dims,n_jobs=args.njobs),
    'kpca-pol':lambda args: KernelPCA(n_components=args.dims, kernel='poly', n_jobs=args.njobs),
    'kpca-rbf':lambda args: KernelPCA(n_components=args.dims, kernel='rbf', n_jobs=args.njobs),
    'kpca-sig':lambda args: KernelPCA(n_components=args.dims, kernel='sigmoid', n_jobs=args.njobs),
    'kpca-cos':lambda args: KernelPCA(n_components=args.dims, kernel='cosine', n_jobs=args.njobs),
    'lda':lambda args: LatentDirichletAllocation(args.dims),
    'lle':lambda args: LocallyLinearEmbedding(n_components=args.dims,n_jobs=args.njobs),
    'lfnmf': lambda args: NimfaWrapper(nimfa.Lfnmf,args.dims),
    'lsnmf': lambda args: NimfaWrapper(nimfa.Lsnmf,args.dims),
    'mctsne':lambda args: MCTSNE(n_components=args.dims,n_jobs=args.njobs),
    'mds':lambda args: MDS(n_components=args.dims,n_jobs=args.njobs),
    'nmf':lambda args: NMF(args.dims),
    'nmf2': lambda args: NimfaWrapper(nimfa.Nmf,args.dims),
    'nsnmf': lambda args: NimfaWrapper(nimfa.Nsnmf,args.dims),
    'pca':lambda args: PCA(n_components=args.dims),
    'phate':lambda args: PHATE(n_components=args.dims,n_jobs=args.njobs) if PHATE_AVAILABLE else _embedding_error(),
    'pmf': lambda args: NimfaWrapper(nimfa.Pmf,args.dims),
    'psmf': lambda args: NimfaWrapper(nimfa.Psmf,args.dims),
    'saucie': lambda args: SaucieWrapper(args.dims) if SAUCIE_AVAILABLE else _embedding_error(),
    'scscope':lambda args: ScScope(args.dims) if SCSCOPE_AVAILABLE else _embedding_error,
    'sepnmf': lambda args: NimfaWrapper(nimfa.SepNMF,args.dims),
    'spca':lambda args: SparsePCA(n_components=args.dims, n_jobs=args.njobs, normalize_components=True),
    'spca-batch': lambda args: MiniBatchSparsePCA(n_components=args.dims, n_jobs=args.njobs, normalize_components=True),
    'spectral':lambda args: SpectralEmbedding(n_components=args.dims,n_jobs=args.njobs),
    'snmf': lambda args: NimfaWrapper(nimfa.Snmf,args.dims),
    'srp': lambda args: SparseRandomProjection(n_components=args.dims),
    'tga': lambda args: TGA(n_components=args.dims) if TGA_AVAILABLE else _embedding_error(),
    'tsvd': lambda args: TruncatedSVD(n_components=args.dims),
    'tsne':lambda args: TSNE(n_components=args.dims),
    'umap':lambda args: umap.UMAP(n_components=args.dims) if UMAP_AVAILABLE else _embedding_error(),
    'vpac':lambda args: VpacWrapper(args.dims) if VPAC_AVAILABLE else _embedding_error(),
    'vasc':lambda args: VascWrapper(args.dims) if VPAC_AVAILABLE else _embedding_error(),
    'zifa':lambda args: ZIFA_Wrapper(args.dims) if ZIFA_AVAILABLE else _embedding_error(),
}


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
        choices = list(model_dict.keys()),
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

    if not args.method in model_dict:
        _embedding_error()

    return model_dict[args.method](args)

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
