'''
mpi_dealer.py
Execution commands:
    >16 Cores => mpirun -n 16 python mpi_dealer.py 1000
    <16 Cores => bsub -q psnehq -o log.txt -n 32 mpirun python mpi_dealer.py 1000
    @NERSC => sbatch -o log.txt submit_simple.sh
'''

from psana import *
from mpi4py import MPI
import h5py, sys, time
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
assert size>1
nbatch = int(sys.argv[1])

comm.Barrier()
start = MPI.Wtime()
file1 = h5py.File('file1.h5', 'r')
file2 = h5py.File('file2.h5', 'r')

#Block distribution among cores
def master(indices):
  for i in indices:
    #asking for a free rank
    rankreq = comm.recv(source=MPI.ANY_SOURCE)
    #hand out a list of indices to that rank
    if i+nbatch < len(file1['timestamp1']):
      myIndices=range(i, i+nbatch)
    else:
      myIndices = range(i, len(file1['timestamp1']))
    smlData = file1['smalldata'][myIndices]
    comm.send(myIndices, dest=rankreq)
  for rankreq in range(size-1):
    rankreq = comm.recv(source=MPI.ANY_SOURCE)
    comm.send('endrun', dest=rankreq)

def client():
  start_local = time.time()
  while True:
    comm.send(rank, dest=0)
    myIndices = comm.recv(source=0)
    if str(myIndices) == 'endrun': 
      print "Rank: %d Time Elapsed (s): %6.3f"%(rank, time.time()-start_local)
      break
    bigData1 = file1['bigdata1'][myIndices]
#Reading the data one-by-one (original way of reading data)
#    if len(myIndices) == nbatch:
#      for i in myIndices:
#        bigData1 = file1['bigdata1'][i] 
#      myIndices = [] 
'''    
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
'''
indices = range(0, len(file1['timestamp1']), nbatch)
if rank == 0:
  master(indices)
else:
  client()

comm.Barrier()
end = MPI.Wtime()

if rank ==0:
    print 'NBATCH', nbatch, 'NEXPEVTS_PERRANK', 'total time in seconds:', end - start
  
