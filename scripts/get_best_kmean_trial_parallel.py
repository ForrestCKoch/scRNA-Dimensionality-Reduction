#!/usr/bin/python3
import sys
import os
import glob
import re

import pandas as pd
import numpy as np

import multiprocessing as mp

def process_data_method_tuple(targ):
    dataset=targ[0]
    method=targ[1]
    kmeans_results = 'data/results/kmeans'
    count_types = os.listdir(os.path.join(kmeans_results,dataset))
    #print('{0:20} {1:20}'.format(dataset,method))
    all_optimal_rows = pd.DataFrame()
    for count in count_types:
        workdir = os.path.join(kmeans_results,dataset,count,method)
        # only iterate if the folder exists ...
        for file in os.listdir(workdir) if os.path.exists(workdir) else []:
            dims = file.split('.')[0]
            # Load the csv into pandas
            try:
                x = pd.read_csv(os.path.join(workdir,file),
                        names=['k','time',
                               'ari','nmi','ss','vrc',
                               'dbs','errors'],
                        engine='python',error_bad_lines=False)
            except pd.errors.EmptyDataError:
                continue

            # Drop the errors column and then any row containing NA's
            x = x.drop('errors',axis=1).dropna()

            if x.shape[0] == 0:
                continue

            # add some extra information ...
            x['dataset'] = dataset
            x['method'] = method
            x['count_type'] = count
            x['dimensions'] = dims

            # get the rows we want to keep
            tokeep = [ x.nlargest(1,i) for i in ['ari','nmi','ss','vrc']] 
            tokeep += [ x.nsmallest(1,i) for i in ['dbs']]

            optimal_rows = pd.concat(tokeep)

            all_optimal_rows = all_optimal_rows.append(optimal_rows)

    # get the rows we want to keep but this time across all dimensions
    if all_optimal_rows.shape[0] == 0:
        #print('failed ...')
        return None

    #print('{0:20} {1:20}'.format(dataset,method))
    tokeep = [ all_optimal_rows.nlargest(1,i) for i in ['ari','nmi','ss','vrc']] 
    tokeep += [ all_optimal_rows.nsmallest(1,i) for i in ['dbs']]
    optimal_rows = pd.concat(tokeep)
    # keep track of which criteria that row is optimal for
    optimal_rows['loss_criteria'] = ['ari','nmi','ss','vrc','dbs']
    return optimal_rows


if __name__ == '__main__':

    kmeans_results = 'data/results/kmeans'
    # Iterate datsets ...
    #method_optimal_rows = pd.DataFrame()
    p = mp.Pool(10)
    argument_tuples = []
    for dataset in os.listdir(kmeans_results):
        count_types = os.listdir(os.path.join(kmeans_results,dataset))
        methods_set = set(np.concatenate([os.listdir(os.path.join(kmeans_results,dataset,x)) for x in count_types]))
        for m in methods_set:
            argument_tuples.append((dataset,m))

    results_list = p.map(process_data_method_tuple,argument_tuples)
    print(len([r for r in results_list if r is not None]))
    method_optimal_rows = pd.concat([r for r in results_list if r is not None]) 
    #method_optimal_rows.columns=method_optimal_rows.columns.str.strip()
    #method_optimal_rows.sort_values(by=['dataset','method','loss_criteria'],inplace=True)

    p.close()
    p.join()

    method_optimal_rows.to_csv('data/results/optimal_kmeans_trials.csv')            
