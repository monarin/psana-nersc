'''
mpi_dealer.py
Execution commands:
    >16 Cores => mpirun -n 16 python mpi_dealer.py 1000
    <16 Cores => bsub -q psnehq -o log.txt -n 32 mpirun python mpi_dealer.py 1000
    @NERSC => sbatch -o log.txt submit_simple.sh
'''

#Logistical Support
from psana import *
from mpi4py import MPI
import h5py, sys, time
import numpy as np

#Initialization Definitions
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
assert size>1
nbatch = int(sys.argv[1])

#Start of Analysis -- Opening h5 Files
comm.Barrier()
start = MPI.Wtime()
file1 = h5py.File('file1.h5', 'r')
file2 = h5py.File('file2.h5', 'r')

#Block distribution among cores
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
#Analysis by blocks of events    
    if evtIndex+nbatch < len(file1['timestamp1']):
      myIndices=range(evtIndex, evtIndex+nbatch)
    else:
      myIndices = range(evtIndex, len(file1['timestamp1']))
    # Read smlData
    smlData = file1['smalldata'][myIndices]
    # Read bigData in batch mode
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
  
