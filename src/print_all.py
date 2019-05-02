#!/usr/bin/python

from svr2019.datasets import *
from svr2019.sumarize import *
from sklearn.preprocessing import LabelEncoder
import os


path_list = list()
#dataset_list = ['campbell','chen','shekhar']
dataset_list = ['baron-human']

#bad_types = ['"unknown"','"miss"','"zothers"',]
bad_types = ['"acinar"','"activated_stellate"','"alpha"','"beta"','"delta"','"ductal"','"endothelial"','"gamma"','"quiescent_stellate"'
]
#for dataset in os.listdir('data/embeddings/'):
#for dataset in ['koh']:
for dataset in dataset_list:
    with open('data/datasets/'+dataset+'.csv','r') as fh:
        cell_types = fh.readline().rstrip('\n').split(',')

    le = LabelEncoder()
    le.fit(cell_types)
    labels = le.transform(cell_types)
    
    # look for bad classes that we want to remove
    exclude = list()
    for x in bad_types:
        if x in le.classes_:
            for i,y in enumerate(cell_types):
                if y == x:
                    exclude.append(i)
    
    for reduction in os.listdir('data/embeddings/'+dataset):
        for item in os.listdir('data/embeddings/'+dataset+'/'+reduction):
            path_list.append((os.path.join('data/embeddings/',dataset,reduction,item),dataset,labels,exclude))
print('hi')
print_summaries(path_list)

exit()
#for dataset in os.listdir('data/embeddings/'):
for dataset in dataset_list:
    ds = DuoBenchmark('data/datasets/'+dataset+'.csv',log_trans=False,split_head=False)
    labels = ds.tags
    points = ds.data

    exclude = list()
    for x in bad_types:
        if x in le.classes_:
            for i,y in enumerate(cell_types):
                if y == x:
                    exclude.append(i)

    embedding = np.delete(embedding,exclude,axis=0)
    points = np.delete(points,exclude,axis=0)

    summary_dict = internal_summary(points, labels)
    print(','.join([dataset] + [str(summary_dict[x]) for x in sorted(summary_dict.keys())]))
