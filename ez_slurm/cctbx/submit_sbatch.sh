#!/bin/bash -l
#SBATCH --partition=realtime
#SBATCH --account=lcls
#SBATCH --job-name=psauto
#SBATCH --nodes=1
#SBATCH --constraint=haswell
#SBATCH --time=00:05:00
t_start=`date +%s`
srun -n 32 -c 2 --cpu_bind=cores shifter --image=docker:monarin/psanatest:latest python test.py
t_end=`date +%s`
echo PSJobCompleted TotalElapsed $((t_end-t_start)) $t_start $t_end
