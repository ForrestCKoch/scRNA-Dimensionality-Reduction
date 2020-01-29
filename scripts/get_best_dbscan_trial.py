#!/usr/bin/python3
import sys
import os
import glob
import re

import pandas as pd
import numpy as np


if __name__ == '__main__':

    dbscan_results = 'data/results/dbscan'
    # Iterate datsets ...
    method_optimal_rows = pd.DataFrame()
    for dataset in os.listdir(dbscan_results):
        count_types = os.listdir(os.path.join(dbscan_results,dataset))
        methods_set = set(np.concatenate([os.listdir(os.path.join(dbscan_results,dataset,x)) for x in count_types]))
        for method in methods_set:
            print('{0:20} {1:20}'.format(dataset,method))
            all_optimal_rows = pd.DataFrame()
            for count in count_types:
                workdir = os.path.join(dbscan_results,dataset,count,method,'euclidean')
                # only iterate if the folder exists ...
                for file in os.listdir(workdir) if os.path.exists(workdir) else []:
                    dims = file.split('.')[0]
                    # Load the csv into pandas
                    try:
                        x = pd.read_csv(os.path.join(workdir,file),
                                names=['metric','eps','minpts','nclust','percnoise','time',
                                       'ari','nnari','nmi','nnnmi','ss','nnss','vrc','nnvrc',
                                       'dbs','nndbs','errors'],
                                engine='python')
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
                print('failed ...')
                continue

            tokeep = [ all_optimal_rows.nlargest(1,i) for i in ['ari','nnari','nmi','nnnmi','ss','nnss','vrc','nnvrc']] 
            tokeep += [ all_optimal_rows.nsmallest(1,i) for i in ['dbs','nndbs']]
            optimal_rows = pd.concat(tokeep)
            # keep track of which criteria that row is optimal for
            optimal_rows['loss_criteria'] = ['ari','nnari','nmi','nnnmi','ss','nnss','vrc','nnvrc','dbs','nndbs']
            method_optimal_rows = method_optimal_rows.append(optimal_rows)

    method_optimal_rows.to_csv('data/results/optimal_dbscan_trials.csv')            
            

        #all_optimal_rows.to_csv(os.path.join(workdir,''))
# TODO:
# work out how to combine results from each of the files to create a summary csv of the best performing trials for each embedding


