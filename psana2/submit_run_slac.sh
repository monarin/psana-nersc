#!/bin/bash


# Standard job with configurated host list and output written to ffb
SLURM_HOSTFILE=slurm_hosts srun -o log.log --partition=anaq --exclusive ./run_slac.sh


# Randomly allocated-host job
#srun --ntasks 1089 --ntasks-per-node 50 -o $$.log --partition=anaq --exclusive ./run_slac.sh


# For testing prometheus server
#SLURM_HOSTFILE=slurm_hosts srun -o $$.log --partition=anaq --exclusive python test_prometheus_push.py
#srun --ntasks 137 --ntasks-per-node 50 -o $$.log --partition=anaq python test_mpi.py
