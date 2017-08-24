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
print "Read Ds Time (s)", end_ds - start_ds, start_ds, end_ds

det = Detector('CxiDs2.0:Cspad.0')

run = ds.runs().next()
times = run.times()
img = None
comm.Barrier()
start = MPI.Wtime()
print "Start Client-Server", start
if rank == 0:
  print "Rank 0: I'm the server."
  for t in times:
    rankreq = comm.recv(source=MPI.ANY_SOURCE)
    comm.send(t, dest=rankreq)
  for rankreq in range(size-1):
    rankreq = comm.recv(source=MPI.ANY_SOURCE)
    comm.send('endrun', dest=rankreq)
else:
  print "Rank %d: I'm a client."%(rank)
  cnEvt = 0
  while True:
    comm.send(rank, dest=0)
    timestamp = comm.recv(source=0)
    if timestamp == 'endrun': break
    evt = run.event(timestamp)
    img = det.raw(evt)
    cnEvt += 1
  end = time.time()
  print "Rank ", rank, 'Time (s)', end-start, start, end, cnEvt

comm.Barrier()
end_total = MPI.Wtime()

if rank == 0: print "Total Time (s)", end_total-start, start, end_total

MPI.Finalize() #finishing gracefully

