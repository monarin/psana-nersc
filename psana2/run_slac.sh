#!/bin/bash
# Usage for this script to employ openmpi with Infinityband
# $/reg/common/package/openmpi/4.0.0-rhel7/bin/mpirun -np 3 --hostfile openmpi_hosts --mca btl_openib_allow_ib 1 run_slac.sh
#source $HOME/lcls2/setup_env.sh
#conda activate ps-1.0.3 # since ps-2.0.0 openmpi is the default mpi sw


# For mpich (run in normal lcls2 env)
# mpirun -n 3 -f host_file ./run_slac.sh


# TAU profile
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

run_psana2_perf() {
    t_start=`date +%s`
    echo "RUN PSANA2 SCRIPT SUBMITTED AT" $t_start 
    export OPENBLAS_NUM_THREADS=1 # preventing blas from openning too many threads?
    python -u ./test_psana2_perf.py
    #python ./test_mpi.py
    t_end=`date +%s`
    echo "PSANA2 JOB COMPLETE AT" $t_end "TOTAL ELAPSED" $((t_end-t_start))
}

run_smd0_perf() {
    echo "RUN SMD0 TEST #FILES=$1"
    python ./dev_smd0.py $1
}

run_psana2_perf

#run_smd0_perf $1
