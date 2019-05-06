#!/usr/bin/evn python3 -u

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


if __name__ == '__main__':
    ###############################################################################
    # For each of the pickled & trained SDAEs in data/sdae_embeddings
    # load it in and calculate the low-dimensional embedding for the coresponding dataset ..
    ###############################################################################

    model_dir = 'data/models'
    model_list = os.listdir(model_dir)
    model_dict = {}

    # to avoid reloading each dataset multiple times, we should sort then out a bit
    print("Loading Model List ...")
    for model in model_list:
        #####################################
        # This section is a bit fiddly as it
        # takes advantage of how the training
        # script saves everything
        #####################################
        tokens = model.split('_')
        ds_name = tokens[0]
        layers = [int(x) for x in tokens[1].split('-')]
        log = str2bool(tokens[7].split('-')[1]) 
        scale  = str2bool(tokens[8].split('-')[1].split('.')[0]) 
        if ds_name not in model_dict:
            # Don't touch the following line... I don't remember
            # why it works but it does so don't break it!
            model_dict[ds_name] = [[[],[]],[[],[]]] # list for 2 lists of 2 lists
        model_dict[ds_name][log][scale].append((model,layers))

    print("Calculating embeddings ...")
    # To avoid loading in each dataset a bazillion times
    # work on one dataset at a time
    for ds_name in model_dict.keys():
        for log in [True]:
            print("Loading "+ds_name+"-log-" + str(log) +" dataset")
            ds_path = os.path.join('data/datasets',ds_name+'.csv')
            dataset = DuoBenchmark(ds_path,log1p=log,split_head=False)
            
            for scale in [True]:
                # Do scaling second as the function will 
                # overwrite the existing data
                # yes - yes I know this is bad design but it's too late now
                mlist = model_dict[ds_name][log][scale]
                # Given all of the pre-existing conditions ...
                # cycle through each of the models that match this criteria 
                for model in mlist:
                    filename = model[0]
                    print(filename)
                    if scale:
                        scale_dataset(dataset)
                    # get parameter information
                    model_path = os.path.join(model_dir,filename)
                    layers = model[1]
                    # prepare the model
                    model = SDAE([dataset.dims]+layers)
                    model.load_state_dict(torch.load(model_path,map_location='cpu'))
                    # generate the embedding
                    inputs = torch.Tensor(dataset.data)
                    embedding = model.encoder(inputs).data.numpy()
                    # save the embedding
                    with open(os.path.join('data/sdae_embeddings',filename+'.pickle'),'wb') as fh:
                        pickle.dump(embedding,fh,protocol=4)
