#!/bin/bash -l
#SBATCH --account=m2859
#SBATCH --job-name=psana2
#SBATCH --nodes=2
#SBATCH --constraint=knl,quad,cache
#SBATCH --time=00:10:00
#SBATCH --image=docker:monarin/ps2cctbx:latest
#SBATCH --qos=premium

t_start=`date +%s`
export PMI_MMAP_SYNC_WAIT_TIME=600
time srun -N 1000 -n 1000 cp ./test.py /tmp/
time srun -n 136 -c 4 --cpu_bind=cores shifter ./mysetup.sh
#srun -n 68000 -c 4 --cpu_bind=cores shifter ./test.sh  
t_end=`date +%s`
echo PSJobCompleted TotalElapsed $((t_end-t_start)) $t_start $t_end

