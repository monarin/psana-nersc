#!/bin/bash -l
#SBATCH --partition=exafel_knl_2
#SBATCH --account=lcls
#SBATCH --job-name=test
#SBATCH --nodes=1
#SBATCH --constraint=knl,quad,cache
#SBATCH --time=00:05:00
t_start=`date +%s`
srun -n 68 -c 4 --cpu_bind=cores ./test.sh
t_end=`date +%s`
echo PSJobCompleted TotalElapsed $((t_end-t_start)) $t_start $t_end
