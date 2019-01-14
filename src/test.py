from svr2019.datasets import E18MouseData
from torch.utils.data import DataLoader
from tqdm import tqdm

ds = E18MouseData('data/datasets/GSE93421_brain_aggregate_matrix.hdf5',nproc=20,selection=list(range(0,1000)))
dl = DataLoader(ds,num_workers=8)

"""
for i in tqdm(dl):
    x = ds.__getitem__(i)
"""

x = 0
for i in tqdm(dl):
    x += 1

