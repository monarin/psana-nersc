import os, time
from psana import DataSource
import numpy as np
from mpi4py import MPI
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

def filter_fn(evt):
    return True

comm.Barrier()
st = MPI.Wtime()
max_events = 10000000
batch_size = 1000
#xtc_dir = "/ffb01/monarin/hsd"
#xtc_dir = "/reg/d/psdm/xpp/xpptut15/scratch/mona/hsd"
#xtc_dir = "/global/cscratch1/sd/monarin/testxtc2/hsd"
xtc_dir = os.path.join(os.environ['DW_PERSISTENT_STRIPED_psana2_hsd'],'hsd')
ds = DataSource('exp=xpptut13:run=1:dir=%s'%(xtc_dir), filter=filter_fn, max_events=max_events, batch_size=batch_size)

#sendbuf = np.zeros(1, dtype='i') 
#recvbuf = None
#if rank == 0:
#    recvbuf = np.empty([size, 1], dtype='i')

for run in ds.runs():
    #det = run.Detector('xppcspad')
    for evt in run.events():
        print("%d %f"%(rank, time.time()))
#        sendbuf += 1 

#comm.Gather(sendbuf, recvbuf, root=0)

comm.Barrier()
en = MPI.Wtime()
if rank == 0:
    #n_events = np.sum(recvbuf)
    n_events = max_events
    smd0 = int(os.environ.get('PS_SMD0_THREADS', 1))
    evtbuilder = int(os.environ.get('PS_SMD_NODES', 1))
    print('#smd0threads: %d #evtbuilder: %d #events: %d total elapsed (s): %6.2f rate (kHz): %6.2f'%(smd0, evtbuilder, n_events, en-st, n_events/((en-st)*1000)))

