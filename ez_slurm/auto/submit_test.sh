#!/bin/bash -l
#SBATCH --reservation=xfeldata
#SBATCH --partition=special
#SBATCH --account=lcls
#SBATCH --job-name=psauto
#SBATCH --nodes=1
#SBATCH --constraint=knl,quad,cache
#SBATCH --time=00:05:00
#SBATCH --image=docker:monarin/psanatest:latest
t_start=`date +%s`
srun -n 1 -c 272 --cpu_bind=cores shifter python testres.py
t_end=`date +%s`
echo PSJobCompleted TotalElapsed $((t_end-t_start)) $t_start $t_end
