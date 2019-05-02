#!/bin/sh
#PBS -l wd
#PBS -o mouse-15kpca.out
#PBS -e mouse-15kpca.err
#PBS -q hugemem
#PBS -l mem=1TB
#PBS -l ncpus=7
#PBS -P yr31
#PBS -l walltime=96:00:00

module unload gcc
module unload intel-fc intel-cc
module unload intel-mkl/17.0.1.132
module load gcc/6.2.0
module load python3/3.6.7-gcc620
module load pytorch/0.5.0a0-py36
module load hdf5/1.10.0

export LD_PRELOAD=/apps/gcc/6.2.0/lib64/libstdc++.so.6
export PYTHONPATH="/home/561/fk5479/.local/lib/python3.6/site-packages":$PYTHONPATH
#echo $LD_LIBRARY_PATH
#export LD_LIBRARY_PATH=/apps/gcc/6.2.0/lib64:/apps/gcc/6.2.0/lib:$LD_LIBRARY_PATH

#env

python3 src/generate_embedding.py --dims 15000 --njobs 7 --method pca --npoints -1 --dataset mouse
