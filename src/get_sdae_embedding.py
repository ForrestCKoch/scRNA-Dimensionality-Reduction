
import pickle
import sys
import os

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import cm

import numpy as np

from svr2019.datasets import *

import torch

from ptsdae.sdae import StackedDenoisingAutoEncoder as SDAE

def str2bool(x):
    return x == 'true'

##############################################################################
model_dir = 'data/models'
model_list = os.listdir(model_dir)
model_dict = {}
# to avoid reloading each dataset multiple times, we should sort then out a bit
for model in model_list:
    tokens = model.split('_')
    ds_name = tokens[0]
    layers = [int(x) for x in tokens[1].split('-')]
    log = str2bool(tokens[7].split('-')[1]) 
    scale  = str2bool(tokens[7].split('-')[1]) 
    if ds_name not in model_dict:
        model_dict[ds_name] = [[[],[]],[[],[]]] # list for 2 lists of 2 lists
    model_dict[ds_name][log][scale].append((model,layers))

for ds_name in model_dict.keys():
    for log in [True, False]:
        ds_path = os.path.join('data/datsets',ds_name+'.csv')
        dataset = DuoBenchmark(ds_path,log_trans=log)
        for scale in [False, True]:
            if scale:
                scale_dataset(dataset)
            # get parameter information
            filename = model_dict[ds_name][log][scale][0]
            model_path = os.path.join(model_list,model_path)
            layers = model_dict[ds_name][log][scale][1]
            # prepare the model
            model = SDAE([dataset.dims]+layers)
            model.load_state_dict(torch.load(model_path))
            # generate the embedding
            inputs = torch.Tensor(dataset.data)
            embedding = model.encoder(inputs).data.numpy()
            # save the embedding
            with open(os.path.join('data/sdae_embeddings',filename+'.pickle'),'wb') as fh:
                pickle.dump(embedding,fh,protocol=4)
