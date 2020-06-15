import os
from psana import DataSource
import numpy as np
import vals
import time
from mpi4py import MPI
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

#xtc_dir = "/gpfs/alpine/proj-shared/chm137/data/LD91"
#xtc_dir = "/gpfs/alpine/proj-shared/chm137/data/test/.tmp"
#xtc_dir = "/ffb01/mona/xtc2/.tmp"
xtc_dir = "/reg/neh/home/monarin/tmp/.tmp"
batch_size = 1000
max_events = 0

def filter_fn(evt):
    return True

# Usecase 1a : two iterators with filter function
st = MPI.Wtime()
ds = DataSource(exp='xpptut13', run=1, dir=xtc_dir, batch_size=batch_size, max_events=max_events, filter=filter_fn)

ds_done_t = MPI.Wtime()

comm.Barrier()
ds_called_ts = time.time()
barrier_t = MPI.Wtime()

sendbuf = np.zeros(1, dtype='i')
recvbuf = None
if rank == 0:
    recvbuf = np.empty([size, 1], dtype='i')

sendstr = ''
for run in ds.runs():
    #det = run.Detector('cspad')
    det = run.Detector('xppcspad')
    for i, evt in enumerate(run.events()):
        sendbuf += 1
        #photon_energy = det.raw.photonEnergy(evt)
        #raw = det.raw.raw(evt)
        raw = det.raw.calib(evt)
        #print(evt.timestamp, raw.shape)
        sendstr += f'{rank} {time.time()}\n'

run_done_t = MPI.Wtime()

comm.Gather(sendbuf, recvbuf, root=0)
sendstr = comm.gather(sendstr, root=0)
en = MPI.Wtime()

if rank == 0:
    n_events = np.sum(recvbuf)
    evtbuilder = int(os.environ.get('PS_SMD_NODES', 1))
    with open('log_dev_bd.txt', 'w') as f:
        f.write(''.join(sendstr))
        f.write(f'#eb: {evtbuilder} #evt:{n_events} total(s): {en-st:.2f} rate(kHz): {n_events/((en-st)*1000):.2f} ds(s): {ds_done_t-st:.2f} barrier(s): {barrier_t-ds_done_t:.2f} run(s): {run_done_t-barrier_t:.2f} gather(s): {en-run_done_t:.2f} ds_called: {ds_called_ts:.0f}')
