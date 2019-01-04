from e18MouseData import E18MouseData

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

import umap

ds = E18MouseData('GSE93421_brain_aggregate_matrix.hdf5',nproc=20,selection=None)

print('applying UMAP')
u = umap.UMAP()
embedded = u.fit_transform(ds.cells)

print('saving image')
plt.scatter(embedded[:,0],embedded[:,1])
plt.savefit('umap-all.pdf')
