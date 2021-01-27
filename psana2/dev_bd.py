import os
from psana import DataSource
import numpy as np
#import vals
import time
from mpi4py import MPI
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

import logging
logging.basicConfig(level=logging.DEBUG,
                format='(%(threadName)-10s) %(message)s',
        )

#xtc_dir = "/ffb01/mona/xtc2/.tmp"
xtc_dir = "/reg/neh/home/monarin/tmp/.tmp"

batch_size = 1000
max_events = 100000

def filter_fn(evt):
    if evt._nanoseconds % 2 == 0:
        time.sleep(3)
        logging.debug(f"{evt._nanoseconds} True rank {rank} sleep 3 s")
        return True
    else:
        logging.debug(f"{evt._nanoseconds} False")
        return False

#def filter_fn(evt):
#    return True

# Usecase 1a : two iterators with filter function
st = MPI.Wtime()
#ds = DataSource(exp='tstx00517', run=72, dir=xtc_dir, batch_size=batch_size, max_events=max_events, live=True, filter=filter_fn)
#ds = DataSource(exp='xpptut15', run=1, dir=xtc_dir, batch_size=batch_size, max_events=max_events, monitor=False)
ds = DataSource(exp='xpptut15', run=1, dir=xtc_dir, batch_size=batch_size, max_events=max_events, monitor=True, filter=filter_fn)

ds_done_t = MPI.Wtime()

comm.Barrier()
ds_called_ts = time.time()
barrier_t = MPI.Wtime()

sendbuf = np.zeros(1, dtype='i')
recvbuf = None
if rank == 0:
    recvbuf = np.empty([size, 1], dtype='i')
    print(f'RANK 0 PID:{os.getpid()}')

sendstr = ''
for run in ds.runs():
    det = run.Detector('xppcspad')
    #det = run.Detector('tmohsd')
    for i, evt in enumerate(run.events()):
        sendbuf += 1
        #photon_energy = det.raw.photonEnergy(evt)
        raw = det.raw.raw(evt)
        #raw = det.raw.waveforms(evt)
        #print(f'bd: ts={evt._seconds}.{evt._nanoseconds} {raw.keys()}')
        #if i % 1000 == 0:
        #    print(f'bd: ts={evt._seconds}.{evt._nanoseconds} {raw.shape}')
        sendstr += f'{rank} {time.time()}\n'
        #if rank == 3:
        #    time.sleep(2)

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
