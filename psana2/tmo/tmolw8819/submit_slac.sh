#!/bin/bash
#SBATCH --partition=milano
#SBATCH --job-name=psana2
#SBATCH --nodes=20
#SBATCH --ntasks=2500
##SBATCH --ntasks-per-node=50
#SBATCH --output=%j.log
#SBATCH --exclusive
 

t_start=`date +%s`


mpirun -n 2500 python test_fast_outer_filling.py


t_end=`date +%s`
echo PSJobCompleted TotalElapsed $((t_end-t_start)) 
