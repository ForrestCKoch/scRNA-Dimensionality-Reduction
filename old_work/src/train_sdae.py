#!/usr/bin/env python3
##################################################
# train_sdae.py
##################################################

import sys
import os
from datetime import datetime

import torch
import torch.utils.data
import torch.optim

import numpy as np

from sc_dm.datasets import *

import ptsdae
from ptsdae.sdae import StackedDenoisingAutoEncoder as SDAE
import ptsdae.model

import argparse

DEFAULT_DATASET='mouse'
DEFAULT_PRETRAIN_EPOCHS=250
DEFAULT_TRAIN_EPOCHS=2*DEFAULT_PRETRAIN_EPOCHS
DEFAULT_BATCH_SIZE=256
DEFAULT_PRETRAIN_LR=1.0
DEFAULT_TRAIN_LR=0.1
DEFAULT_LR_STEP=0.975
DEFAULT_NJOBS=1
DEFAULT_NPOINTS=250000
DEFAULT_LAYERS=[5000,500,2000,50]

def get_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--dataset',
        type=str,
        choices=['mouse','koh','kumar',
                 'simk4easy','simk4hard','simk8hard',
                 'zhengmix4eq','zhengmix8eq','pickle',
                 'chen','baron-human','campbell',
                 'macosko','marques','shekhar'],
        default=DEFAULT_DATASET,
        help='dataset to be used [Default: \'mouse\']'
    )

    parser.add_argument(
        '--pickle-path',
        type=str,
        default=None,
        help='if --dataset is set to pickle, load from this path [Default=None]'
    )
    
    parser.add_argument(
        '--pickle-name', 
        type=str,
        default=None,
        help='if --dataset is set to pickle, this will be the name written to file'
    )

    parser.add_argument(
        '--pretrain-epochs',
        type=int,
        default=DEFAULT_PRETRAIN_EPOCHS,
        help='the number of epochs to run at each stage during pretraining [Default: 250]'
    )

    parser.add_argument(
        '--train-epochs',
        type=int,
        default=DEFAULT_TRAIN_EPOCHS,
        help='the number of epochs to run at each stage during training [Default: 500]'
    )

    parser.add_argument(
        '--batch-size',
        type=int,
        default=DEFAULT_BATCH_SIZE,
        help='the batch size to be used [Default: 256]'
    )

    parser.add_argument(
        '--pretrain-lr',
        type=float,
        default=DEFAULT_PRETRAIN_LR,
        help='the learning rate to be used for pretraining [Default: 1.0]'
    )

    parser.add_argument(
        '--train-lr',
        type=float,
        default=DEFAULT_TRAIN_LR,
        help='the learning rate to be used for training [Default: 0.1]'
    )

    parser.add_argument(
        '--lr-step',
        type=float,
        default=DEFAULT_LR_STEP,
        help='multiplicative factor for LR at end of each epoch'
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
        '--scale',
        action='store_true',
        help='scale each feature 0-1 [Default: False]'
    )

    parser.add_argument(
        '--njobs',
        type=int,
        default=DEFAULT_NJOBS,
        help='how many jobs to use for loading data [Default: 1]',
    )

    parser.add_argument(
        '--npoints',
        type=int,
        default=DEFAULT_NPOINTS,
        help='how many points to load from the mouse dataset [Default: 250000]'
    )

    parser.add_argument(
        '--layers',
        nargs='+',
        type=int,
        default=DEFAULT_LAYERS
    ) 

    parser.add_argument(
        '--model-dir',
        type=str,
        default='data/models',
    )

    return parser

def get_dataset(args):
    if args.npoints == -1:
        selection = None
    else:
        selection = list(range(0,args.npoints))

    if args.dataset == 'mouse':
        ds_path = 'data/datasets/GSE93421_brain_aggregate_matrix.hdf5'
        data = E18MouseData(ds_path,
                          nproc=args.njobs,
                          selection=selection,
                          log1p=args.log1p)
    elif args.dataset == 'pickle':
        data = FromPickle(args.pickle_path)
    elif args.dataset in ['chen','baron-human','campbell','macosko','marques','shekhar']:
        ds_path = 'data/datasets/'+args.dataset+'.csv'
        data = DuoBenchmark(ds_path,log_trans=args.log,log1p=args.log1p,split_head=False)
    else:
        ds_path = 'data/datasets/'+args.dataset+'.csv'
        data = DuoBenchmark(ds_path,log_trans=args.log,log1p=args.log1p)

    if args.scale:
        print("Scaling dataset")
        scale_dataset(data)
    return data


if __name__ == '__main__':

    parser = get_parser()
    args = parser.parse_args()

    # a couple of local functions
    def get_opt(model, lr = args.pretrain_lr):
        return torch.optim.SGD(
                    params = model.parameters(),
                    lr = lr, 
                    momentum = 0.9)

    def get_sched(opt):
        return torch.optim.lr_scheduler.StepLR(
                    optimizer = opt,
                    step_size = 1,
                    gamma = args.lr_step,
                    last_epoch = -1)

    print("Loading Data ...")
    sys.stdout.flush()
    dataset = get_dataset(args)

    validation = None

    ae = SDAE([dataset.dims] + args.layers)

    timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    
    print("Pretraining ...")
    sys.stdout.flush()
    # pretrain
    ptsdae.model.pretrain(
                dataset,
                autoencoder = ae,
                epochs = args.pretrain_epochs,
                batch_size = args.batch_size, 
                optimizer = get_opt,
                scheduler = get_sched,
                validation = validation,
                update_freq = args.pretrain_epochs // 50,
                cuda = True,
                num_workers = args.njobs)
                            

    # train 

    # prep for cuda usage ...
    ae.cuda()

    # get our scheduler and optimizers
    opt = get_opt(ae,lr = args.train_lr)
    sched = get_sched(opt)

    print("Training ...")
    sys.stdout.flush()
    ptsdae.model.train(
                dataset,
                autoencoder = ae,
                epochs = args.train_epochs,
                batch_size = args.batch_size,
                optimizer = opt,
                scheduler = sched,
                validation = validation,
                update_freq = args.train_epochs // 50,
                cuda=True, 
                num_workers = args.njobs)

    # Save just the autoencoder model
    print("Saving Autoencoder model ...")
    sys.stdout.flush()

    samples = len(dataset)
    if args.dataset == 'pickle':
        set_name = args.pickle_name + '-pickle'
    else:
        set_name = args.dataset

    if args.log1p or args.log:
        log_flag = 'true'
    else: 
        log_flag = 'false'

    model_name = '_'.join(
                    [set_name] +
                    ['-'.join([str(x) for x in args.layers])] +
                    ['plr-'+str(args.pretrain_lr)] +
                    ['tlr-'+str(args.train_lr)] +
                    ['step-'+str(args.lr_step)] +
                    ['pepoch-'+str(args.pretrain_epochs)] +
                    ['tepoch-'+str(args.train_epochs)] +
                    ['log-'+log_flag] +
                    ['scale-'+str(args.scale).lower()]
                 )+'.pt'

    torch.save(ae.state_dict(),os.path.join(args.model_dir,model_name))
