#!/bin/sh
#PBS -q gpu
#PBS -l ncpus=6
#PBS -l mem=128GB
#PBS -l ngpus=2
#PBS -l wd
#PBS -l walltime=24:00:00
#PBS -P yr31

####################################
# This script is used to run
# src/train_sdae.py on raijin
####################################


####################################
# Fixup our environment as necessary
####################################

# Add our special little module folder
module use $HOME/modules

# Remove some modules
module unload gcc
module unload intel-fc intel-cc
#module unload intel-mkl

# And add a few in
#module load intel-mkl
module load gcc/6.2.0
module load python3/3.6.7-gcc620
module load hdf5/1.10.0
# CUDA
module load cuda/10.0
module load cudnn/7.4.2-cuda10.0 # From $HOME/modules

# Force gcc/6.2.0 libraries loading 
export LD_PRELOAD=/apps/gcc/6.2.0/lib64/libstdc++.so.6
# Ensure packages in the home directory are given preference
export PYTHONPATH="/short/ey6/fk5479/local/lib/python3.6/site-packages":$PYTHONPATH

# and run ...
CUDA_VISIBLE_DEVICES=0 python3 -u src/train_sdae.py $args0 > $logs0 2>&1 &
CUDA_VISIBLE_DEVICES=1 python3 -u src/train_sdae.py $args1 > $logs1 2>&1 &

wait
