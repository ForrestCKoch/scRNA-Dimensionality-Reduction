#!/usr/bin/python3
import os
import pickle

from sklearn.metrics import calinski_harabaz_score, silhouette_score
import numpy as np

from svr2019.metrics import davies_bouldin_score, dunn_index
from svr2019.datasets import *

import matplotlib.pyplot as plt
import seaborn as sns

from scipy.stats import chi2

def internal_summary(points, labels):
    """
    Generate a summary of internal validation measures.
    Returns a dictionary containing elements:
    - 'calinski-harabaz'
    - 'davies-bouldin'
    - 'dunn-index'
    - 'silhouette-score'
    
    :param points: a numpy array of data points
    :param labels: a numpy array of labels for each point
    """

    labels = np.array(labels)

    calinski_harabaz = calinski_harabaz_score(points, labels)
    #davies_bouldin = davies_bouldin_score(points, labels)
    davies_bouldin = -1
    #di = dunn_index(points, labels)
    di = -1
    silhouette = silhouette_score(points, labels)

    return {
            'calinski-harabaz':calinski_harabaz,
            'davies-bouldin':davies_bouldin,
            'dunn-index':di,
            'silhouette-score':silhouette,
           }


def print_summaries(path_list):
    """
    Print out a comma separated summary for each
    element in the provided list    

    :param path_list: list of paths to embeddings
    """
    head = True
    for path,dataset,labels,exclude in path_list:
        #labels = DuoBenchmark('data/datasets/'+dataset+'.csv').tags 
        with open(path,'rb') as fh:
            embedding = np.load(fh).astype(np.float32)

        embedding = np.delete(embedding,exclude,axis=0)
        labels = np.delete(labels,exclude,axis=0)

        try:
            summary_dict = internal_summary(embedding, labels)
            summary_list = [path]+[str(summary_dict[x]) for x in sorted(summary_dict.keys())]
            if head:
                print(','.join(['path']+sorted(summary_dict.keys())))
                head = False
            print(','.join(summary_list))
        except ValueError:
            pass

def get_table_dict(results_file,lwr_bnd_dims=2,upr_bnd_dims=90):
    """
    Note that due to upr/lwr bounds, 'full' datasets will likely be excluded.
    To work around this format the dimension like '22k' 

    :param results_file: path to results file. Should be a csv in the format
    dataset,method,dimensions,log,vrc,db,di,ss
    however, do not include both log = True/False for the same entry
    :param lwr_bnd_dims: exclude entries with dimensionality below this
    :param upr_bnd_dims: exclude entries with dimensionality above this
    :return: table_dict, method    
    """
    table_dict = dict()
    # organize results into a dictionary
    # Keys are dataset names
    # entries are also dictionaries of the form
    # {'ch':[],'db':[],'di':[],'ss':[]} 
    # Where each list contains entries of [value,method,dimensions]
    with open(results_file,'r') as fh: 
        methods = list()
        header = fh.readline().rstrip('\n')
        for line in fh: 
            # extract our values
            v = line.rstrip('\n').split(',')
            name = v[0]
            meth = v[1]
            dims = v[2]
            if meth not in methods:
                methods.append(meth)

            # The exception we expect to see here is in the case
            # of a dimension formatted like '22k' which will fail
            # integer conversion.  This is used as a convenience to
            # allow for plotting of the heatmaps without too many
            # digits.
            try:
                if int(dims) < lwr_bnd_dims or int(dims) >= upr_bnd_dims:
                    continue
            except:
                pass
            ch = [float(v[4]),dims,meth]
            db = [float(v[5]),dims,meth]
            di = [float(v[6]),dims,meth]
            ss = [float(v[7]),dims,meth]

            if name not in table_dict.keys():
                table_dict[name] = {'ch' : list(),
                                    'db' : list(),
                                    'di' : list(),
                                    'ss' : list()}

            table_dict[name]['ch'].append(ch)
            table_dict[name]['db'].append(db)
            table_dict[name]['di'].append(di)
            table_dict[name]['ss'].append(ss)

    return table_dict,methods

