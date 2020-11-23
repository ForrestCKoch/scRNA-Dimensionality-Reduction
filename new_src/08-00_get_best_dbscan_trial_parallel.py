#!/usr/bin/python3
"""
    08-00_get_best_dbscan_trial_parallel.py

    This script will search the each of the results files from the dbscan random trials and find which
    trials resulted in the "best" scores (for a variety of measures). Runs using 10 threads by default.
"""
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
    metric=targ[2]
    dbscan_results = 'data/results/dbscan'
    count_types = os.listdir(os.path.join(dbscan_results,dataset))
    all_optimal_rows = pd.DataFrame()
    for count in count_types:
        workdir = os.path.join(dbscan_results,dataset,count,method,metric)
        # only iterate if the folder exists ...
        for file in os.listdir(workdir) if os.path.exists(workdir) else []:
            dims = file.split('.')[0]
            # Load the csv into pandas
            try:
                x = pd.read_csv(os.path.join(workdir,file),
                        names=['metric','eps','minpts','nclust','percnoise','time',
                               'ari','nnari','nmi','nnnmi','ss','nnss','vrc','nnvrc',
                               'dbs','nndbs','errors'],
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
            tokeep = [ x.nlargest(1,i) for i in ['ari','nnari','nmi','nnnmi','ss','nnss','vrc','nnvrc']] 
            tokeep += [ x.nsmallest(1,i) for i in ['dbs','nndbs']]

            optimal_rows = pd.concat(tokeep)

            all_optimal_rows = all_optimal_rows.append(optimal_rows)

    # get the rows we want to keep but this time across all dimensions
    if all_optimal_rows.shape[0] == 0:
        #print('failed ...')
        return None

    tokeep = [ all_optimal_rows.nlargest(1,i) for i in ['ari','nnari','nmi','nnnmi','ss','nnss','vrc','nnvrc','dbs','nndbs']] 
    optimal_rows = pd.concat(tokeep)

    # keep track of which criteria that row is optimal for
    optimal_rows['loss_criteria'] = ['ari','nnari','nmi','nnnmi','ss','nnss','vrc','nnvrc','dbs','nndbs']
    return optimal_rows


if __name__ == '__main__':

    dbscan_results = 'data/results/dbscan'

    # Iterate datsets ...
    p = mp.Pool(10)
    for metric in ['euclidean', 'seuclidean', 'correlation','cosine']:
        argument_tuples = []
        for dataset in os.listdir(dbscan_results):
            count_types = os.listdir(os.path.join(dbscan_results,dataset))
            methods_set = set(np.concatenate([os.listdir(os.path.join(dbscan_results,dataset,x)) for x in count_types]))
            for m in methods_set:
                argument_tuples.append((dataset,m,metric))

        results_list = p.map(process_data_method_tuple,argument_tuples)
        method_optimal_rows = pd.concat([r for r in results_list if r is not None]) 
        method_optimal_rows.to_csv('data/results/optimal_dbscan_trials_'+metric+'_tmp.csv')            

    p.close()
    p.join()
