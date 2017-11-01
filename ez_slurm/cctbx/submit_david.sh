#!/bin/bash -l

#SBATCH --nodes=1
#SBATCH --ntasks=32
#SBATCH --time=00:05:00
#SBATCH --partition=realtime
#SBATCH --account=lcls
#SBATCH --job-name=wf-merge
#SBATCH --output=wf-merge.out
#SBATCH --error=wf-merge.error
#SBATCH --constraint=haswell

echo "Works"

