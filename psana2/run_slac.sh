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


. $HOME/tmp/client_bash/prometheus.bash

export PROMETHEUS_GATEWAY=psdm03:9091

io::prometheus::NewGauge name=psana_start_time help='time_t when cron job last started' \
           labels=jobid,rank
psana_start_time -jobid=$$ -rank=0 set $(date +'%s.%N')
io::prometheus::PushAdd job=psana_pushgateway instance=$HOSTNAME gateway=$PROMETHEUS_GATEWAY


source $HOME/lcls2/setup_env.sh
#export PS_SMD_NODES=20
/reg/g/psdm/sw/conda2/inst/envs/ps-3.1.16/bin/mpirun -n 40 --hostfile openmpi_hosts --mca btl_openib_allow_ib 1 ./run_with_prometheus.sh

io::prometheus::NewGauge name=psana_end_time help='time_t when cron job last ended' \
           labels=jobid,rank
psana_end_time -jobid=$$ -rank=0 set $(date +'%s.%N')
io::prometheus::PushAdd job=psana_pushgateway instance=$HOSTNAME gateway=$PROMETHEUS_GATEWAY

#conda activate ps-1.2.2-openmpi
#python test_send_recv.py
#python test_mpi.py
#echo $HOSTNAME

#conda activate test
#python test_mpi.py
