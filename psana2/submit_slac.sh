#!/bin/bash
#SBATCH --partition=drpq
#SBATCH --job-name=psana2
#SBATCH --nodes=1
#SBATCH --ntasks=2
#SBATCH --output=%j.log
##SBATCH --exclusive
 

t_start=`date +%s`


#source setup_hosts.sh
#echo SLURM_HOSTFILE $SLURM_HOSTFILE SLURM_NTASKS $SLURM_NTASKS 


#export PS_EB_NODES=26
#export PS_VERBOSITY=1
#MAX_EVENTS=0
#EXP="tmoc00221"
#RUNNO=29
#XTCDIR="/cds/data/drpsrcf"
#srun ./run_slac.sh $MAX_EVENTS $EXP $RUNNO $XTCDIR
srun -n 2 python test_mpi.py


t_end=`date +%s`
echo PSJobCompleted TotalElapsed $((t_end-t_start)) 
