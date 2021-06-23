#!/bin/bash

JOBID=$1
BATCH_SIZE=$2
QUERY_START=$3

for i in $(seq 1 20)
do
    python monitor.py $JOBID $QUERY_START > xx
    python read_monitor_output.py xx $BATCH_SIZE $QUERY_START
    QUERY_START=$(( QUERY_START + 15 ))
done
