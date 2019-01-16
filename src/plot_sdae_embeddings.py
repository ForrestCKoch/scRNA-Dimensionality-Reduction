
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

# #############################################################################
dset = sys.argv[1]
raw_data = DuoBenchmark('data/datasets/'+dset+'.csv')
model = SDAE([raw_data.dims,2500,500,2000,50])
model.load_state_dict(torch.load('data/models/'+dset+'.pt'))
var = torch.autograd.variable.Variable(torch.Tensor(raw_data.data))
embedding = model.encoder(var).data.numpy()

tsne_embedding = TSNE(n_components=2).fit_transform(embedding)

# #############################################################################


plt_file = 'data/plots/'+dset+'_SDAE.pdf'

plt.scatter(tsne_embedding[:,0],tsne_embedding[:,1],c=raw_data.tags,s=1,marker=',')

plt.title('Actual clusters in %s: %d' % (dset,max(raw_data.tags)+1))
plt.savefig(plt_file)
