#!/usr/bin/python3
import os
import sys
import pickle

import numpy as np

import matplotlib as mpl
#mpl.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

from scipy.stats import spearmanr

from sklearn.metrics import pairwise_distances

from svr2019.datasets import *
from svr2019.sumarize import *

def reject_outliers(data, m=5):
    mu = np.mean(data)
    sd = np.std(data)
    return data[abs(data - mu) < m * sd]

def trim_data(data, m=0.5):
    intvl = np.percentile(data,[m,100-m])
    return data[(data >= intvl[0]) & (data <= intvl[1])]

color_dict=dict()
for j in range(0,11):
    i = j*13%10
    x = (i/10)
    y = (1-x)/2
    z = 1- (x**2 + y**2)
    color_dict[j] = [x,y,z]

if __name__ == '__main__':
    table_dict,methods = get_table_dict('results/csvs/internal_metrics_reduced.csv')

    ss_res = get_rankings(table_dict,'ss',methods)

    n_meth = len(methods) - 1
    n_data = len(ss_res.keys())
    count = 1

    plt.rcParams["figure.figsize"] = (8,11)
    first_row=True
    for dataset in ss_res.keys():
        print(dataset)
        #ds = DuoBenchmark('data/datasets/'+dataset+'.csv',split_head=False)
        #raw_data = ds.data
        #pw_raw = pairwise_distances(raw_data)
        first_col=True
        colour = 1
        for i,entry in enumerate(sorted(ss_res[dataset],key = lambda x:x[2])):
            method = entry[2]
            dims = entry[1]
            if method == 'full':
                continue
            if method == 'sdae':
                emb_file = 'data/embeddings/'+dataset+'/'+method+'/'+dims+'-log-True.pickle'
            else:
                emb_file = 'data/embeddings/'+dataset+'/'+method+'/'+dims+'-log-False.pickle'
            with open(emb_file,'rb') as fh:
                emb_data = pickle.load(fh)
    #        pw_emb = pairwise_distances(emb_data).flatten()
            
            plt.subplot(n_data,n_meth+1,count)
            count += 1
            r = np.random.randn(100,100).flatten()
            hist = plt.hist(trim_data(r),bins='scott',color=color_dict[i])
            yl,yh = plt.ylim()
            plt.ylim((yl,yh*1.1))
            xl,xh = plt.xlim()
    #        hist = plt.hist(reject_outliers(pw_emb),bins='scott')
    #        hist = plt.hist(trim_data(pw_emb),bins='scott')
            # remove our ticks and labels
            plt.xticks(ticks=[],labels=[])
            # add the dataset to the first column
            p = hist[0]
            if first_col:
                plt.yticks(ticks=[np.max(p)/2],labels=[dataset])
                first_col=False
            else:
                plt.yticks(ticks=[],labels=[])
            # add titles only to the first row
            if first_row:
                plt.title(method)

        
    #        scor = np.mean([spearmanr(pw_emb[i],pw_raw[i]).correlation for i in range(0,len(pw_emb))])
            scor = 3.143452345
            plt.text(xl,.95*yh,' r = {:.2f}'.format(scor),fontsize=8)
            #print('\t'+method+' : '+str(scor))
            print('\t'+method)

        # and then plot the histogram 
        plt.subplot(n_data,n_meth+1,count)
        count += 1
        r = np.random.randn(100,100).flatten()
        hist = plt.hist(trim_data(r),bins='scott',color=[0,1,0])
        plt.xticks(ticks=[],labels=[])
        plt.yticks(ticks=[],labels=[])
        if first_row:
            plt.title('Original')


        first_row = False
            
    #plt.savefig('test.pdf') 
    plt.show(block=True)
