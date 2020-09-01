##!/usr/bin/env python3
###############################################################################
# Usage: "python3 00-03_convert_csv_to_pd.py [dataset_name]"
# 
# Converts the specified *.csv.gz into a pickled pandas dataframe
###############################################################################
import sys
import os

import numpy as np
import pandas as pd

def main(ds):
    x = pd.read_csv('data/datasets/csvs/'+ds+'.csv.gz')
    x = x.rename(columns={'Unnamed: 0':'cell_type'})
    cell_type = x['cell_type']
    x = x.drop('cell_type',axis=1)
    # Drop Columns with unexpressed genes
    to_drop = (x.apply(np.sum,axis=0) == 0)
    keys_to_drop = np.array(x.keys())[to_drop]
    x = x.drop(keys_to_drop,axis=1)
    x.insert(0,'cell_type',cell_type)
    x.to_pickle('data/datasets/pddf/'+ds+'.pkl')

if __name__ == '__main__':
    if(len(sys.argv) != 2):
        print("Usage: python3 00-03_convert_csv_to_pd.py [dataset_name]",file=sys.stderr)
        exit()
    main(sys.argv[1])
