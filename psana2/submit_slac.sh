#!/bin/bash
#SBATCH --partition=anaq
#SBATCH --job-name=psana2
#SBATCH --nodes=9
#SBATCH --ntasks=396
##SBATCH --ntasks-per-node=50
#SBATCH --output=%j.log
#SBATCH --exclusive
 

t_start=`date +%s`


source setup_hosts.sh
echo SLURM_HOSTFILE $SLURM_HOSTFILE SLURM_NTASKS $SLURM_NTASKS 


export PS_EB_NODES=32
MAX_EVENTS=0
EXP="tstx00817"
RUNNO=59
srun ./run_slac.sh $MAX_EVENTS $EXP $RUNNO


t_end=`date +%s`
echo PSJobCompleted TotalElapsed $((t_end-t_start)) 
