#!/bin/bash

BATCH_SIZE=$1
SSUBMIT_HOST=$2
JOBID=$3
N_EB_NODES=$4
N_RANKS=$5
QUERY_START=$6
#QUERY_START=`date +%s`

export SUBMIT_HOST=$SSUBMIT_HOST

for i in $(seq 1 10)
do
    python monitor.py $JOBID $QUERY_START $N_EB_NODES $N_RANKS > prom_tmp_log
    python read_monitor_output.py prom_tmp_log $BATCH_SIZE $QUERY_START
    QUERY_START=$(( QUERY_START + 15 ))
done
