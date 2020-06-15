#!/bin/bash
#SLURM_HOSTFILE=./hosts srun -N 3 -n 61 python dev_eventbuilder.py
strace -ttt -f -o $$.log python -c "a=0"
