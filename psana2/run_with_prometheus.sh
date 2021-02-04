#!/bin/bash

run_it() {
    /reg/g/psdm/sw/conda2/inst/envs/ps-3.1.16/bin/mpirun -n 40 --hostfile openmpi_hosts --mca btl_openib_allow_ib 1 ./run_slac.sh
}

run_it_slurm() {
    #srun --partition=anaq --ntasks=131 --ntasks-per-node=131 ./run_slac.sh
    srun --partition=anaq --ntasks=261 ./run_slac.sh # default tasks per node is 128
}

run_with_prometheus() {
    . $HOME/tmp/client_bash/prometheus.bash

    export PROMETHEUS_GATEWAY=psdm03:9091

    io::prometheus::NewGauge name=psana_start_time help='time_t when cron job last started' \
               labels=jobid,rank
    psana_start_time -jobid=$$ -rank=0 set $(date +'%s.%N')
    io::prometheus::PushAdd job=psana_pushgateway instance=$HOSTNAME gateway=$PROMETHEUS_GATEWAY

    run_it_slurm

    io::prometheus::NewGauge name=psana_end_time help='time_t when cron job last ended' \
               labels=jobid,rank
    psana_end_time -jobid=$$ -rank=0 set $(date +'%s.%N')
    io::prometheus::PushAdd job=psana_pushgateway instance=$HOSTNAME gateway=$PROMETHEUS_GATEWAY
}

export PS_EB_NODES=4
export PS_SMD_N_EVENTS=40000
run_with_prometheus
