#!/usr/bin/python3
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def get_rankings(table_dict,score,methods):
# the results the internal statistics of the embeddings

# It will generate a heatmap of rankings foreach dataset & the internal statistics of the embeddings

    res_dict = dict()
    for key in table_dict.keys():
        res_dict[key] = list() 
        """
        d = table_dict[key]
        lineout=[key]+[d[x][2]+'-'+d[x][1] for x in sorted(table_dict[key].keys())]
        
        print(','.join(lineout))
        """
        #print(key)
        seen = list()
        order = -1
        if score == 'db':
            order = 1
        c = 1

        for i,entry in enumerate(sorted(table_dict[key][score],key = lambda x: order*x[0])):
            if entry[2] not in seen:
                seen.append(entry[2]) 
                entry.append(c)    
                c += 1
                res_dict[key].append(entry)

        for m in methods:
            if m not in seen:
                res_dict[key].append([np.nan,np.nan,m,len(m)])
                
    return res_dict
            

table_dict = dict()

with open('results/csvs/internal_metrics_reduced.csv','r') as fh:
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

        if int(dims) < 2 or int(dims) >= 5000:
            continue
        ch = [float(v[4]),dims,meth]
        db = [float(v[5]),dims,meth]
        di = [float(v[6]),dims,meth]
        ss = [float(v[7]),dims,meth]
      
        if name not in table_dict.keys():
            """
            table_dict[name] = {'ch' : ch,
                                'db' : db, 
                                'di' : di,
                                'ss' : ss}
            """
            table_dict[name] = {'ch' : list(),
                                'db' : list(), 
                                'di' : list(),
                                'ss' : list()}
        else: 
            pass
            """
            table_dict[name]['ch'] = max(ch,table_dict[name]['ch'])
            table_dict[name]['db'] = min(db,table_dict[name]['db'])
            table_dict[name]['di'] = max(ch,table_dict[name]['di'])
            table_dict[name]['ss'] = max(ch,table_dict[name]['ss'])
            """
        table_dict[name]['ch'].append(ch)
        table_dict[name]['db'].append(db)
        table_dict[name]['di'].append(di)
        table_dict[name]['ss'].append(ss)

ss_res = get_rankings(table_dict,sys.argv[1],methods)
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
plt.savefig(os.path.join('results/plots',sys.argv[1]))
