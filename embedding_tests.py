from e18MouseData import E18MouseData

import pickle
import sys

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

from sklearn.manifold import TSNE as sk_tsne
from MulticoreTSNE import MulticoreTSNE as mc_tsne
import umap

NPROCS=20

def get_embedding(embed_func,npoints):
    ds = E18MouseData('GSE93421_brain_aggregate_matrix.hdf5',
                      nproc=NPROCS,
                      selection=list(range(0,npoints)))
    print('Generating Embedding ...')
    embedding = embed_func(ds.cells)

if __name__ == '__main__':

    embed_opt = sys.argv[1]

    if embed_opt == 'umap':
        embed_func = umap.UMAP().fit_transform
    elif embed_opt == 'sk_tsne':
        embed_func = sk_tsne(n_components=2).fit_transform
    elif embed_opt == 'mc_tsne':
        embed_func = mc_tsne(n_components=2).fit_transform
    else:
        print("ERROR: Invalid embedding option", file=sys.stderr)
        exit()

    embedded = get_embedding(embed_func,250000)

    print('saving image')
    plt.scatter(embedded[:,0],embedded[:,1])
    plt.savefig(embed_opt+'-250k.pdf')

    print('saving embedding')
    with open(embed_opt+'-250k-embedding.pickle','wb') as fh:
        pickle.dump(embedded,fh,protocol=4)

