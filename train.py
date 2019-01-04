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


BATCH_SIZE = 512
EPOCHS = 100
RATIO = 0.01
LOADING_PROCS = 20
DL_WORKERS = 8

if __name__ == '__main__':
    dataset = E18MouseData(sys.argv[1],nproc = LOADING_PROCS,ratio = RATIO)
    SDAE_DIMS = [dataset.dims, 500, 500, 2000, 30]
    ae = SDAE(SDAE_DIMS)

    timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    
    # pretrain
    ptsdae.model.pretrain(dataset,ae,EPOCHS,BATCH_SIZE, 
                        lambda x : torch.optim.SGD(x.parameters(),
                        lr = 0.1, momentum = 0.9), cuda=True,
                        num_workers= DL_WORKERS)
                            
    ae.cuda()


    ptsdae.model.train(dataset,ae,EPOCHS,BATCH_SIZE,
                        torch.optim.SGD(ae.parameters(),lr = 0.1, momentum = 0.9),
                        cuda=True, num_workers = DL_WORKERS)

    # Save just the autoencoder model
    print("Saving Autoencoder model ...")
    torch.save(ae.state_dict(),os.path.join('models','ae_'+timestamp+'.pt'))
