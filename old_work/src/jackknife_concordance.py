#!/usr/bin/env/python3
##############################################################
# jackknife_concordance.py
# 
# Description:
#   This script calculates a jacknife estimate of the
#   variance of concordance.
##############################################################

from svr2019.sumarize import *
import sys

for metric in ['ss','ch','db','di']:

    d,m = get_table_dict("results/csvs/internal_metrics_reduced.csv")
    jk = list()
    for k in d.keys():
        l = list(d.keys())
        l.remove(k)
        nd = {j:d[j] for j in l}
        jk.append(get_concordance(nd,m,metric)[1])

    n = len(jk)
    mu = np.mean(jk)
    v = ((n-1)/n)*np.sum((np.array(jk)-mu)**2)

    print("For "+metric+":")
    print("\tMean: "+str(mu))
    print("\tVar: " +str(v))


