#!/bin/bash -l
#SBATCH --partition=regular
#SBATCH --qos=premium
#SBATCH --account=lcls
#SBATCH --job-name=psauto
#SBATCH --nodes=1
#SBATCH --constraint=knl,quad,cache
#SBATCH --time=00:20:00
#SBATCH --image=docker:monarin/psanatest:latest
#DW persistentdw name=myBBsml
t_start=`date +%s`
srun -n 2 -c 136 --cpu_bind=cores shifter /global/cscratch1/sd/monarin/d/psdm/cxi/cxid9114/scratch/mona/psana-nersc/ez_slurm/auto/index.sh cxid9114 98 98 10 BB myBBsml 
t_end=`date +%s`
n_cpus=2
echo N_Cpus $n_cpus
t_submit 1506025075
echo PSJobCompleted TotalElapsed $((t_end-t_start)) $t_start $t_end
