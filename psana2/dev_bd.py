import os
from psana import DataSource
import numpy as np
import vals
from mpi4py import MPI
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

def filter_fn(evt):
    return True

xtc_dir = "/ffb01/mona/xtc2/.tmp"
max_events = 2000
batch_size = 2000
n_files = 16
os.environ['PS_SMD_N_EVENTS']=str(batch_size)

# Usecase 1a : two iterators with filter function
st = MPI.Wtime()
ds = DataSource(exp='xpptut13', run=1, dir=xtc_dir, filter=filter_fn, max_events=max_events)

sendbuf = np.zeros(1, dtype='i')
recvbuf = None
if rank == 0:
    recvbuf = np.empty([size, 1], dtype='i')

for run in ds.runs():
    det = run.Detector('xppcspad')
    edet = run.Detector('HX2:DVD:GCC:01:PMON')
    for step in run.steps():
        for evt in step.events():
            sendbuf += 1
            assert evt._size == n_files # check that n_files dgrams are in there
            assert edet(evt) is None or edet(evt) == 41.0
        print(sendbuf)

comm.Gather(sendbuf, recvbuf, root=0)
en = MPI.Wtime()

if rank == 0:
    n_events = np.sum(recvbuf)
    evtbuilder = int(os.environ.get('PS_SMD_NODES', 1))
    print('#evtbuilder: %d #events: %d total elapsed (s): %6.2f rate (kHz): %6.2f'%(evtbuilder, n_events, en-st, n_events/((en-st)*1000)))
