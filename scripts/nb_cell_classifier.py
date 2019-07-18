import pandas as pd
import numpy as np
import sys

def get_marker_matrix(filename):
    """
    Returns a binary matrix where rows represent cell types,
    columns represent gene markers, and entries represent
    whether the gene serves as a marker for the given cell type.
    :param filename: file to spreadsheet containing cell types and markers
    """
    df = pd.read_csv(filename)
    cell_types = df['cell type']
    gene_list = df['cell marker']
    gene_set = list()
    cell_marker_dict = dict()
    for i in range(0,len(df)): 
        ct = cell_types[i]
        genes = gene_list[i].split(', ')
        if ct not in cell_marker_dict:
            cell_marker_dict[ct] = list()
        for gene in genes:
            if gene not in gene_set:
                gene_set.append(gene)
            if gene not in cell_marker_dict[ct]:
                cell_marker_dict[ct].append(gene)
    cell_set = list(cell_marker_dict.keys())
    marker_matrix = np.zeros((len(cell_set),len(gene_set)))

    for i in range(0,len(cell_set)):
        for j in range(0,len(gene_set)):
            ct = cell_set[i]
            g = gene_set[j]
            if g in cell_marker_dict[ct]:
                marker_matrix[i,j] = 1

    return pd.DataFrame(marker_matrix,index=cell_set,columns=gene_set)

def get_conditionals(df,marker_weight):
    adj_df = (df*marker_weight)+1
    row_sums = adj_df.apply(np.sum,axis=1)
    return adj_df.apply(lambda x:np.divide(x,row_sums),axis=0)

def get_gene_indicies(h5file,targets):
    gene_names = list(h5file['mm10']['gene_names'])
    index_list = list()
    for i in range(0,len(gene_names)):
        if gene_names[i] in targets:
            index_list.append(i)

def get_cell_expr(n,h5file,index_set,thr):
    start_idx = h5['mm10']['indptr'][n]
    end_idx = h5['mm10']['indptr'][n+1] - 1 if n+1 < len(h5['mm10']['indptr']) \
            else len(h5['mm10']['indptr'])

    expr_genes = list()
    for i in range(start_idx,end_idx+1):
        idx = h5['mm10']['indices'][i]
        if idx in index_set:
            if h5['mm10']['data'][i] > thr:
                expr_genes.append(h5['mm10']['gene_names'][i].decode().lower()) 
    return expr_genes
    

if __name__ == '__main__':
    filename =  sys.argv[1]
