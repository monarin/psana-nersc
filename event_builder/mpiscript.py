#---------- Will use "mpirun -n 5 python testmpi.py" command to run on 5 cores
#Distributes data over cores and displays the first 5 entries of each core

#logistical support
from mpi4py import MPI
import h5py, glob, time, sys
import numpy as np

#initializatoin commands
nbatch = int(sys.argv[1])
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size() #number of cores

#profile mpitime
comm.Barrier()
start = MPI.Wtime()

#list distribution for file 1
time1Dist = h5py.File('file1.h5', 'r')
times=time1Dist['timestamp1']

#check valid nbatch
if nbatch > len(times)/size: 
  print "Batch size is too large. Maximum size is", len(times)/size

  exit()
#striping
mytime = [i for i in xrange(len(times)) if i%(size*nbatch) >= (rank*nbatch) and i%(size*nbatch) < (rank+1)*nbatch]

ts = time1Dist['timestamp1'][mytime]
smldata = time1Dist['smalldata'][mytime]

ds = time1Dist['bigdata1']

#reading in batch for SLAC
i = 0
start_local = time.time()
while i < len(mytime):
  # reading
  if i + nbatch < len(mytime):
    c = ds[mytime][i:i+nbatch]
  else:
    c = ds[mytime][i:]
  """
  if i + nbatch < len(mytime):
    for j in range(i, i+nbatch):
      c = ds[mytime][j]
      print rank, j, c
  else:
    for j in range(i, len(mytime)):
      c = ds[mytime][j]
      print rank, j, c
  """
  i += nbatch

#for debugging
print 'TIMESTAMP RANK:%d TSB1[0]: %5.1f TSSIZE: %d NEVENTS: %d TIME:%6.2f'%(rank, ts[0], len(ts), len(mytime), time.time()-start_local)

comm.Barrier()
end = MPI.Wtime()
if rank== 0: print 'NBATCH', nbatch, 'NEXPEVTS_PERRANK', len(times)/size, 'TOTALTIME (s)', end-start
MPI.Finalize()
