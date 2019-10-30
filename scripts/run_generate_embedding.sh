#!/bin/sh

module load python/3.6.6
#!/bin/sh
###############################################################################
# run_generate_embedding.sh
# 
# a wrapper script around generate_embedding.py inteded to be use for 
# job submission
###############################################################################
/usr/bin/time -v python3 src/generate_embedding.py --dataset $dataset --method $method --outdir $outdir --trial-name $name --dims $dims --njobs $njobs
