#!/usr/bin/env python3
###########################################
# This module implements a few classes to 
# help load data into PyTorch compatible 
# datasets.
#
# Although the aim is PyTorch compatibility
# there is no problem in utilizing these
# datasets for general computation
###########################################
from typing import Any, Callable, Optional
from time import time

import numpy as np

#import torch
#from torch.utils.data import Dataset

from tqdm import tqdm
import h5py
import sharedmem as sm

import pickle

from sklearn.decomposition import PCA

from sklearn.preprocessing import LabelEncoder

class Dataset:
    pass

class DuoBenchmark(Dataset):
    def __init__(self,path,log_trans=False,log1p=False,split_head=True):
        """
        Load a dataset from a given path.

        The supplied file should be ',' separated with the first row
        consisting of cell identifiers in one of two formats indicated by
        the split_head parameter.
            -- split_head=True : identifiers are in the format 'id - type'
            -- split_head=False : identifiers are just the cell type

        Each remaining row are the counts for a particular gene
            ** note that there are no gene identifiers in this format
               ... this may need to be considered in future revisions
    
        Note: this was originally written to be used with datasets from the
        2018 Duo paper; however, it's utility has evolved beyond this
        and hence the name should be changed in future revisions.

        :param path: path to csv file
        :param log_trans: whether to take the log transform of the cell counts
        :param log1p: whether to take the log(1+x) transform of the cell counts
        :param split_head: indicated whether the header is 'id - type' (True) or 'type'
        """
        
        # Read the data in as np.float32
        self.data = np.transpose(np.genfromtxt(path,delimiter=',',skip_header=1,dtype=np.float32))

        # take the log transform if necessary
        if log_trans:
            self.data = np.log(self.data)
        elif log1p:
            self.data = np.log(1+self.data)

        # capture the labels from the header
        with open(path,'r') as fh:
            head = fh.readline().rstrip('\n').replace('"','')
            if split_head:
                self.labels = [(x.split('-'))[1].lstrip(' ') for x in head.split(',')]
            else:
                self.labels = head.split(',')

        # note for the following code block, there is
        # probably a cleaner way of doing this using
        # sklearn.preprocessing.LabelEncoder
        
        # assign each label a unique numerical id
        label_dict = dict()
        count = 0
        for label in self.labels:
            if label not in label_dict:
                label_dict[label] = count
                count += 1

        # assign each cell it's corresponding numerical id
        self.tags = [label_dict[l] for l in self.labels]

        # get the number of dimensions
        self.dims = len(self.data[0])
        

    # necessary for Dataset class
    def __getitem__(self, index):
        return self.data[index]

    # necessary for Dataset class
    def __len__(self):
        return len(self.labels)

class PCAReducedDuo(DuoBenchmark):
    """
    Same as DuoBenchmark but performs a preliminary PCA on the data.
    Usage is discouraged as it has not been updated to reflect recent
    Changes to the DuoBenchmark class
    """
    def __init__(self,path,n_components=2,log_trans=False,log1p=False):
        super(PCAReducedDuo,self).__init__(path,log_trans=log_trans,log1p=log1p)
        self.old_data = self.data
        self.data = PCA(n_components=n_components).fit_transform(self.old_data)
        self.dims = len(self.data[0])


class FromPickle(Dataset):
    """
    Load a Dataset from a pickled object.
    At this stage, however, labels will not be available
    for the Dataset.

    It is currently being used in scripts to compare
    embeddings.  Labels can be taken from the full dataset
    """
    def __init__(self,path):
        with open(path,'rb') as fh:
            self.data = pickle.load(fh).astype(np.float32)
        self.dims = len(self.data[0])
  
    def __getitem__(self,index):
        return self.data[index]

    def __len__(self):
        return len(self.data) 

class FromPickledPanda(Dataset):
    """
    Load a dataset from pickled pandas dataframe
    """
    def __init__(self,path):
        with open(path,'rb') as fh:
            pd_df = pickle.load(fh)
            self.labels = [str(x) for x in pd_df['cell_type']]
            pd_df = pd_df.drop('cell_type',axis=1)
            self.data = pd_df.values
            self.dims = len(self.data[0])
            self.tags = LabelEncoder().fit_transform(self.labels) 

    def __getitem__(self,index):
        return self.data[index]

    def __len__(self):
        return len(self.tags) 

class E18MouseData(Dataset):

    def __init__(self, 
                 path: str,
                 log1p: Optional[bool] = False,
                 nproc: Optional[int] = 1,
                 selection: Optional[list] = None,
                 silent: Optional[bool] = False ) -> None:
        """
        PyTorch Dataset wrapper to handle the GSE93421 hdf5 dataset

        :param path: path to hdf5 file for e18 Mouse Data
        :param nproc: number of processes to use in contructing vectors
        :param ratio: ratio of the dataset to actually load
        :param selection: list of cells to load data for
        :param silent: whether print statements should print
        """
        hdf5 = h5py.File(path,'r',driver='core')
        self.dims = len(hdf5['mm10']['genes'])
        
        # allow a customizable selection of cells
        if selection is not None:
            self._len = len(selection)
        else:
            self._len = len(hdf5['mm10']['indptr'])
            selection = range(0,self._len)
        self.selection = selection
        # get a list that can be shared between processes
        selected_cells = sm.empty(self._len,dtype=np.int)
        for i in range(0,self._len):
            selected_cells[i] = self.selection[i]
        
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
        del ds

        ###########################
        # Create empty cell vectors
        ###########################
        # build the vector foreach cell 
        if not silent: print("Creating 0 vectors ...")
        start = time()

        self.data = sm.full((self._len,self.dims),0,dtype=tmp)
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
                    [self.data] * nproc, [iptr] * nproc,
                    [indx] * nproc, [data] * nproc,
                    range(0,nproc) ,[nproc] * nproc,
                    [selected_cells] * nproc,
                    [log1p] * nproc))
            )

        end = time()
        if not silent: print("\t"+str(end-start)+"s ...")
    
        # Some explicit cleanup to conserve memory
        # Not sure if necessary, but I don't trust Python
        del iptr
        del indx
        del data
        del selected_cells
   
    def __getitem__(self, index):
        #return torch.Tensor(self.data[index])
        return np.array(self.data[index])

    def __len__(self):
        return self._len

def _build_tensor(args):
    """
    Helper function to allow parallel loading of tensors 
    """
    cells,iptr,indx,data,tid,nproc,selected,log1p = args

    for i in range(0+tid,len(cells),nproc):
        index = selected[i]
        sidx = iptr[index]
        # find the number of gene entries for
        # this cell
        if index < len(iptr) - 1:
            # find length to next cell
            nentries = iptr[index + 1] - sidx 
        else:
            # find length to the end
            nentries = len(data) - sidx

        for j in range(0,nentries):
            if log1p:
                cells[i][indx[sidx+j]] = np.log(1+(data[sidx+j]))
            else:
                cells[i][indx[sidx+j]] = (data[sidx+j])
            #cells[i][indx[sidx+j]] = float(data[sidx+j])

def scale_dataset(ds):
    """
    Scale each feature to be between 0 and 1
    Note that overwrites the original data.
    In the future, this function should be changed
    to retain scaling information
    
    :param ds: dataset to be scaled
    """
    for i in range(0,ds.dims):
        fmax = ds.data[0][i]
        for j in range(1,len(ds)):
            curr = ds.data[j][i]
            if curr > fmax:
                fmax = curr           
        if fmax > 0:
            for j in range(0,len(ds)):
                ds.data[j][i] /= fmax



if __name__ == '__main__':
    pass
