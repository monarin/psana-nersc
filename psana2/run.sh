#!/bin/bash


# Test Smd0
# Note that running with jsrun --erf_input erf0.txt ./run.sh
# or jsrun -n 1 ./run.sh (w or w/o OMP_NUM_THREADS)
# give the SAME performance (10 MHz - 20200420)
# erf0.txt is
# 1 : {host: 1; cpu: {0-63}} or 
# 1 : {host: 1; cpu: {0-16}}
#export OMP_NUM_THREADS=15
#source $MEMBERWORK/chm137/installation/cctbx/summit/env.sh
#python dev_smd0.py
#strace -ttt -f -o $$.log python dev_smd0.py


# Test bigdata
#export PS_SMD_NODES=1
#export PS_SMD_MAX_RETRIES=0
#export PS_SMD_N_EVENTS=1000
#export LCLS_CALIB_HTTP=http://login5:6748/calib_ws
#export PS_PARALLEL=none
#echo "testing $1 files"
#python dev_smd0.py $1
#python dev_smdreader_manager.py
#python dev_bd.py


source /reg/g/psdm/etc/psconda.sh -py3
# Test mpi
python test_send_recv.py

