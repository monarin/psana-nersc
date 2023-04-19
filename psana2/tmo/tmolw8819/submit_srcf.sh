#!/bin/bash
#SBATCH --partition=anaq
#SBATCH --job-name=psana2
#SBATCH --nodes=18
#SBATCH --ntasks=1024
##SBATCH --ntasks-per-node=50
#SBATCH --output=%j.log
#SBATCH --exclusive
 

t_start=`date +%s`


# include pytorch manually
export PYTHONPATH=$PYTHONPATH:/cds/home/m/monarin/sw/pytorch

srun -N 1 -n 1 python test_fast_outer_filling.py
srun -N 1 -n 2 python test_fast_outer_filling.py
srun -N 1 -n 4 python test_fast_outer_filling.py
srun -N 1 -n 8 python test_fast_outer_filling.py
srun -N 1 -n 16 python test_fast_outer_filling.py
srun -N 1 -n 32 python test_fast_outer_filling.py
srun -N 2 -n 64 python test_fast_outer_filling.py
srun -N 3 -n 128 python test_fast_outer_filling.py
srun -N 5 -n 256 python test_fast_outer_filling.py
srun -N 9 -n 512 python test_fast_outer_filling.py
srun -N 18 -n 1024 python test_fast_outer_filling.py


t_end=`date +%s`
echo PSJobCompleted TotalElapsed $((t_end-t_start)) 
