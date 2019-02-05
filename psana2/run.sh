#!/bin/bash
export OMP_PLACES=threads
export OMP_PROC_BIND=spread

OMP_NUM_THREADS=16 srun -N 1 -n 1 -c 64 --cpu_bind=cores python test_mpi.py &
OMP_NUM_THREADS=1 srun -N 1 -n 32 -c 2 --cpu_bind=cores python test_mpi.py
