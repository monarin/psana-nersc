#!/bin/bash -l
#SBATCH --account=m2859
#SBATCH --qos=priority
#SBATCH --job-name=psana2-perf
#SBATCH --nodes=1
#SBATCH --constraint=knl,quad,cache
#SBATCH --time=00:15:00
#SBATCH --exclusive


t_start=`date +%s`


srun -n 68 -c 4 --cpu_bind=cores python $HOME/psana-nersc/psana2/test_mpi.py 


t_end=`date +%s`


echo PSJobCompleted TotalElapsed $((t_end-t_start)) 
