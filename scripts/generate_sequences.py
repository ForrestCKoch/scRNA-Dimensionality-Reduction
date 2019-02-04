#!/usr/bin/python3


TARGETS = [5,10,25,50,100,250,500,1000,2500,5000,10000,15000]
DECAY=5

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
        
    
