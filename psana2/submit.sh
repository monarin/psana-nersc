#!/bin/bash -l
#SBATCH --account=m2859
#SBATCH --job-name=psana2
#SBATCH --nodes=7
#SBATCH --constraint=haswell
#SBATCH --time=00:20:00
#SBATCH --image=docker:monarin/psana2:latest
#SBATCH --exclusive
#SBATCH --qos=premium
#DW persistentdw name=psana2_hsd

t_start=`date +%s`

export PMI_MMAP_SYNC_WAIT_TIME=600
./gen_hosts.sh
export SLURM_HOSTFILE=./hosts

sbcast ./dev_bd.py /tmp/dev_bd.py
export PS_SMD_NODES=32
srun -n 193 shifter python /tmp/dev_bd.py
t_end=`date +%s`
echo PSJobCompleted TotalElapsed $((t_end-t_start)) $t_start $t_end
