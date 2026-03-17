#!/bin/bash
#SBATCH -A m1759
#SBATCH -C gpu
#SBATCH -q regular
#SBATCH -t 1:00:00
#SBATCH -n 4
#SBATCH --ntasks-per-node=4
#SBATCH -c 10
#SBATCH --gpus-per-task=1

export SLURM_CPU_BIND="cores"
srun python $HOME/psana-nersc/psana2/test_mpi.py 
