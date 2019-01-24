#!/bin/sh
import sys
import os
from datetime import datetime

import torch
import torch.utils.data
import torch.optim

import numpy as np

from svr2019.datasets import *

import ptsdae
from ptsdae.sdae import StackedDenoisingAutoEncoder as SDAE
import ptsdae.model

import argparse

BATCH_SIZE = 256
EPOCHS = 250
RATIO = 0.01
LOADING_PROCS = 20
DL_WORKERS = 8

TOTAL_SIZE = 1306127
TRAIN_SIZE = 10000
VALID_SIZE = 1000

def get_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--dataset',
        type=str,
        choices=['mouse','koh','kumar'
                 'simk4easy','simk4hard','simk8hard',
                 'zhengmix4eq','zhengmix8eq','pickle'],
        default='mouse',
        help='dataset to be used [Default: \'koh\']'
    )

    parser.add_argument(
        '--pickle-path',
        type=str,
        default=None,
        help='if --dataset is set to pickle, load from this path [Default=None]'
    )

    parser.add_argument(
        '--pretrain-epochs',
        type=int,
        default=250,
        help='the number of epochs to run at each stage during pretraining [Default: 250]'
    )

    parser.add_argument(
        '--train-epochs',
        type=int,
        default=500,
        help='the number of epochs to run at each stage during training [Default: 500]'
    )

    parser.add_argument(
        '--batch-size',
        type=int,
        default=256,
        help='the batch size to be used [Default: 256]'
    )

    parser.add_argument(
        '--pretrain-lr',
        type=float,
        default=1.0,
        help='the learning rate to be used for pretraining [Default: 1.0]'
    )

    parser.add_argument(
        '--train-lr',
        type=float,
        default=0.1,
        help='the learning rate to be used for training [Default: 0.1]'
    )

    parser.add_argument(
        '--log1p',
        action='store_true',
        help='apply a log(1+x) transform to the data [Default: False]'
    )

    parser.add_argument(
        '--log',
        action='store_true',
        help='apply a log transform to the data [Default: False]'
    )

    parser.add_argument(
        '--njobs',
        type=int,
        default=1,
        help='how many jobs to use for loading data [Default: 1]',
    )

    parser.add_argument(
        '--npoints',
        type=int,
        default=250000,
        help='how many points to load from the mouse dataset [Default: 250000]'
    )

    



    return parser


if __name__ == '__main__':

    # a couple of local functions
    def get_opt(model, lr = 1.0):
        return torch.optim.SGD(
                    params = model.parameters(),
                    lr = lr, 
                    momentum = 0.9)

    def get_sched(opt):
        return torch.optim.lr_scheduler.StepLR(
                    optimizer = opt,
                    step_size = 1,
                    gamma = 0.975,
                    last_epoch = -1)


    # get a selection
    """
    subset = np.random.choice(list(range(0,TOTAL_SIZE)),
                        size = TRAIN_SIZE + VALID_SIZE)
    np.random.shuffle(subset)
    train_set = subset[0:TRAIN_SIZE]
    valid_set = subset[TRAIN_SIZE:] 
    """
    train_set = list(range(0,250000))
    valid_set = list(range(250000,260000))

    #dataset = E18MouseData(sys.argv[1],nproc = LOADING_PROCS,selection = train_set)
    ds_name = sys.argv[1]
    ds_path = 'data/datasets/'+ds_name+'.csv'
    #dataset = DuoBenchmark(ds_path,log1p=True)
    #dataset = PCAReducedDuo(ds_path,n_components=250,log_trans=True)
    ds_path = 'data/embeddings/mouse-pca-15000-log1p-True.pickle'
    dataset = FromPickle(ds_path)
    #validation = E18MouseData(sys.argv[1],nproc = LOADING_PROCS,selection = valid_set)
    validation = None
    SDAE_DIMS = [dataset.dims, 7500, 500, 2000, 50]
    #SDAE_DIMS = [dataset.dims, 250, 1000, 50]
    ae = SDAE(SDAE_DIMS)

    timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    
    # pretrain
    ptsdae.model.pretrain(
                dataset,
                autoencoder = ae,
                epochs = EPOCHS,
                batch_size = BATCH_SIZE, 
                optimizer = get_opt,
                scheduler = get_sched,
                validation = validation,
                update_freq = EPOCHS // 50,
                cuda = True,
                num_workers = DL_WORKERS)
                            

    # train 

    # prep for cuda usage ...
    ae.cuda()

    # get our scheduler and optimizers
    opt = get_opt(ae,lr = 0.1)
    sched = get_sched(opt)

    ptsdae.model.train(
                dataset,
                autoencoder = ae,
                epochs = 2 * EPOCHS,
                batch_size = BATCH_SIZE,
                optimizer = opt,
                scheduler = sched,
                validation = validation,
                update_freq = EPOCHS // 50,
                cuda=True, 
                num_workers = DL_WORKERS)

    # Save just the autoencoder model
    print("Saving Autoencoder model ...")
    #model_name = ds_name+'_sdae_5k-500-2k-50_'+timestamp+'.pt' 
    model_name = ds_name +
                 '_sdae_' +
                 '-'.join(SDAE_DIMS +
                 '_' + timestamp +'.pt'
    torch.save(ae.state_dict(),os.path.join('data','models',model_name))
