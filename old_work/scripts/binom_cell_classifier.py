import h5py
import sys
from tqdm import tqdm
from scipy.stats import binom

from nb_multithreaded import get_marker_matrix, get_gene_indicies

def get_count_dict(n,h5file,index_set):
    count_dict = {i:0 for i in list(index_set)}
    start_idx = h5['mm10']['indptr'][n]
    end_idx = h5['mm10']['indptr'][n+1] - 1 if n+1 < len(h5['mm10']['indptr']) \
        else len(h5['mm10']['indptr'])

    for i in range(start_idx,end_idx+1):
        idx = h5['mm10']['indices'][i]
        if idx in index_set:
            v = h5['mm10']['data'][i]
            count_dict[idx] += max(0,v-1)
    return count_dict

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

    ngenes = len(available_genes)
    gene_to_idx = {h5['mm10']['gene_names'][i].decode().lower():i for i in index_set}
    for i in range(0,len(h5['mm10']['indptr'])):
        count_dict = get_count_dict(i,h5,index_set)
        count_total = sum([count_dict[k] for k in count_dict.keys()])
        min_p_value = 1.0
        min_cell_type = None
        for cell_type in available_markers.index:
            cell_type_genes = available_markers.columns[
                    available_markers.loc[cell_type] > 0 ]
            count = 0
            for g in cell_type_genes:
                g_idx = gene_to_idx[g]
                count += count_dict[g_idx]
            p_value = binom.cdf(count,n=count_total,p=len(cell_type_genes)/ngenes)
            if p_value < min_p_value:
                min_p_value = p_value
                min_cell_type = cell_type
        print('{},{},{}'.format(str(i),min_cell_type,str(min_p_value)))

