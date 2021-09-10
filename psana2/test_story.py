import sys
import os
import numpy as np
from psana import DataSource
from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
# comm.Barrier()
st = MPI.Wtime() # el start time

# xtc_dir = os.path.join(os.environ.get('TEST_XTC_DIR', os.getcwd()),'.tmp')
if rank == 0:
    print('ENVIRONMENT VARIABLES')
    print(f"PS_SMD0_NUM_THREADS: {os.environ.get('PS_SMD0_NUM_THREADS', '16')}", flush=True)
    print(f"PS_SMD_N_EVENTS:     {os.environ.get('PS_SMD_N_EVENTS', '1000')}", flush=True)
    print(f"PS_EB_NODES:         {os.environ.get('PS_EB_NODES', '1')}", flush=True)
exp1 = 'tmoc00118'
xtc_dir = '/cds/data/drpsrcf/users/monarin/tmoc00118/xtc4n'
#max_events=10

ds = DataSource(exp=exp1, run=463, dir=xtc_dir, batch_size=10000)

sendbuf = np.zeros(1, dtype='i')
recvbuf = None

if rank == 0:
    recvbuf = np.empty([size, 1], dtype='i')

for run in ds.runs():
    det = run.Detector('hsd')
    for evt in run.events():
        #print(evt.timestamp)
        sendbuf += 1

comm.Gather(sendbuf, recvbuf, root=0)
# comm.Barrier()
en = MPI.Wtime() # el total time

if rank == 0:
    print(en - st)
