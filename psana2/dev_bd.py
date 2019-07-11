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

xtc_dir = "/reg/neh/home/monarin/lcls2/tmp2"

# Usecase 1a : two iterators with filter function
st = MPI.Wtime()
ds = DataSource(exp='xpptut13', run=1, dir=xtc_dir, filter=filter_fn)

sendbuf = np.zeros(1, dtype='i')
recvbuf = None
if rank == 0:
    recvbuf = np.empty([size, 1], dtype='i')

for run in ds.runs():
    det = run.Detector('xppcspad')
    edet = run.Detector('XPP:VARS:STRING:01')
    for evt in run.events():
        sendbuf += 1
        padarray = vals.padarray
        assert(np.array_equal(det.raw.calib(evt),np.stack((padarray,padarray,padarray,padarray))))
        assert evt._size == 2 # check that two dgrams are in there
        assert edet(evt) == "Test String"

comm.Gather(sendbuf, recvbuf, root=0)

en = MPI.Wtime()
if rank == 0:
    n_events = np.sum(recvbuf)
    evtbuilder = int(os.environ.get('PS_SMD_NODES', 1))
    print('#evtbuilder: %d #events: %d total elapsed (s): %6.2f rate (kHz): %6.2f'%(evtbuilder, n_events, en-st, n_events/((en-st)*1000)))
