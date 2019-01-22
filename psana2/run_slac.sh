#!/bin/bash
# Usage for this script to employ openmpi with Infinityband
# $/reg/g/psdm/sw/conda2/inst/envs/ps-1.0.3/bin/mpirun -np 2 --hostfile openmpi_hosts --mca btl_openib_allow_ib 1 run_slac.sh
source $HOME/lcls2/setup_env.sh
conda activate ps-1.0.3

#export TAU_MAKEFILE=/reg/neh/home/monarin/tau-2.28/x86_64/lib/Makefile.tau-ompt-mpi-pdt-openmp
#export PATH=/reg/neh/home/monarin/tau-2.28/x86_64/bin:$PATH
#tau_exec python $HOME/lcls2/psana/psana/tests/dev_eventbuilder.py

python test_mpi.py

#export PS_SMD_NODES=2
#python $HOME/lcls2/psana/psana/tests/dev_bd.py
