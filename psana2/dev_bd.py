import os
from psana import DataSource
import numpy as np
import vals
import time
from mpi4py import MPI
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

xtc_dir = "/gpfs/alpine/proj-shared/chm137/data/LD91"
#xtc_dir = "/gpfs/alpine/proj-shared/chm137/data/test/.tmp"
batch_size = 100

# Usecase 1a : two iterators with filter function
st = MPI.Wtime()
ds = DataSource(exp='cxid9114', run=95, dir=xtc_dir, batch_size=batch_size)

ds_done_t = MPI.Wtime()

comm.Barrier()
ds_called_ts = time.time()
barrier_t = MPI.Wtime()

sendbuf = np.zeros(1, dtype='i')
recvbuf = None
if rank == 0:
    recvbuf = np.empty([size, 1], dtype='i')

for run in ds.runs():
    det = run.Detector('cspad')
    #det = run.Detector('xppcspad')
    for evt in run.events():
        sendbuf += 1
        photon_energy = det.raw.photonEnergy(evt)
        raw = det.raw.raw(evt)
        #raw = det.raw.calib(evt)
        print(evt.timestamp, raw.shape)

run_done_t = MPI.Wtime()

comm.Gather(sendbuf, recvbuf, root=0)
en = MPI.Wtime()

if rank == 0:
    n_events = np.sum(recvbuf)
    evtbuilder = int(os.environ.get('PS_SMD_NODES', 1))
    print(f'#eb: {evtbuilder} total(s): {en-st:.2f} rate(kHz): {n_events/((en-st)*1000):.2f} ds(s): {ds_done_t-st:.2f} barrier(s): {barrier_t-ds_done_t:.2f} run(s): {run_done_t-barrier_t:.2f} gather(s): {en-run_done_t:.2f} ds_called: {ds_called_ts:.0f}')
