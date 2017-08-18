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
time2Dist = h5py.File('file2.h5', 'r')

#check valid nbatch
if nbatch > len(times)/size: 
  print "Batch size is too large. Maximum size is", len(times)/size
  exit()

#striping
mytime = [i for i in xrange(len(times)) if i%(size*nbatch) >= (rank*nbatch) and i%(size*nbatch) < (rank+1)*nbatch]

#only get address of the data for batching
timestamp1 = time1Dist['timestamp1']
ds = time1Dist['bigdata1']

#for smldata read the entire column
smldata = time1Dist['smalldata'][mytime]

i = 0
while i < len(mytime):
  start_local = time.time()
  # reading
  if i + nbatch < len(mytime):
    c = ds[mytime][i:i+nbatch]
    ts = timestamp1[mytime][i:i+nbatch]
  else:
    c = ds[mytime][i:]
    ts = timestamp1[mytime][i: ]
  #search for ind in the second file
  foundind = np.searchsorted(time2Dist['timestamp2'], ts, side='left')
  cn_found = 0
  for n,ind in enumerate(foundind):
    if ind == len(time2Dist['timestamp2']): continue
    if ts[n] == time2Dist['timestamp2'][ind]:
      dat1 = time1Dist['bigdata1'][n]
      dat2 = time2Dist['bigdata2'][ind]
      cn_found += 1
  i += nbatch

#for debugging
print 'TIMESTAMP RANK TSB1[0] TSSIZE NEVENTS: ', rank, ts[0], len(ts), len(mytime)
comm.Barrier()
end = MPI.Wtime()
if rank== 0: print 'NBATCH', nbatch, 'NEXPEVTS_PERRANK', len(times)/size, 'TOTALTIME (s)', end-start

MPI.Finalize()
