#!/usr/bin/python

from svr2019.datasets import *
from svr2019.sumarize import *
import os


path_list = list()
for dataset in os.listdir('data/embeddings/'):
#    labels = DuoBenchmark('data/datasets/'+dataset+'.csv').tags
    for reduction in os.listdir('data/embeddings/'+dataset):
        for item in os.listdir('data/embeddings/'+dataset+'/'+reduction):
            path_list.append((os.path.join('data/embeddings/',dataset,reduction,item),dataset))

print_summaries(path_list)