def get_rankings(table_dict,score,methods):
    """
    Obtain the rankings of each method within each dataset according
    to it's performance on 'score'

    :param table_dict: a dictionary of results for methods & datasets 
    provided by get_table_dict
    :param score: one of \{'ch','ss','db','di'\}. the score you wish to
    obtain the ranking over 
    :param methods: methods for which you wish to obtain the ranking over
    """
    res_dict = dict()
    for key in table_dict.keys():
        res_dict[key] = list()
        seen = list()
        order = -1
        if score == 'db':
            order = 1
        c = 1

        for i,entry in enumerate(sorted(table_dict[key][score],key = lambda x: order*x[0])):
            if (entry[2] not in seen) and (entry[2] in methods):
                seen.append(entry[2])
                entry.append(c)
                c += 1
                res_dict[key].append(entry)

        for m in methods:
            if m not in seen:
                res_dict[key].append([np.nan,np.nan,m,len(m)])

    return res_dict

def plot_optimal_heatmap(metric, results_file, methods):
    """
    
    :param metric: one of {'ch','ss','db','di'}
    :param results_file: file of cleaned csv output from print_all.py
    :param methods: methods which should be plotted
    """

    table_dict,_ = get_table_dict(results_file)

    # produce a dictionary of rankings from the table
    # but only for the metric of intrest
    ss_res = get_rankings(table_dict,metric,methods)
    for i in sorted(ss_res.keys()):
        ss_res[i] = sorted(ss_res[i],key = lambda x: x[2])
    data = list()
    annot = list()
    for i in sorted(ss_res.keys()):
        data.append([x[-1] for x in ss_res[i]])
        annot.append([x[1] for x in ss_res[i]])
    annot = np.array(annot)
    ylabs = sorted(ss_res.keys())
    xlabs = sorted([x[2] for x in ss_res['chen']])
    #sns.heatmap(data,xticklabels=xlabs,yticklabels=ylabs,cmap="YlGnBu")
    sns.heatmap(data,xticklabels=xlabs,yticklabels=ylabs,annot=annot,fmt="s")
    plt.tight_layout()
    plt.savefig(os.path.join('results/plots',metric))

def plot_embedding(pickled_file,xd=0,yd=1):
    """
    Do not use... this should probably be removed
    """
    x = pickle.load(open(pickled_file,'rb'))
    plt.scatter(x=x[:,xd],y=x[:,yd],s=0.5)
    plt.show()

def get_concordance(table_dict,methods,score):
    """
    Calculates the concordance of ranking by 'score' across
    each of the datasets in 'table_dict'.  The statistic
    calculated is Kendall's W which asymptotically follows
    a chi-square with n-1 d.o.f where n is the number of methods.
    
    :param table_dict: a dictionary of results for methods & datasets 
    provided by get_table_dict
    :param methods: methods for which you wish to obtain the ranking over
    :param score: one of \{'ch','ss','db','di'\}. the score you wish to
    obtain the ranking over 
    :return: a tuple of (p.value,W)
    """
    n = len(methods)
    ranks = get_rankings(table_dict,score,methods)
    k = len(ranks.keys())

    rank_sums = list()
    for m in methods:
        s = 0
        for d in table_dict.keys():
            idx = [ranks[d][x][2] == m for x in range(0,n)].index(True)
            s += ranks[d][idx][-1]
        rank_sums.append(s)
    
    rank_sums = np.array(rank_sums)
    
    S = np.sum((rank_sums-(k*(n+1)/2))**2)
    W = (12*S)/(k**2*n*(n**2-1))
    Q = W*(n-1)*k
    return chi2.cdf(Q,df=n-1),W

if __name__ == '__main__':
    pass
