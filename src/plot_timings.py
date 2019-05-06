#!/usr/bin/python3
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

if __name__ == '__main__':
    timing_file = 'results/csvs/timings.csv'
    df = pd.read_csv(timing_file)
    df = df.loc[(df.Method != 'mctsn') & (df.Method != 'spectral') & (df.Dataset != 'macosko')]
    df['time'] = ((60*(df.userM+df.sysM))+df.userS+df.sysS)/60


    fig, axes = plt.subplots(len(set(df.Dataset))//2+1, 2, figsize=(10,4))
    plt.subplots_adjust(left=0.125, bottom=0.1, right=0.9, top=0.9, wspace=0.2, hspace=0.5)

    title_dict = {
    'baron-human':' (20k)',
    'campbell':' (26k)',
    'chen':' (23k)',
    'marques':' (23k)',
    'shekhar':' (13k)'
    }
    for i,dataset in enumerate(sorted(set(df.Dataset))):
        bh = df.loc[(df.Dataset == dataset)]
        labels = list()
        lines = list()
        #plt.subplot(len(set(df.Dataset))//2+1,2,i+1)
        curr = axes.flatten()[i]
        curr.set_yscale('log')
        curr.set_title(dataset+title_dict[dataset])
        curr.set_xlabel('dimensions')
        curr.set_ylabel('run time (minutes)')
        for method in sorted(set(bh.Method)):
            subset = bh.loc[(bh.Method == method) & (bh.Dimensions < 100) & (bh.Dimensions > 1)]
            lines.append(curr.plot(subset.Dimensions,subset.time)[0])
            labels.append(method)
        #axes[i].yscale('log')
        #axes[i].yscale('log')

    curr = axes.flatten()[-1]
    curr.set_axis_off()
    fig.suptitle('run time against dimensions for each datset')
    fig.legend(lines, labels,loc=(0.66,0.12),ncol=2)
    plt.show()
