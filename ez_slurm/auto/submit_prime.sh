#!/bin/bash -l
#SBATCH --partition=regular
#SBATCH --qos=premium
#SBATCH --account=lcls
#SBATCH --job-name=prime
#SBATCH --nodes=10
#SBATCH --constraint=knl,quad,cache
#SBATCH --time=00:15:00
#SBATCH --image=docker:monarin/psananersc:latest
#DW persistentdw name=myBBsml
t_start=`date +%s`
srun -n 680 -c 4 --cpu_bind=cores shifter ./prime.sh cxid9114 0 lustre
t_end=`date +%s`
echo PSJobCompleted TotalElapsed $((t_end-t_start)) $t_start $t_end
