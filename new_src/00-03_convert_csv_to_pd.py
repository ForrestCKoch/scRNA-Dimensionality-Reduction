#!/usr/bin/env python3
import numpy as np
import pandas as pd
import sys
ds = sys.argv[1]
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

