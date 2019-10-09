for line in $(cat sdae_filtered_nodup.csv); do
    echo $(echo $line|cut -d'/' -f3),sdae,$(echo $line|cut -d'_' -f2|rev|cut -d'-' -f1|rev),$(echo $line|cut -d'_' -f8|cut -d'-' -f2),$(echo $line|cut -d',' -f2-)
done > sdae_formatted.csv
