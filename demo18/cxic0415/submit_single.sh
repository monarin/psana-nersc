#!/bin/bash -l
#SBATCH --account=lcls
#SBATCH --job-name=ps2cctbx
#SBATCH --nodes=250
#SBATCH --constraint=knl,quad,cache
#SBATCH --time=00:20:00
#SBATCH --image=docker:monarin/ps2cctbx:latest
#SBATCH --qos=premium

t_start=`date +%s`

srun -N 250 -n 250 cp ./xtc_process.py ./input/process_batch.phil ./input/mask.pickle ./input/pedestals.npy ./input/metro.pickle ./input/gain_mask.pickle /tmp/
srun -N 250 -n 250 mkdir -p /tmp/output/discovery/dials/r0001/000/out /tmp/output/discovery/dials/r0001/000/stdout /tmp/output/discovery/dials/r0001/000/tmp
srun -n 17000 -c 4 --cpu_bind=cores shifter ./index_single.sh cxic0415 1 0 debug
t_end=`date +%s`
echo PSJobCompleted TotalElapsed $((t_end-t_start)) $t_start $t_end
