#!/bin/bash
#SBATCH --partition=anaq
#SBATCH --job-name=psana2
#SBATCH --nodes=12
#SBATCH --ntasks=594
##SBATCH --ntasks-per-node=50
#SBATCH --output=/cds/data/drpsrcf/users/monarin/log/%j.log
#SBATCH --exclusive
 

t_start=`date +%s`

source setup_hosts.sh
echo SLURM_HOSTFILE $SLURM_HOSTFILE SLURM_NTASKS $SLURM_NTASKS 
srun ./run_slac.sh

t_end=`date +%s`

echo PSJobCompleted TotalElapsed $((t_end-t_start)) 
