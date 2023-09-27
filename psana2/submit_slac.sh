#!/bin/bash
#SBATCH --partition=anaq
#SBATCH --job-name=psana2
#SBATCH --nodes=7
#SBATCH --ntasks=334
##SBATCH --ntasks-per-node=50
#SBATCH --output=%j.log
#SBATCH --exclusive
 

t_start=`date +%s`


source setup_hosts.sh
echo SLURM_HOSTFILE $SLURM_HOSTFILE SLURM_NTASKS $SLURM_NTASKS 


export PS_EB_NODES=26
export PS_VERBOSITY=1
MAX_EVENTS=0
EXP="tmoc00221"
RUNNO=29
XTCDIR="/cds/data/drpsrcf"
srun ./run_slac.sh $MAX_EVENTS $EXP $RUNNO $XTCDIR


t_end=`date +%s`
echo PSJobCompleted TotalElapsed $((t_end-t_start)) 
