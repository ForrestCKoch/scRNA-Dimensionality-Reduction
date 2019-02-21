#!/usr/bin/python3

import sys

table_dict = dict()

with open('results/csvs/internal_stats_new2.csv','r') as fh:
    header = fh.readline().rstrip('\n')
    for line in fh:
        # extract our values
        v = line.rstrip('\n').split(',')
        name = v[0]
        meth = v[1]
        dims = v[2]

        if int(dims) < 10 or int(dims) >= 10000:
            continue
        ch = (float(v[4]),dims,meth)
        db = (float(v[5]),dims,meth)
        di = (float(v[6]),dims,meth)
        ss = (float(v[7]),dims,meth)
      
        if name not in table_dict.keys():
            table_dict[name] = {'ch' : ch,
                                'db' : db, 
                                'di' : di,
                                'ss' : ss}
        else: 
            table_dict[name]['ch'] = max(ch,table_dict[name]['ch'])
            table_dict[name]['db'] = min(db,table_dict[name]['db'])
            table_dict[name]['di'] = max(ch,table_dict[name]['di'])
            table_dict[name]['ss'] = max(ch,table_dict[name]['ss'])

   
for key in table_dict.keys():

    d = table_dict[key]
    lineout=[key]+[d[x][2]+'-'+d[x][1] for x in sorted(table_dict[key].keys())]
    
    print(','.join(lineout))
