import os
import sys
import pickle

import pandas as pd
import numpy as np
from sklearn.metrics import silhouette_samples
from tqdm import tqdm

EXCLUDED_TYPES = ["alpha.contaminated", "beta.contaminated", "delta.contaminated", "Excluded", "gamma.contaminated", "miss", "NA", "not applicable", "unclassified", "unknown", "Unknown", "zothers",'nan']

if __name__ == '__main__':
    #dataset = sys.argv[1]
    for dataset in tqdm(os.listdir('data/embeddings')):
        all_embeddings = []
        for count_type in tqdm(os.listdir('data/embeddings/'+dataset)):
            count_path = os.path.join('data/embeddings',dataset,count_type)
            for method in tqdm(os.listdir(count_path)):
                method_path = os.path.join(count_path,method)
                for dim in ['2','4','8','16','32','48','96']:
                    embedding_path = os.path.join(method_path,dim+'.pkl')
                    if os.path.exists(embedding_path):
                        x = pd.read_pickle(embedding_path)
                        to_remove = []
                        for i in range(len(x.cell_type)):
                            if x.cell_type[i] in EXCLUDED_TYPES or pd.isna(x.cell_type[i]):
                                to_remove.append(i)
                        x.drop(index=to_remove,inplace=True)
                        labs = x.cell_type
                        dat = x.drop('cell_type',axis=1)
                        try:
                            ss = pd.DataFrame(data=silhouette_samples(dat,labs))
                        except Exception as e:
                            continue
                        ss['cell_type'] = labs
                        #all_embeddings = all_embeddings.append(ss.groupby('cell_type').mean().T)
                        type_mean = ss.groupby('cell_type').mean().T
                        type_mean['file'] = embedding_path
                        all_embeddings.append(type_mean)
        pd.concat(all_embeddings).to_csv(os.path.join('data/results/silhouette_samples',dataset+'.csv'))
