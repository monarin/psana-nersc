#!/bin/bash

JOBID=$3
BATCH_SIZE=$1
QUERY_START=`date +%s`
SSUBMIT_HOST=$2

export SUBMIT_HOST=$SSUBMIT_HOST
for i in $(seq 1 5)
do
    python monitor.py $JOBID $QUERY_START > prom_tmp_log
    python read_monitor_output.py prom_tmp_log $BATCH_SIZE $QUERY_START
    QUERY_START=$(( QUERY_START - 15 ))
done
