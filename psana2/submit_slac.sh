#!/bin/bash
#SBATCH --partition=anaq
#SBATCH --job-name=psana2-test
#SBATCH --nodes=13
#SBATCH --ntasks=577
##SBATCH --ntasks-per-node=50
#SBATCH --output=%j.log
#SBATCH --exclusive
 

t_start=`date +%s`

source setup_hosts.sh
echo SLURM_HOSTFILE $SLURM_HOSTFILE SLURM_NTASKS $SLURM_NTASKS 
srun ./run_slac.sh

#srun -n 339320 -c 4 --cpu_bind=cores -x=nid08201,nid11988 shifter ./index_lite.sh cxid9114 2 99 debug 0
t_end=`date +%s`

echo PSJobCompleted TotalElapsed $((t_end-t_start)) 
