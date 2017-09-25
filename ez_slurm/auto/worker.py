from psana import *
import numpy as np
import time
import sys

from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

exp = sys.argv[1]
run_st = int(sys.argv[2])
run_en = int(sys.argv[3])

for run_no in range(run_st, run_en):
  comm.Barrier()
  start_ds = MPI.Wtime()
  ds = DataSource('exp='+exp+':run='+str(run_no)+':idx')
  comm.Barrier()
  end_ds = MPI.Wtime()
  det = Detector('CxiDs2.0:Cspad.0')
  run = ds.runs().next()

  # list of all events
  times = run.times()
  # striping
  #mytimes = [times[i] for i in xrange(len(times)) if (i+rank)%size == 0]
  # splitting
  mytimes = np.array_split(times, size)[rank]

  comm.Barrier()
  start = MPI.Wtime()
  img = None
  for i,timestamp in enumerate(mytimes):
    evt = run.event(timestamp)
    #calling det.raw point blank
    img = det.raw(evt)
    if i==0:
      comm.Barrier()
      end_1 = MPI.Wtime()

  comm.Barrier()
  end = MPI.Wtime()
  if rank == 0: print 'Ds (s)', start_ds, end_ds, end_ds-start_ds, 'Run Time (s)', start, end_1, end, end_1-start, end-start
MPI.Finalize() #finishing gracefully



