#!/bin/bash -l
#SBATCH --account=m2859
#SBATCH --job-name=psana2
#SBATCH --nodes=1
#SBATCH --constraint=knl
#SBATCH --time=00:15:00
#SBATCH --image=docker:slaclcls/lcls-py2:latest
#SBATCH --exclusive
#SBATCH --qos=premium

t_start=`date +%s`

export PMI_MMAP_SYNC_WAIT_TIME=600

srun -n 68 -c 4 shifter ./run_nersc.sh

t_end=`date +%s`
echo PSJobCompleted TotalElapsed $((t_end-t_start)) $t_start $t_end
