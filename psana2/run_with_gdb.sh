#!/bin/bash

mpirun -n 2 xterm -e gdb -ex r --args python test_mpi.py
