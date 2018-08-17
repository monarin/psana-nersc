#!/bin/bash -l
#SBATCH --account=lcls
#SBATCH --job-name=ps2cctbx
#SBATCH --nodes=100
#SBATCH --constraint=knl,quad,cache
#SBATCH --time=01:30:00
#SBATCH --image=docker:monarin/ps2cctbx:test
#SBATCH --qos=premium

t_start=`date +%s`

srun -N 100 -n 100 cp ./xtc_process.py ./input/process_batch.phil ./input/mask.pickle ./input/pedestals.npy ./input/metro.pickle ./input/gain_mask.pickle /tmp/
#srun -N 100 -n 100 mkdir -p /tmp/output/discovery/dials/r0001/000/out /tmp/output/discovery/dials/r0001/000/stdout /tmp/output/discovery/dials/r0001/000/tmp
srun -n 6800 -c 4 --cpu_bind=cores shifter ./index_new.sh cxic0415 1 0 debug
t_end=`date +%s`
echo PSJobCompleted TotalElapsed $((t_end-t_start)) $t_start $t_end
