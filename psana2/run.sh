#!/bin/bash
#export OMP_PLACES=threads
#export OMP_PROC_BIND=spread

#OMP_NUM_THREADS=16 srun -N 1 -n 1 -c 64 --cpu_bind=cores python test_mpi.py &
#OMP_NUM_THREADS=1 srun -N 1 -n 32 -c 2 --cpu_bind=cores python test_mpi.py

# SUMMIT

# Test Smd0
# Need to submit with jsrun --erf_input erf0.txt ./run.sh
# where erf0.txt is
# 1 : {host: 1; cpu: {0-63}}
#export OMP_NUM_THREADS=16
#source $MEMBERWORK/chm137/installation/cctbx/summit/env.sh
#python dev_smd0.py
#strace -ttt -f -o $$.log python dev_smd0.py

#export PS_SMD_NODES=1
export LCLS_CALIB_HTTP=http://login2:6748/calib_ws
python dev_bd.py

#python test_mpi.py

