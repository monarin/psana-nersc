from psana import *
import numpy as np
import time
import sys

from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

exp = sys.argv[1]
runNo = sys.argv[2]

#comm.Barrier()
#start = MPI.Wtime()
ds = DataSource('exp='+exp+':run='+runNo+':idx')
#comm.Barrier()
#end = MPI.Wtime()
#if rank == 0: print "Opening Datasource (s)", end - start

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
if rank == 0: print "Total Elapsed (s)", start, end, end-start

MPI.Finalize() #finishing gracefully



