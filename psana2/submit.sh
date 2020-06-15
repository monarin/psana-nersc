#!/bin/bash -l
#SBATCH --account=m2859
#SBATCH --job-name=psana2
#SBATCH --nodes=2000
#SBATCH --constraint=knl
#SBATCH --time=00:30:00
#SBATCH --image=docker:slaclcls/lcls2:latest
#SBATCH --exclusive
#SBATCH --qos=premium
#SBATCH --mail-user=monarin@slac.stanford.edu
#SBATCH --mail-type=ALL

t_start=`date +%s`

#export PMI_MMAP_SYNC_WAIT_TIME=600
#./gen_hosts.sh
#export SLURM_HOSTFILE=./hosts

#sbcast ./dev_bd.py /tmp/dev_bd.py
#export PS_SMD_NODES=1

srun -n 136000 -c 4 shifter ./run_nersc.sh

t_end=`date +%s`
echo PSJobCompleted TotalElapsed $((t_end-t_start)) $t_start $t_end
