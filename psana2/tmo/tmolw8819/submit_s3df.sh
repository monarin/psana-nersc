#!/bin/bash
#SBATCH --partition=milano
#SBATCH --job-name=psana2
#SBATCH --nodes=18
#SBATCH --ntasks=2048
##SBATCH --ntasks-per-node=50
#SBATCH --output=%j.log
#SBATCH --exclusive
 

t_start=`date +%s`


source $HOME/lcls2/setup_env.sh
mpirun -n 1 python test_fast_outer_filling.py
mpirun -n 2 python test_fast_outer_filling.py
mpirun -n 4 python test_fast_outer_filling.py
mpirun -n 8 python test_fast_outer_filling.py
mpirun -n 16 python test_fast_outer_filling.py
mpirun -n 32 python test_fast_outer_filling.py
mpirun -n 64 python test_fast_outer_filling.py
mpirun -n 128 python test_fast_outer_filling.py
mpirun -n 256 python test_fast_outer_filling.py
mpirun -n 512 python test_fast_outer_filling.py
mpirun -n 1024 python test_fast_outer_filling.py
mpirun -n 2048 python test_fast_outer_filling.py


t_end=`date +%s`
echo PSJobCompleted TotalElapsed $((t_end-t_start)) 
