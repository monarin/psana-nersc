""" For testing live mode and other PSANA2 performance measurement

on drp-srcf, generate slurm_hosts then run
SLURM_HOSTFILE=slurm_hosts srun -o log.log --partition=anaq --exclusive python -u test_live.py

"""
import time
import os,sys
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
    batch_size = 1000
    max_events = 0
    
    hutch='tst'
    exp=sys.argv[1]
    runno=int(sys.argv[2])

    #hutch='rix'
    #exp='rixtst099'
    #runno=12

    xtc_dir=f'/cds/data/drpsrcf/{hutch}/{exp}/xtc/'

    ds = DataSource(exp=exp, 
                    run=runno, 
                    batch_size=batch_size, 
                    max_events=max_events, 
                    dir=xtc_dir, 
                    live=True
                    )

    sendbuf = np.zeros(1, dtype='i')
    recvbuf = None
    if rank == 0:
        recvbuf = np.empty([size, 1], dtype='i')

    st = time.time()
    for run in ds.runs():
        for nevt, evt in enumerate(run.events()):
            if nevt % 1000 == 0 and nevt > 0:
                en = time.time()
                print(f'RANK: {rank:4d} EVENTS: {nevt:10d} RATE: {(1000/(en-st))*1e-3:.2f}kHz', flush=True)
                st = time.time()
            sendbuf += 1
    
    # Count total no. of events
    comm.Gather(sendbuf, recvbuf, root=0)
    if rank == 0:
        n_events = np.sum(recvbuf)
    else:
        n_events = None
    n_events = comm.bcast(n_events, root=0)
    return n_events


if __name__ == "__main__":
    comm.Barrier()
    t0 = MPI.Wtime()
    
    n_events = test_standard()
    
    comm.Barrier()
    t1 = MPI.Wtime()
    if rank == 0:
        n_eb_nodes = int(os.environ.get('PS_EB_NODES', '1'))
        print(f'TOTAL TIME:{t1-t0:.2f}s #EB: {n_eb_nodes:3d} EVENTS:{n_events:10d} RATE:{(n_events/(t1-t0))*1e-6:.2f}MHz', flush=True)

