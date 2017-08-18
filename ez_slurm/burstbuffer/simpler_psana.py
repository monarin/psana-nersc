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
  ds = DataSource('exp='+exp+':run='+str(run_no)+':idx')
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

  comm.Barrier()
  end = MPI.Wtime()
  print 'Rank', rank, 'Run Time (s)', end - start, start, end

MPI.Finalize() #finishing gracefully



