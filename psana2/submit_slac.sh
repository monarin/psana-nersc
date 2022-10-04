#!/bin/bash
#SBATCH --partition=anaq
#SBATCH --job-name=psana2
#SBATCH --nodes=23
#SBATCH --ntasks=1138
##SBATCH --ntasks-per-node=50
#SBATCH --output=%j.log
#SBATCH --exclusive
 

t_start=`date +%s`


source setup_hosts.sh
echo SLURM_HOSTFILE $SLURM_HOSTFILE SLURM_NTASKS $SLURM_NTASKS 


export PS_EB_NODES=64
MAX_EVENTS=0
srun ./run_slac.sh $MAX_EVENTS


t_end=`date +%s`
echo PSJobCompleted TotalElapsed $((t_end-t_start)) 
