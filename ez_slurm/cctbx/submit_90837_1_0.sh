#!/bin/bash -l
#SBATCH --reservation=exafel2
#SBATCH --account=lcls
#SBATCH --job-name=psauto
#SBATCH --nodes=1
#SBATCH --constraint=knl,quad,cache
#SBATCH --time=00:10:00
#SBATCH --image=docker:monarin/psananersc:latest
t_start=`date +%s`
srun -n 8 -c 32 --cpu_bind=cores shifter ./index_david.sh cxid9114 95 89 lustre
t_end=`date +%s`
echo PSJobCompleted TotalElapsed $((t_end-t_start)) $t_start $t_end
