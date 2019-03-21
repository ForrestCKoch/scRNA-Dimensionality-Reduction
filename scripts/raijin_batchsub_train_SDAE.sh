#!/bin/sh


#for dataset in "koh" "kumar" "simk4easy" "simk4hard" "simk8hard" "zhengmix8eq" "zhengmix4eq"; do
#for dataset in "simk4easy" "simk4hard" "simk8hard"; do
#for dataset in "kumar"; do
for dataset in "zhengmix4eq" "zhengmix8eq"; do

        # --log and ' '
        for log in ' ' '--log'; do
            if [ "$log" == "--log" ]; then
                flag='true'
            else
                flag='false'
            fi

        # --scale and ' '
        for scale in ' ' '--scale'; do
            if [ "$scale" == "--scale" ]; then
                sflag='true'
            else
                sflag='false'
            fi

        # adjust looping delimiter
set -f              # turn off globbing
IFS='
'            # split at newlines only
                for dims in $(cat 'scripts/target_seqs/decay2.csv'|grep $dataset|cut -d',' -f2-|tr ',' '\n');do
                #for log in '--log' ' '; do

                    dlabs=$(echo $dims|tr ' ' '-'|sed 's/"//g')
                    logfile="logs/$dataset/decay-2_bs-64_pt-500_t-1000_plr-1_tlr-01_lrstep-985_log-${flag}_scale-${sflag}_dims-${dlabs}"
                    a="--dataset $dataset --batch-size 64 --pretrain-epochs 500 --train-epochs 1000 --layers $(echo $dims|sed 's/"//g')  --lr-step 0.985 $log $scale"
                    qsub -N SDAE-$dataset -o ${logfile}.out -e ${logfile}.err -v args="$a" scripts/raijin_train_SDAE.sh

                done
        unset IFS
        set +f
    done
    done
done
