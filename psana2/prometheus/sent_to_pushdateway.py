#!/usr/bin/env python3

import time
import random
import threading
import os
import logging

from prometheus_client import CollectorRegistry, Counter, push_to_gateway, Summary
from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()

import logging
logging.basicConfig(level=logging.DEBUG,
        format='(%(threadName)-10s) %(message)s',
        )

registry = CollectorRegistry()

# Test Summary
s = Summary('psana_wait_recv_ms', 'Waiting for something', registry=registry)
@s.time()
def receive():
    time.sleep(2)

def push_metrics(e, registry):
    while not e.isSet():
        push_to_gateway('psdm03:9091', job='pushgateway', grouping_key={'pid': os.getpid()}, registry=registry)
        logging.debug('rank: %d (pid: %d) pushed %s'%(rank, os.getpid(), time.time()))
        time.sleep(5)    

def test_send():
    # Test Counter
    if rank == 0:
        c = Counter('evts_transmit', 'events handed to big data nodes', ['unit'], registry=registry)
    else:
        c = Counter('evts_received', 'events received', ['unit'], registry=registry)

    if rank == 0:
        another_c = registry._names_to_collectors['evts_transmit_total']
    else:
        another_c = registry._names_to_collectors['evts_received_total']

    e = threading.Event()
    gw_thread = threading.Thread(target=push_metrics, args=(e, registry), daemon=True)
    gw_thread.start()

    cn = 0
    while True:
        if rank == 0:
            another_c.labels('evts').inc(1)
            another_c.labels('size').inc(100)
        else:
            another_c.labels('evts').inc(5)
            another_c.labels('size').inc(500)

        time.sleep(2)
        cn += 1
        logging.debug('cn=%d'%cn)
        
        receive()
        logging.debug('call receive def')

        #if cn == 30:
        #    break

    logging.debug('exit')
    e.set()

if __name__ == "__main__":
    logging.debug('test 1')
    test_send()
    #logging.debug('test 2')
    #test_send()
