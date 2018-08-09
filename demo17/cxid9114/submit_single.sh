#!/bin/bash -l
#SBATCH --account=lcls
#SBATCH --job-name=ps1cctbx
#SBATCH --nodes=1
#SBATCH --constraint=knl,quad,cache
#SBATCH --time=00:10:00
#SBATCH --image=docker:monarin/ps1cctbx:latest
#SBATCH --qos=premium

t_start=`date +%s`
srun -n 8 -c 32 --cpu_bind=cores shifter ./index_single.sh cxid9114 95 0 debug 
t_end=`date +%s`
echo PSJobCompleted TotalElapsed $((t_end-t_start)) $t_start $t_end
