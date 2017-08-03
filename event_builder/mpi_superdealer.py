from psana import *
from mpi4py import MPI
import h5py, sys, time
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
assert size>1

comm.Barrier()
start = MPI.Wtime()
file1 = h5py.File('file1.h5', 'r')
file2 = h5py.File('file2.h5', 'r')

# input n_batch
nbatch = int(sys.argv[1])


def master(indices):
  for i in indices:
    rankreq = comm.recv(source=MPI.ANY_SOURCE)
    comm.send(i, dest=rankreq)
  for rankreq in range(size-1):
    rankreq = comm.recv(source=MPI.ANY_SOURCE)
    comm.send('endrun', dest=rankreq)

def client():
  start_local = time.time()
  myIndices = []
  while True:
    comm.send(rank, dest=0)
    evtIndex = comm.recv(source=0)
    if str(evtIndex) == 'endrun': 
      print "Rank: %d Time Elapsed (s): %6.3f"%(rank, time.time()-start_local)
      break
    myIndices.append(evtIndex)
    # Read smlData
    smlData = file1['smalldata'][evtIndex]
    # Read timestamp
    # Read bigData in batch mode
    #if len(myIndices) == nbatch:
    #  for i in myIndices:
    #    bigData1 = file1['bigdata1'][i] 
    #  myIndices = [] 
    # Access the second file
    if len(myIndices) == nbatch:
      timestamp1 = file1['timestamp1'][myIndices]
      foundind = np.searchsorted(file2['timestamp2'], timestamp1, side='left')
      for i,ind in enumerate(foundind):  
        if ind == len(file2['timestamp2']): continue
        if timestamp1[i] == file2['timestamp2'][ind]:
          bigData1 = file1['bigdata1'][i]
          bigData2 = file2['bigdata2'][ind]
      myIndices = []

indices = range(len(file1['timestamp1']))
if rank == 0:
  master(indices)
else:
  client()

comm.Barrier()
end = MPI.Wtime()

if rank ==0:
    print 'NBATCH', nbatch, 'NEXPEVTS_PERRANK', 'total time in seconds:', end - start
  
