#!/bin/bash

#SBATCH --partition=milano
#SBATCH --job-name=test-psana2-live
#SBATCH --output=output-%j.txt
#SBATCH --error=output-%j.txt
#SBATCH --nodes=2
#SBATCH --ntasks=44
##SBATCH --ntasks-per-node=1 
#SBATCH --exclusive
#SBATCH --time=30:00


t_start=`date +%s`


source setup_hosts.sh
echo SLURM_HOSTFILE $SLURM_HOSTFILE SLURM_NTASKS $SLURM_NTASKS 


export PS_EB_NODES=1
MAX_EVENTS=0
EXP="tmoc00221"
RUNNO=20
XTCDIR="/sdf/data/lcls/drpsrcf/ffb"
mpirun -n 25 ./run_slac.sh $MAX_EVENTS $EXP $RUNNO $XTCDIR


t_end=`date +%s`
echo PSJobCompleted TotalElapsed $((t_end-t_start)) 
