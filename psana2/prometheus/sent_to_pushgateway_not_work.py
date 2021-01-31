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
        push_to_gateway('psdm03:9091', job='batch_duplicate',  registry=registry)
        print(f'rank: {rank} pushed {registry._collector_to_names.keys()} {time.time()}')
        time.sleep(5)

c_1 = Counter('evts_transmit', 'events handed to big data nodes', registry=registry)
c_2 = Counter('evts_size', 'size of events', registry=registry)

print(f'rank: {rank} creating {registry._collector_to_names.keys()}')
if rank == 0:
    gw_thread = threading.Thread(target=push_metrics)
    gw_thread.start()

while True:
    if rank == 0:
        c_1.inc(1)
    else:
        c_2.inc(100)

    time.sleep(2)
