import h5py
import sys
from tqdm import tqdm
from scipy.stats import hypergeom

from nb_cell_classifier import get_marker_matrix, get_gene_indicies, get_cell_expr

if __name__ == '__main__':
    h5file = sys.argv[1]
    marker_file = sys.argv[2]
    h5 = h5py.File(h5file,'r')

    markers = get_marker_matrix(marker_file)
    target_set = set(markers.keys())
    gene_idx = get_gene_indicies(h5,target_set)
    
    available_genes = [x[1] for x in gene_idx]
    gene_set = set(available_genes)
    index_set = set([x[0] for x in gene_idx])
    available_markers = markers[available_genes]

    n_genes = len(h5['mm10']['gene_names'])

    ngenes = len(available_genes)
    for i in range(0,len(h5['mm10']['indptr'])):
        cell_expr = set(get_cell_expr(i,h5,index_set,2))
        min_p_value = 1.0
        min_cell_type = None
        for cell_type in available_markers.index:
            cell_type_genes = set(
                    available_markers.columns[ available_markers.loc[cell_type] > 0 ]
            )
            
            M = n_genes
            n = len(cell_type_genes)
            N = len(cell_expr)
            k = len(set.intersection(cell_type_genes,cell_expr))

            p_value = hypergeom.cdf(k,M,n,N)

            if p_value < min_p_value:
                min_p_value = p_value
                min_cell_type = cell_type
        print('{},{},{}'.format(str(i),min_cell_type,str(min_p_value)))

