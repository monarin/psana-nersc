#!/bin/bash
#SBATCH --partition=anaq
#SBATCH --job-name=psana2-test
#SBATCH --nodes=2
#SBATCH --ntasks=4
##SBATCH --ntasks-per-node=50
#SBATCH --output=%j.log
#SBATCH --exclusive
 

t_start=`date +%s`

source setup_hosts.sh
echo SLURM_HOSTFILE $SLURM_HOSTFILE SLURM_NTASKS $SLURM_NTASKS 
srun ./run_slac.sh

t_end=`date +%s`

echo PSJobCompleted TotalElapsed $((t_end-t_start)) 
