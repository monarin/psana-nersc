import time
import os
from psana import DataSource
import numpy as np
import vals
from mpi4py import MPI
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

#import logging
#logger = logging.getLogger('psana.psexp')
#logger.setLevel(logging.DEBUG)
#ch = logging.StreamHandler()
#ch.setLevel(logging.DEBUG)
#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#ch.setFormatter(formatter)
#logger.addHandler(ch)
def test_standard():
    #exp='tstx00417'
    #runno=224
    #xtc_dir='/cds/data/drpsrcf/tst/tstx00417/xtc'
    exp='rixtst099'
    runno=12
    xtc_dir='/cds/data/drpsrcf/rix/rixtst099/xtc/'
    batch_size = 1000
    max_events = 0
    comm.Barrier()
    t0 = MPI.Wtime()
    ds = DataSource(exp=exp, run=runno, batch_size=batch_size, max_events=max_events, dir=xtc_dir, live=True)

    sendbuf = np.zeros(1, dtype='i')
    recvbuf = None
    if rank == 0:
        recvbuf = np.empty([size, 1], dtype='i')

    st = time.time()
    for run in ds.runs():
        for nevt, evt in enumerate(run.events()):
            if nevt % 1000 == 0:
                en = time.time()
                print(nevt, evt.timestamp, (1000/(en-st))*1e-3, flush=True)
                st = time.time()
            sendbuf += 1

    comm.Gather(sendbuf, recvbuf, root=0)
    comm.Barrier()
    t1 = MPI.Wtime()
    if rank == 0:
        n_eb_nodes = int(os.environ.get('PS_EB_NODES', '1'))
        print(f'TOTAL TIME:{t1-t0:.2f}s #EB: {n_eb_nodes} n_events={np.sum(recvbuf)}')

test_standard()

