from psana import *
from mpi4py import MPI
import h5py, sys, time
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
assert size>1
nbatch = int(sys.argv[1])
#print '!!!!!!!!!!!!!!!!!!!!!!test1'

number_of_files = 10
j = 2
#print '!!!!!!!!!!!!!!!!!!!!test2', number_of_files, j
comm.Barrier()
start = MPI.Wtime()
file1 = h5py.File('file1.h5', 'r')
#print '!!!!!!!!!!!!!!!!!!!!test3', file1
#   ####   file2 = h5py.file('file2.h5', 'r')
truncSD = [i for i, x in enumerate(file1['smalldata']) if 'red' in x]
#print 'TRUNCATED SMALL DATA:', truncSD

truncTS = [file1['timestamp1'][i] for i in truncSD]
#print 'TRUNCATED TIME STAMP 1:', truncTS

data1 = [file1['bigdata1'][i] for i in truncTS]
#print 'TRUNCATED BIG DATA 1:', data1

while j <= number_of_files:
  def master():
    #open one h5 file per loop
    f = h5py.File('file%s.h5' %j, 'r')
    #match the timestamps
    foundind = [i for i, item in enumerate(f['timestamp%s' %j]) if item in truncTS]
    #print 'FOUNDIND NUMBER:', j, 'FOUNDIND:', foundind
    #I DON'T THINK SEARCHSORTED WORKS HERE!!!!!!!!!!!!!!!!!!!!!
    #foundind = np.searchsorted(file1['timestamp1'], file2['timestamp2'])
    #print 'FOUNDIND 1:', foundind
    indices = range(0, len(foundind), nbatch)
    #print indices
    for i in indices:
      # get indices for this rank
      if i+nbatch < len(foundind):
        myIndices=range(i, i+nbatch)
        foundind = [foundind[x] for x in myIndices]
        #print myIndices
      else:
        myIndices = range(i, len(foundind))
        foundind = [foundind[x] for x in myIndices]
      #print 'batched foundind:', foundind
      rankreq = comm.recv(source=MPI.ANY_SOURCE)
      comm.send((foundind, myIndices), dest=rankreq)
      #comm.send((list(foundind[myIndices]), myIndices), dest=rankreq)
    for rankreq in range(size-1):
      rankreq = comm.recv(source=MPI.ANY_SOURCE)
      comm.send('endrun', dest=rankreq)

  def client():
    f = h5py.File('file%s.h5' %j, 'r')
    start_local = time.time()
    while True:
      comm.send(rank, dest=0)
      results = comm.recv(source=0)
      if str(results) == 'endrun': 
        print "Rank: %d Time Elapsed (s): %6.3f"%(rank, time.time()-start_local)
        break
      #bigData1 = file1['bigdata1'][results[0]]
      #bigData2 = file2['bigdata2'][results[1]]
      #Pair the subsequential bigdata with the truncated subsequential timestamp
      data = [f['bigdata%s' %j][i] for i in truncTS]
      #print 'TRUNCATED BIG DATA', j, ':', data
  if rank == 0:
    master()
  else:
    client()
  j = j+1

comm.Barrier()
end = MPI.Wtime()

if rank ==0:
    print 'NBATCH', nbatch, 'NEXPEVTS_PERRANK', 'total time in seconds:', end - start
