#!/bin/bash

#SBATCH --partition=milano
#SBATCH --job-name=test-psana2-live
#SBATCH --output=output-%j.txt
#SBATCH --error=output-%j.txt
#SBATCH --nodes=4
#SBATCH --ntasks=469
##SBATCH --ntasks-per-node=1 
#SBATCH --exclusive
#SBATCH --time=10:00


t_start=`date +%s`


source setup_hosts.sh
echo SLURM_HOSTFILE $SLURM_HOSTFILE SLURM_NTASKS $SLURM_NTASKS 


export PS_EB_NODES=32
MAX_EVENTS=0
EXP="tstx00817"
RUNNO=63
XTCDIR="/sdf/data/lcls/drpsrcf/ffb"
mpirun -n 385 ./run_slac.sh $MAX_EVENTS $EXP $RUNNO $XTCDIR


t_end=`date +%s`
echo PSJobCompleted TotalElapsed $((t_end-t_start)) 
