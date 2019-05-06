
import pickle
import sys

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import cm

import numpy as np

from sklearn.cluster import DBSCAN
from sklearn.manifold import TSNE

from svr2019.datasets import *

import torch

from ptsdae.sdae import StackedDenoisingAutoEncoder as SDAE

if __name__ == '__main__':
    # #############################################################################
    dset = sys.argv[1]
    #raw_data = DuoBenchmark('data/datasets/'+dset+'.csv')
    raw_data = FromPickle('data/embeddings/mouse-pca-15000-log1p-True.pickle')
    model = SDAE([raw_data.dims,7500,500,2000,50])
    #model.load_state_dict(torch.load('data/models/'+dset+'.pt'))
    model.load_state_dict(torch.load(sys.argv[1]))
    if int(torch.__version__.split('.')[1]) == 3:
        var = torch.autograd.variable.Variable(torch.Tensor(raw_data.data))
    else:
        var = torch.Tensor(raw_data.data)
    embedding = model.encoder(var).data.numpy()

    labels = DBSCAN().fit(embedding).labels_

    tsne_embedding = TSNE(n_components=2).fit_transform(embedding)

    # #############################################################################


    plt_file = 'data/plots/mouse_SDAE.pdf'

    plt.scatter(tsne_embedding[:,0],tsne_embedding[:,1],c=labels,s=1,marker=',')

    plt.title('Clusters in %s: %d' % (dset,max(labels)+1))
    plt.savefig(plt_file)
