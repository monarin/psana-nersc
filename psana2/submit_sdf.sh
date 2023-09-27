#!/bin/bash

#SBATCH --partition=milano
#SBATCH --job-name=test-psana2-live
#SBATCH --output=output-%j.txt
#SBATCH --error=output-%j.txt
#SBATCH --nodes=4
#SBATCH --exclusive
#SBATCH --time=10:00


t_start=`date +%s`


source setup_hosts_openmpi.sh


#mpirun -np 287 --hostfile slurm_host_${SLURM_JOB_ID} python test_mpi.py
export PS_EB_NODES=26
export PS_VERBOSITY=0
export PS_ZEROEDBUG_WAIT_SEC=1
MAX_EVENTS=0
EXP="tmoc00221"
RUNNO=34
XTCDIR="/sdf/data/lcls/drpsrcf/ffb"
mpirun -np 287 --hostfile slurm_host_${SLURM_JOB_ID} python test_live.py $EXP $RUNNO $MAX_EVENTS ${XTCDIR}


t_end=`date +%s`
echo PSJobCompleted TotalElapsed $((t_end-t_start)) 
