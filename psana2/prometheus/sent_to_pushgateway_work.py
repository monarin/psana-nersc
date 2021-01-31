#!/usr/bin/env python3

import time
import random
import threading

from prometheus_client import CollectorRegistry, Counter, push_to_gateway
from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()

registry = CollectorRegistry()

def push_metrics():

    while True:
        push_to_gateway('psdm03:9091', job='pushgateway_rank_%d'%(rank),  registry=registry)
        print(f'rank: {rank} pushed {registry._collector_to_names.keys()} {time.time()}')
        time.sleep(5)

if rank == 0:
    c = Counter('evts_transmit', 'events handed to big data nodes', ['unit'], registry=registry)
else:
    c = Counter('evts_received', 'events received', ['unit'], registry=registry)

print(f'rank: {rank} creating {registry._collector_to_names.keys()}')
gw_thread = threading.Thread(target=push_metrics)
gw_thread.start()

while True:
    if rank == 0:
        c.labels('evts').inc(1)
        c.labels('size').inc(100)
    else:
        c.labels('evts').inc(5)
        c.labels('size').inc(500)

    time.sleep(2)
