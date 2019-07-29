import pandas as pd
import numpy as np
import h5py
import sys
from tqdm import tqdm

import multiprocessing as mp

def get_marker_matrix(filename):
    """
    Returns a binary matrix where rows represent cell types,
    columns represent gene markers, and entries represent
    whether the gene serves as a marker for the given cell type.
    :param filename: file to spreadsheet containing cell types and markers
    """
    df = pd.read_csv(filename,engine='python')
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
    """
    return the class conditional probabilities of each gene
    :param df: pandas.DataFrame object with genes in columns and classes in rows
    :param marker_weight: multiplicative weighting factor for observed markers.
    each entry in the table will have 1 added to it to avoid 0 probability 
    conditionals.
    """
    adj_df = (df*marker_weight)+1
    row_sums = adj_df.apply(np.sum,axis=1)
    return adj_df.apply(lambda x:np.divide(x,row_sums),axis=0).astype(np.longdouble)

def get_likelihood(cell_expr,class_conditionals):
    pos = class_conditionals[cell_expr].astype(np.longdouble)
    neg = (1 - class_conditionals.drop(columns=cell_expr)).astype(np.longdouble)
    """
    print(pos.apply(np.prod,axis=1))
    print(neg.apply(np.prod,axis=1))
    likelihood = pos.apply(np.prod,axis=1)*((1-neg).apply(np.prod,axis=1))
    """
    log_pos = pos.apply(np.log,axis=0).astype(np.longdouble)
    sum_log_pos = log_pos.apply(np.sum,axis=1).astype(np.longdouble)
    
    log_neg = neg.apply(np.log,axis=0).astype(np.longdouble)
    sum_log_neg =log_neg.apply(np.sum,axis=1).astype(np.longdouble)

    tot = (sum_log_pos+sum_log_neg).astype(np.longdouble)

    exp_tot = tot.apply(np.exp).astype(np.longdouble)
    sum_tot = np.sum(exp_tot).astype(np.longdouble)
    log_tot = np.log(sum_tot).astype(np.longdouble)
    denom = log_tot
    #print(tot)
    #print(tot-denom)
    likelihood = (tot-denom).apply(np.exp)
    #print(np.sum(likelihood))
    #print(likelihood)
     
    return likelihood
    

def get_gene_indicies(h5file,target_set):
    """
    return the gene indices corresponding to the requested set of genes
    :param h5file: h5py.File object containing the E18 Mouse data
    :param target_set: set of genes which we are interested in
    """
    gene_names = list(h5file['mm10']['gene_names'])
    index_list = list()
    for i in range(0,len(gene_names)):
        gene = gene_names[i].decode().lower()
        if gene in target_set:
            index_list.append((i,gene))
    return index_list

def get_cell_expr(n,h5,index_set,thr):
    """
    return a set of expressed genes in the n^th sample
    :param n: cell id we are interested in
    :param h5: h5py.File object containing the E18 Mouse data
    :param index_set: set of gene indices we are interested in
    :param thr: threshold above which we will consider gene expression
    """
    start_idx = h5['mm10']['indptr'][n]
    end_idx = h5['mm10']['indptr'][n+1] - 1 if n+1 < len(h5['mm10']['indptr']) \
            else len(h5['mm10']['indptr'])

    expr_genes = list()
    for i in range(start_idx,end_idx+1):
        idx = h5['mm10']['indices'][i]
        if idx in index_set:
            if h5['mm10']['data'][i] > thr:
                expr_genes.append(h5['mm10']['gene_names'][idx].decode().lower()) 
    return expr_genes
    

#if __name__ == '__main__':
def initialize_worker(h5file,marker_file,K):
    # Declare the Global Variables First
    global class_conditionals
    global h5
    global index_set

    # get our h5file
    h5 = h5py.File(h5file,'r')

    # load the full marker csv into a matrix
    markers = get_marker_matrix(marker_file)
    # our targets are the columns of markers
    target_set = set(markers.keys())
    # obtain a list of idx,name pairs in the h5py file
    # that match what we have in the target set
    gene_idx = get_gene_indicies(h5,target_set)

    # obtain a list of genes available to be used as a marker
    available_genes = [x[1] for x in gene_idx]
    gene_set = set(available_genes)
    index_set = set([x[0] for x in gene_idx])
    # reduce the marker matrix to only contain available genes
    available_markers = markers[available_genes]

    # sanity checking
    """
    print(len(gene_idx))
    print(len(target_set))
    print(len(available_markers.keys()))
    """
    
    # generate the class conditionals for our marker genes
    class_conditionals = get_conditionals(available_markers,K)
    
def classify_cell(i):
    outfile = str(mp.current_process().name)+'.txt'
    with open(outfile,'a') as fh:
        expr = get_cell_expr(i,h5,index_set,2)
        if len(expr) > 0:
            likelihood = get_likelihood(expr,class_conditionals)
            cell_guess = likelihood.idxmax()
            print('{2},{0},{1},{3}'.format(
                cell_guess,
                likelihood[cell_guess],
                i,
                len(expr)),
                file=fh
            )
        else:
            print('{},NA,NA,0'.format(i),file=fh)

if __name__ == '__main__':
    h5 = h5py.File(sys.argv[1],'r')
    ncells = len(h5['mm10']['indptr'])
    del h5
    p = mp.Pool(32,initialize_worker,[sys.argv[1],sys.argv[2],2])
    p.map(classify_cell,range(0,ncells))
