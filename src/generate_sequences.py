#!/usr/bin/python3
# This script is intended to be used to generate sequences
# indicating the size of each hidden layer to be trained in the SDAE

# Target dimension(s)
TARGETS = [2,3,4,5,10,25,50,100,250,500,1000,2500]
# Factor for the geometric series.  The size of the next layer is floor(current/DECAY)
DECAY=5

# Datatset names and their dimensions.  This should probably be automated by directly
# inspecting the csv
dimensions={'koh':48981,'kumar':45159,
            'simk4easy':43606,'simk4hard':43638,'simk8hard':43601,
            'zhengmix4eq':15568,'zhengmix8eq':15716}

if __name__ == '__main__':
    for key in dimensions.keys():
        seqs = list()
        for t in TARGETS:
            trial = list()
            curr = dimensions[key] // DECAY
            while(curr > t):
                trial.append(str(curr))
                curr = curr // DECAY
            trial.append(str(t))
            seqs.append(trial)
        print(','.join([key]+['"'+" ".join([x for x in s])+'"' for s in seqs]))
        
    
