from e18MouseData import E18MouseData

import pickle
import sys

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

from sklearn.manifold import TSNE as sk_tsne
from sklearn.decomposition import PCA
from MulticoreTSNE import MulticoreTSNE as mc_tsne
import umap

NPROCS=20

def get_embedding(embed_func,npoints):
    ds = E18MouseData('GSE93421_brain_aggregate_matrix.hdf5',
                      nproc=NPROCS,
                      selection=list(range(0,npoints)))
    print('Generating Embedding ...')
    embedding = embed_func(ds.cells)
    return embedding

def umap_to_tsne(x):
    semi_embedded = umap.UMAP(n_components=50).fit_transform(x)
    embedded = mc_tsne(n_components=2,n_jobs=NPROCS).fit_transform(semi_embedded)
    return embedded

def pca_to_tsne(x):
    semi_embedded = PCA(n_components=50).fit_transform(x)
    embedded = mc_tsne(n_components=2,n_jobs=NPROCS).fit_transform(semi_embedded)
    return embedded

if __name__ == '__main__':

    embed_opt = sys.argv[1]

    if embed_opt == 'umap':
        embed_func = umap.UMAP().fit_transform
    elif embed_opt == 'pca':
        embed_func = PCA(n_components=2).fit_transform
    elif embed_opt == 'umap-mctsne':
        embed_func = umap_to_tsne
    elif embed_opt == 'pca-mctsne':
        embed_func = pca_to_tsne
    else:
        print("ERROR: Invalid embedding option", file=sys.stderr)
        exit()

    embedded = get_embedding(embed_func,250000)

    print('saving image')
    plt.scatter(embedded[:,0],embedded[:,1])
    plt.savefig('plots/'+embed_opt+'-250k.pdf')

    print('saving embedding')
    with open('embeddings/'+embed_opt+'-250k-embedding.pickle','wb') as fh:
        pickle.dump(embedded,fh,protocol=4)

