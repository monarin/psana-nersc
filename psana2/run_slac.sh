#!/bin/bash
# Usage for this script to employ openmpi with Infinityband
# $/reg/common/package/openmpi/4.0.0-rhel7/bin/mpirun -np 3 --hostfile openmpi_hosts --mca btl_openib_allow_ib 1 run_slac.sh
#source $HOME/lcls2/setup_env.sh
#conda activate ps-1.0.3 # since ps-2.0.0 openmpi is the default mpi sw
#export PATH=/reg/neh/home/monarin/tmp/4.0.0-rhel7/bin:$PATH
#export LD_LIBRARY_PATH=/reg/neh/home/monarin/tmp/4.0.0-rhel7/lib


# Usage for mpich (run in normal lcls2 env)
# mpirun -n 3 -f host_file ./run_slac.sh


# Usage for TAU profile
#export TAU_MAKEFILE=/reg/neh/home/monarin/tau-2.28/x86_64/lib/Makefile.tau-ompt-mpi-pdt-openmp
#export PATH=/reg/neh/home/monarin/tau-2.28/x86_64/bin:$PATH
#tau_exec python $HOME/lcls2/psana/psana/tests/dev_eventbuilder.py


# Usage for submit as psana2-style (SMD0 on single node) on srcf
# Update --nodes and --ntasks in submit_slac.sh
# Run sbatch submit_slac.sh
# See ref. no in https://docs.google.com/spreadsheets/d/111exVHQH_zOTYJYSl6XrYtj22Z-jqC0YZg847kaVt_8/edit?usp=sharing


t_start=`date +%s`
echo "RUN PSANA2 SCRIPT SUBMITTED AT" $t_start 

# For psana2
export PS_R_MAX_RETRIES=60
export PS_SMD_N_EVENTS=10000
export PS_FAKESTEP_FLAG=0
export PS_SMD0_NUM_THREADS=32
# For amo06516 (Exafel SPI data)
#export PS_SMD_CHUNKSIZE=32000000
#source $HOME/lcls2/setup_env.sh

# Preventing blas from openning too many threads?
#export OPENBLAS_NUM_THREADS=1 

# For openmpi
#export OMPI_MCA_btl=self,tcp,vader
export OMPI_MCA_btl_tcp_if_include=172.21.164.90/1072
#ompi_info --param btl all --level 9

#python -u ./dummy.py
MAX_EVENTS=${1}
EXP=${2}
RUNNO=${3}
#python -u ${HOME}/psana-nersc/psana2/test_psana2_perf.py $MAX_EVENTS
python -u ${HOME}/psana-nersc/psana2/test_live.py $EXP $RUNNO
#python -u ${HOME}/problems/tdd14/preproc.py 406
#python -u ./test_fex_cfd1.py
#python -u ./test_mpi.py
#python -u ./test_live.py
#python -u ./test_prometheus_monitor.py

# test Roentdek algorithm 
# input args: 
#   1 MODE (1=READ, 2=PEAKFINDING, 3=ROENTDEK, 4=WRITE)
#   2 max_events
#   3 n_dets 
#   4 ROENTDEK algorithm ('dldproc', 'hitfinder')
#export PS_EB_NODES=1
#export PS_SRV_NODES=$PS_EB_NODES
#python -u ./test_roentdek.py 1 25600000 2 hitfinder

t_end=`date +%s`
echo "PSANA2 JOB COMPLETE AT" $t_end "TOTAL ELAPSED" $((t_end-t_start)) "N_TASKS" $SLURM_NTASKS


#echo "RUN SMD0 TEST"
#source $HOME/lcls2/setup_env.sh
#python ./dev_smd0.py 60

