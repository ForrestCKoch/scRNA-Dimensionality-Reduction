#!/bin/sh

file="sivm_dinfo.csv"
header=$(head -n1 $file)

IFS=$'\n'
echo $(echo $header|cut -d',' -f1-10),method,score
for line in $(tail -n +2 $file); do
    for i in $(seq 11 43); do
        echo $(echo $line|cut -d',' -f1-10),$(echo $header|cut -d',' -f $i),$(echo $line|cut -d',' -f $i)
    done
done
