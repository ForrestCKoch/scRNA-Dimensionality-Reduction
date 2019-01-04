#!/usr/bin/env python3
from typing import Any, Callable, Optional
from time import time

import numpy as np

import torch
from torch.utils.data import Dataset
from torchvision import transforms

from tqdm import tqdm
import h5py
import sharedmem as sm



class E18MouseData(Dataset):

    def __init__(self, 
                 path: str,
                 nproc: Optional[int] = 1,
                 ratio: Optional[float] = 1.0,
                 silent: Optional[bool] = False ) -> None:
        """
        PyTorch Dataset wrapper to handle the GSE93421 hdf5 dataset

        :param path: path to hdf5 file for e18 Mouse Data
        :param nproc: number of processes to use in contructing vectors
        :param ratio: ratio of the dataset to actually load
        :param silent: whether print statements should print
        """
        # 
        hdf5 = h5py.File(path,'r',driver='core')
        self.dims = len(hdf5['mm10']['genes'])
        self._len = int(len(hdf5['mm10']['indptr'])*ratio)
        #self.cells = sm.full((self._len,self.dims),0,dtype=np.int16)
        # Load all of the important information into memory

        #############
        # Data
        #############
        if not silent: print("Reading data ...")
        start = time()

        ds = hdf5['mm10']['data']
        data = sm.empty(len(ds),dtype=ds.dtype)
        ds.read_direct(data)
        tmp = ds.dtype

        end = time()
        if not silent: print("\t"+str(end-start)+"s ...")

        #############
        # Indices
        #############
        if not silent: print("Reading indices ...")
        start = time()

        ds = hdf5['mm10']['indices']
        indx = sm.empty(len(ds),dtype=ds.dtype)
        ds.read_direct(indx)

        end = time()
        if not silent: print("\t"+str(end-start)+"s ...")

        
        #############
        # Indptr
        #############
        if not silent: print("Reading indptr ...")
        start = time()

        ds = hdf5['mm10']['indptr']
        iptr = sm.empty(len(ds),dtype=ds.dtype)
        ds.read_direct(iptr)

        end = time()
        if not silent: print("\t"+str(end-start)+"s ...")

        hdf5.close()

        ###########################
        # Create empty cell vectors
        ###########################
        # build the vector foreach cell 
        if not silent: print("Creating 0 vectors ...")
        start = time()

        self.cells = sm.full((self._len,self.dims),0,dtype=tmp)
        #self.cells = sm.full((self._len,self.dims),0,dtype=float)
        
        end = time()
        if not silent: print("\t"+str(end-start)+"s ...")
        
        ###########################
        # Multi-core loading ...
        ###########################
        if not silent: print("Building Tensor List ...")
        start = time()
        with sm.MapReduce(np = nproc) as pool:
            pool.map(_build_tensor, list(zip(
                    [self.cells] * nproc, [iptr] * nproc,
                    [indx] * nproc, [data] * nproc,
                    range(0,nproc) ,[nproc] * nproc))
            )

        end = time()
        if not silent: print("\t"+str(end-start)+"s ...")
    
        # Some explicit cleanup to conserve memory
        # Not sure if necessary, but I don't trust Python
        del iptr
        del indx
        del data
   
    def __getitem__(self, index):
        return torch.Tensor(self.cells[index])

    def __len__(self):
        return self._len

def _build_tensor(args):
    """
    Helper function to allow parallel loading of tensors 
    """
    cells,iptr,indx,data,tid,nproc = args

    for index in range(0+tid,len(cells),nproc):
        sidx = iptr[index]
        # find the number of gene entries for
        # this cell
        if index < len(iptr) - 1:
            # find length to next cell
            nentries = iptr[index + 1] - sidx 
        else:
            # find length to the end
            nentries = len(data) - sidx

        for i in range(0,nentries):
            cells[index][indx[sidx+i]] = (data[sidx+i])
            #cells[index][indx[sidx+i]] = float(data[sidx+i])

if __name__ == '__main__':
    pass
