from e18MouseData import E18MouseData

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

from sklearn.manifold import TSNE

ds = E18MouseData('GSE93421_brain_aggregate_matrix.hdf5',nproc=20,selection=list(range(0,250000)))

print('applying tsne')
embedded = u.fit_transform(ds.cells)
embedded = TSNE(n_components=2).fit_transform(ds.cells)

print('saving image')
plt.scatter(embedded[:,0],embedded[:,1])
plt.savefig('tsne_250k.pdf')
