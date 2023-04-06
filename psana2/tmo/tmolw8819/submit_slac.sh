#!/bin/bash
#SBATCH --partition=anaq
#SBATCH --job-name=psana2
#SBATCH --nodes=2
#SBATCH --ntasks=100
##SBATCH --ntasks-per-node=50
#SBATCH --output=%j.log
#SBATCH --exclusive
 

t_start=`date +%s`


srun python test_fast_outer_filling.py


t_end=`date +%s`
echo PSJobCompleted TotalElapsed $((t_end-t_start)) 
