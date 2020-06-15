#!/bin/bash
# Usage for this script to employ openmpi with Infinityband
# $/reg/common/package/openmpi/4.0.0-rhel7/bin/mpirun -np 3 --hostfile openmpi_hosts --mca btl_openib_allow_ib 1 run_slac.sh
#source $HOME/lcls2/setup_env.sh
#conda activate ps-1.0.3 # since ps-2.0.0 openmpi is the default mpi sw

#export TAU_MAKEFILE=/reg/neh/home/monarin/tau-2.28/x86_64/lib/Makefile.tau-ompt-mpi-pdt-openmp
#export PATH=/reg/neh/home/monarin/tau-2.28/x86_64/bin:$PATH
#tau_exec python $HOME/lcls2/psana/psana/tests/dev_eventbuilder.py

#python test_mpi.py
#python dev_bd.py
#python test_send_recv.py

#export PS_SMD_NODES=12
#. "/reg/neh/home/monarin/miniconda3/etc/profile.d/conda.sh"
#conda activate test
#python $HOME/psana-nersc/psana2/test_mpi.py


#export PATH=/reg/neh/home/monarin/tmp/4.0.0-rhel7/bin:$PATH
#export LD_LIBRARY_PATH=/reg/neh/home/monarin/tmp/4.0.0-rhel7/lib
source $HOME/lcls2/setup_env.sh
conda activate ps-3.1.8
#conda activate ps-1.2.2-openmpi
python test_send_recv.py
#python test_mpi.py
#echo $HOSTNAME

#conda activate test
#python test_mpi.py
