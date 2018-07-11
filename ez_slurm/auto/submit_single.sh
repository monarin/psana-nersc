#!/bin/bash -l
#SBATCH --account=lcls
#SBATCH --job-name=psauto
#SBATCH --nodes=3
#SBATCH --constraint=knl,quad,cache
#SBATCH --time=00:10:00
#SBATCH --image=docker:monarin/psananersc:latest
#SBATCH --qos=premium

t_start=`date +%s`
srun -n 137 -c 4 --cpu_bind=cores shifter /global/cscratch1/sd/monarin/d/psdm/cxi/cxid9114/scratch/mona/psana-nersc/ez_slurm/auto/index.sh cxid9114 96 96 2 lustre None debug 
t_end=`date +%s`
echo PSJobCompleted TotalElapsed $((t_end-t_start)) $t_start $t_end
