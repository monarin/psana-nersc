import os
from psana import DataSource
import numpy as np
from mpi4py import MPI

def filter(evt):
    return True

xtc_dir = os.path.join(os.environ.get('SCRATCH'),'d/psdm/cxi/cxid9114/xtc2') 
ds = DataSource('exp=cxid9114:run=1:dir=%s'%(xtc_dir), filter=filter, batch_size=100)

comm = ds.mpi.comm
rank = ds.mpi.rank
size = ds.mpi.size

comm.Barrier()
st = MPI.Wtime()
cn_evt = 0
for run in ds.runs():
    for evt in run.events():
        for d in evt:
            cn_evt += 1

sendbuf = np.zeros(1, dtype='i') + cn_evt
recvbuf = None
if rank == 0:
    recvbuf = np.empty([size, 1], dtype='i')
comm.Gather(sendbuf, recvbuf, root=0)

comm.Barrier()
en = MPI.Wtime()
if rank == 0:
    print("No. of events: %d Elapsed Time: %f s Rate: %f (kHz)"%(np.sum(recvbuf), en-st, np.sum(recvbuf)/((en-st)*1e3)))

