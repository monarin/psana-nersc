#!/bin/bash -l
#SBATCH --account=m2859
#SBATCH --job-name=psana2
#SBATCH --nodes=1
#SBATCH --constraint=knl,quad,cache
#SBATCH --time=00:10:00
#SBATCH --image=docker:monarin/ps2cctbx:test
#SBATCH --exclusive
#SBATCH --qos=premium

t_start=`date +%s`
export PMI_MMAP_SYNC_WAIT_TIME=600
sbcast -p ./test_read.py /tmp/test_read.py
sbcast -p ./input/pedestals.npy /tmp/pedestals.npy
sbcast -p ./input/gain_mask.pickle /tmp/gain_mask.pickle
t_end_sbcast=`date +%s`
srun -n 68 -c 4 --cpu_bind=cores shifter ./mysetup.sh
t_end=`date +%s`
echo PSJobCompleted sbcast $((t_end_sbcast-t_start)) TotalElapsed $((t_end-t_start))

