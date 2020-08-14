#!/bin/sh

echo "dataset,count_type,method,dimensions,seconds,memory"
for file in $(find data/embeddings/ -type f -name '*.log'); do

    ds=$(echo $file|cut -d'/' -f3) 
    c=$(echo $file|cut -d'/' -f4) 
    m=$(echo $file|cut -d'/' -f5) 
    d=$(echo $file|cut -d'/' -f7|cut -d'.' -f1) 

    seconds=$(cat $file|egrep -o 'Completed empedding in [0-9]*\.[0-9]+ seconds'|cut -d' ' -f4)
    maxmem=$(cat $file|egrep 'Maximum resident set size'|cut -d':' -f2|sed 's/^ //')

    echo $ds,$c,$m,$d,$seconds,$maxmem

done
