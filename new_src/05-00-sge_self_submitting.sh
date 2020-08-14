#!/bin/bash
#PBS -q normal
#PBS -lwalltime=4:00:00
#PBS -v NJOB,JNAME,PROJECT,SPOOL,CPU,MEM
#PBS -l wd
#PBS -lstorage=gdata/ey6
  
# =============================================================================
#  Self resubmitting PBS bash script:
#
#  * Submits a followon job before executing the current job.  The followon 
#    job will be in the "H"eld state until the current job completes
#
#  * Assumes program being run is checkpointing at regular intervals and is
#    able to resume execution from a checkpoint
#
#  * Does not assume the program will complete within the requested time
#
#  * Uses an environment variable (NJOBS) to limit the total number of 
#    resubmissions in the sequence of jobs
#
#  * Allows the early termination of the sequence of jobs - just create/touch
#    the file STOP_SEQUENCE in the jobs working directory.  This may be done 
#    by the executable program when it has completed the "whole" job or by hand 
#    if there is a problem
#
#  * This script may be renamed anything (<15 characters) but if you use the -N 
#    option to qsub you must edit the qsub line below to give the script name 
#    explicitly
#
#  * To use: 
#         - make appropriate changes to the PBS options above and to the 
#           execution and file manipulation lines belo
#         - submit the job with the appropriate value of NJOBS, eg:
#                    qsub -v NJOBS=5 <scriptname>
#
#  * To kill a job sequence, either touch the file STOP_SEQUENCE or qdel
#    the held job followed by the running job
#
#  * To test, try  "sleep 100"  as your executable line
#
# ===============================================================================


ECHO=/bin/echo
workdir="/g/data/ey6/fk5479/scRNA-Dimensionality-Reduction"

#
# These variables are assumed to be set:
#   NJOBS is the total number of jobs in a sequence of jobs (defaults to 1)
#   NJOB is the number of the previous job in the sequence (defaults to 0)
#
  
if [ X$NJOB == X ]; then
    exit
fi

if [ X$JNAME == X ]; then
    exit
fi

if [ X$PROJECT == X ]; then
    exit
fi

if [ X$SPOOL == X ]; then
    exit
fi

if [ X$CPU == X ]; then
    exit
fi

if [ X$MEM == X ]; then
    exit
fi

# Increment the counter to get current job number
#
NJOB=$(($NJOB+1))

#
# Are we in an incomplete job sequence - more jobs to run ?
#
#~#PBS -lmem=4gb
#~#PBS -lncpus=1
queue_dir="${workdir}/data/${SPOOL}/queued"
if [ $(find $queue_dir -type f|wc -l) -gt 0 ]; then
    $ECHO "Submitting job number $NEXTJOB in sequence of $NJOBS jobs"
    qsub -P $PROJECT -lmem=$MEM -lncpus=$CPU -N ${JNAME}-${NJOB} -W depend=afterany:$PBS_JOBID -o ${workdir}/logs/dbscan/${JNAME}-${NJOB}.log -e ${workdir}/logs/dbscan/${JNAME}-${NJOB}.err scripts/self_submitting.sh
fi


#
# Now run the job ...
#

#===================================================
# .... USER INSERTION OF EXECUTABLE LINE HERE 
#===================================================

module load python3/3.7.4

./cluster-pool.sh -w data/${SPOOL} -p ${PBS_JOBID}-${JNAME}-${NJOB} -n 1
