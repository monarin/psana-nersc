from psana import *
import numpy as np
import time, sys
from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

exp = sys.argv[1]
runNo = sys.argv[2]

comm.Barrier()
start_ds = MPI.Wtime()
ds = DataSource('exp='+exp+':run='+str(runNo)+':idx')
comm.Barrier()
end_ds = MPI.Wtime()

det = Detector('CxiDs2.0:Cspad.0')

run = ds.runs().next()
times = run.times()
img = None
comm.Barrier()
start = MPI.Wtime()
if rank == 0:
  for t in times:
    rankreq = comm.recv(source=MPI.ANY_SOURCE)
    comm.send(t, dest=rankreq)
  for rankreq in range(size-1):
    rankreq = comm.recv(source=MPI.ANY_SOURCE)
    comm.send('endrun', dest=rankreq)
else:
  while True:
    comm.send(rank, dest=0)
    timestamp = comm.recv(source=0)
    if timestamp == 'endrun': break
    evt = run.event(timestamp)
    img = det.raw(evt)

comm.Barrier()
end = MPI.Wtime()

if rank == 0: print 'Ds (s)', start_ds, end_ds, end_ds-start_ds, 'Run Time (s)', start, end, end, end-start, end-start

MPI.Finalize() #finishing gracefully

