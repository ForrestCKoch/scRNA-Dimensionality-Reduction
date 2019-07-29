import h5py
import sys
from tqdm import tqdm
from scipy.stats import hypergeom

import multiprocessing as mp

from nb_cell_classifier import get_marker_matrix, get_gene_indicies, get_cell_expr

def initialize_worker(h5file,marker_file):
    global n_genes
    global n_avail_genes
    global index_set
    global available_markers
    global h5
    h5 = h5py.File(h5file,'r')

    markers = get_marker_matrix(marker_file)
    target_set = set(markers.keys())
    gene_idx = get_gene_indicies(h5,target_set)
    
    available_genes = [x[1] for x in gene_idx]
    gene_set = set(available_genes)
    index_set = set([x[0] for x in gene_idx])
    available_markers = markers[available_genes]

    n_genes = len(h5['mm10']['gene_names'])

    n_avail_genes = len(available_genes)

def classify_cell(i):
    cell_expr = set(get_cell_expr(i,h5,index_set,2))
    outfile = str(mp.current_process().name)+'.txt'
    with open('hypergeom/'+outfile,'a') as fh:
        if len(cell_expr)>0:
            min_p_value = 1.0
            min_cell_type = None
            for cell_type in available_markers.index:
                cell_type_genes = set(
                        available_markers.columns[ available_markers.loc[cell_type] > 0 ]
                )
                
                M = n_avail_genes
                n = len(cell_type_genes)+1
                N = len(cell_expr)+1
                k = len(set.intersection(cell_type_genes,cell_expr))

                p_value = 1-hypergeom.cdf(k,M,n,N)

                if p_value < min_p_value:
                    min_p_value = p_value
                    min_cell_type = cell_type
                    min_n = n
                    min_N = n
                    min_k = k
            print('{},{},{},{},{},{}'.format(
                str(i),
                min_cell_type,
                str(min_p_value),
                len(cell_expr),
                N-1,
                min_k),
                file=fh
            )
        else:
            print('{},NA,NA,0'.format(i),file=fh)


if __name__ == '__main__':
    h5file = sys.argv[1]
    marker_file = sys.argv[2]
    h5 = h5py.File(h5file,'r')
    ncells = len(h5['mm10']['indptr'])
    del h5
    p = mp.Pool(32,initialize_worker,[h5file,marker_file])
    p.map(classify_cell,range(0,ncells))
