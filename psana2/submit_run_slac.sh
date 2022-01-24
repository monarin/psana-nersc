#!/bin/bash
SLURM_HOSTFILE=slurm_hosts srun -o $$.log --partition=anaq --exclusive ./run_slac.sh
#srun --ntasks 1089 --ntasks-per-node 50 -o $$.log --partition=anaq --exclusive ./run_slac.sh
