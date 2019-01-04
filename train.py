#!/bin/sh
import sys
import os
from datetime import datetime

import torch
import torch.utils.data
import torch.optim

from e18MouseData import E18MouseData

import ptsdae
from ptsdae.sdae import StackedDenoisingAutoEncoder as SDAE
import ptsdae.model


BATCH_SIZE = 256
EPOCHS = 500
RATIO = 0.01
LOADING_PROCS = 20
DL_WORKERS = 8

if __name__ == '__main__':

    # a couple of local functions
    def get_opt(model):
        return torch.optim.SGD(
                    params = model.parameters(),
                    lr = 0.1, 
                    momentum = 0.9)

    def get_sched(opt):
        return torch.optim.lr_scheduler.StepLR(
                    optimizer = opt,
                    step_size = 7500,
                    gamma = 0.1,
                    last_epoch = -1)

    dataset = E18MouseData(sys.argv[1],nproc = LOADING_PROCS,selection = None)
    SDAE_DIMS = [dataset.dims, 5000, 500, 500, 2000, 30]
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
                validation = dataset,
                update_freq = EPOCHS // 50,
                cuda = True,
                num_workers = DL_WORKERS)
                            

    # train 

    # prep for cuda usage ...
    ae.cuda()

    # get our scheduler and optimizers
    opt = get_opt(ae)
    sched = get_sched(opt)

    ptsdae.model.train(
                dataset,
                autoencoder = ae,
                epochs = 2 * EPOCHS,
                batch_size = BATCH_SIZE,
                optimizer = opt,
                scheduler = sched,
                validation = dataset,
                update_freq = EPOCHS // 50,
                cuda=True, 
                num_workers = DL_WORKERS)

    # Save just the autoencoder model
    print("Saving Autoencoder model ...")
    torch.save(ae.state_dict(),os.path.join('models','ae_'+timestamp+'.pt'))
