from psana import DataSource
import os, time
import numpy as np
from mpi4py import MPI
comm=MPI.COMM_WORLD
rank=comm.Get_rank()
size=comm.Get_size()

import logging
logger = logging.getLogger('psana.psexp.node')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

def filter_fn(evt):
    return True

def test_live():
    xtc_dir = './tmp'
    ds = DataSource(exp='xpptut15', run=1, dir=xtc_dir, live=True)
    sendbuf = np.zeros(1, dtype='i')
    recvbuf = None
    if rank == 0:
        recvbuf = np.empty([size, 1], dtype='i')

    for run in ds.runs():
        #det = run.Detector('hsd')
        for evt in run.events():
            print(evt.timestamp)
            sendbuf += 1
    comm.Gather(sendbuf, recvbuf, root=0)
    return recvbuf


recvbuf = test_live()
if rank == 0:
    processed_events = np.sum(recvbuf)
    print(f'#events={processed_events}') 
