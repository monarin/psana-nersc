from psana import DataSource
import time, os
from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
if rank == 0:
    print(f'RANK 0 PID={os.getpid()}')

# Defines run parameters and creates datasource
xtc_dir='/cds/data/drpsrcf/users/monarin/amox27716/big'
max_events = 0
NUMCHS = 5
ds = DataSource(exp='amox27716', 
                run=85,
                dir=xtc_dir,
                monitor=True,
                max_events=max_events)
run = next(ds.runs())
det = run.Detector("tmo_quadanode")


# Starts reading data
st = time.monotonic()
for i_evt, evt in enumerate(run.events()):
    for i_chan in range(NUMCHS):
        wfs_chan = det.fex.waveforms(evt, i_chan)
        ts_chan = det.fex.times(evt, i_chan)
    if i_evt % 1000 == 0 and i_evt > 0:
        en = time.monotonic()
        print(f'RANK:{rank:4d} RATE:{(1000/(en-st))*1e-3:.2f}kHz')
        st = time.monotonic()
