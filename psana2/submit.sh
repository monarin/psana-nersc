#!/bin/bash -l
#SBATCH --account=m2859
#SBATCH --job-name=psana2
#SBATCH --nodes=1
#SBATCH --constraint=haswell
#SBATCH --time=00:10:00
#SBATCH --image=docker:monarin/psana2:latest
#SBATCH --exclusive
#SBATCH --qos=premium

t_start=`date +%s`

export PMI_MMAP_SYNC_WAIT_TIME=600
./gen_hosts.sh


srun -n 32 -c 2 --cpu_bind=cores python /global/cscratch1/sd/monarin/sw/lcls2/psana/psana/tests/dev_eventbuilder.py
t_end=`date +%s`
echo PSJobCompleted TotalElapsed $((t_end-t_start)) $t_start $t_end
