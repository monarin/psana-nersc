#!/usr/bin/env python3
import time, os
import random
import threading
from prometheus_client import CollectorRegistry, Counter, push_to_gateway
 
from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if rank == 0:
    jobid = os.getpid()
    print(f'test_pushgateway jobid={jobid}')
else:
    jobid = None
jobid = comm.bcast(jobid, root=0)
 
registry = CollectorRegistry()
PUSH_GATEWAY = 'psdm03:9091'
TIMEOUT=None
 
def push_metrics():
    while True:
        print(f'rank: {rank} jobid: {jobid} pushed {time.time()}')
        push_to_gateway(PUSH_GATEWAY, job='test_pushgateway', grouping_key={'jobid': jobid, 'rank': rank}, registry=registry, timeout=TIMEOUT)
        time.sleep(5)
 
c = Counter('evts_transmit', 'no. of events sent', ['unit','endpoint'], registry=registry)
 
print(f'rank: {rank} creating {registry._collector_to_names.keys()}')
gw_thread = threading.Thread(target=push_metrics)
gw_thread.start()
 
while True:
    c.labels('evts', 0).inc(1000)
    time.sleep(1)
