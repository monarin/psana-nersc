#!/bin/bash

#SBATCH --partition=lcls
#SBATCH --job-name=test-openmpi
#SBATCH --output=output-%j.txt
#SBATCH --error=output-%j.txt
#SBATCH --nodes=2
#SBATCH --ntasks=2
#SBATCH --ntasks-per-node=1 
#SBATCH --exclusive
#SBATCH --time=10:00

srun -n 2 python test_mpi.py

