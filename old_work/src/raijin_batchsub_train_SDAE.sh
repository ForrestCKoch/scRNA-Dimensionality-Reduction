#!/bin/sh

# This script is used to submit jobs to the queue at Raijin.
# generate_sequences.py should have been called prior to running this script
# and the output stored in scripts/target_seqs/decay?.csv where ? is the decay rate

# All datasets we want to run
#for dataset in "koh" "kumar" "simk4easy" "simk4hard" "simk8hard" "zhengmix8eq" "zhengmix4eq"; do
alt_flag=0
for dataset in "campbell" "baron-human" "chen" "macosko" "marques" "shekhar"; do

    #######################
    # handle log/scale options
    #######################
    log="--log1p"
    flag='true'

    scale='--scale'
    sflag='true'

        # adjust looping delimiter
set -f              # turn off globbing
IFS='
'            # split at newlines only
    for dims in $(cat 'scripts/target_seqs/decay4.csv'|grep $dataset|cut -d',' -f2-|tr ',' '\n');do

        # In order to submit 2 jobs at a time, we need to alternate between states
        if [[ $alt_flag -eq 0 ]]; then
            dlabs=$(echo $dims|tr ' ' '-'|sed 's/"//g')
            mkdir -p "logs/$dataset/"

            l0="logs/$dataset/decay-4_bs-64_pt-250_t-250_plr-1_tlr-01_lrstep-985_log-${flag}_scale-${sflag}_dims-${dlabs}"
            a0="--dataset $dataset --batch-size 64 --pretrain-epochs 250 --train-epochs 250 --layers $(echo $dims|sed 's/"//g')  --lr-step 0.985 $log $scale"
            alt_flag=1
        else
            dlabs=$(echo $dims|tr ' ' '-'|sed 's/"//g')
            mkdir -p "logs/$dataset/"

            l1="logs/$dataset/decay-4_bs-64_pt-250_t-250_plr-1_tlr-01_lrstep-985_log-${flag}_scale-${sflag}_dims-${dlabs}"
            a1="--dataset $dataset --batch-size 64 --pretrain-epochs 250 --train-epochs 250 --layers $(echo $dims|sed 's/"//g')  --lr-step 0.985 $log $scale"
            alt_flag=0
        
            # Submit a job with every other loop
            qsub -N SDAE-$dataset -o logs/stdout.txt -e logs/stderr.txt -v args0="$a0",args1="$a1",logs0="$l0",logs1="$l1" scripts/raijin_train_SDAE.sh
        fi

    done
    unset IFS
    set +f
done
