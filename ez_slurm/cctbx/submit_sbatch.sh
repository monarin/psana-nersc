#!/bin/bash -l
#SBATCH --partition=regular
#SBATCH --account=lcls
#SBATCH --qos=premium
#SBATCH --job-name=psauto
#SBATCH --nodes=3
#SBATCH --constraint=knl
#SBATCH --time=02:30:00
#SBATCH --image=docker:monarin/psanatest:latest
t_start=`date +%s`
srun -n 204 -c 4 --cpu_bind=cores shifter ./index.sh cxid9114 108 1 lustre 
t_end=`date +%s`
n_cpus=204
echo N_Cpus $n_cpus
echo PSJobCompleted TotalElapsed $((t_end-t_start)) $t_start $t_end
