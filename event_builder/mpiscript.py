#---------- Will use "mpirun -n 5 python testmpi.py" command to run on 5 cores
#Distributes data over cores and displays the first 5 entries of each core

#logistical support
from mpi4py import MPI
import h5py, glob, time, sys
import numpy as np

start = time.time()

#initializatoin commands
nbatch = int(sys.argv[1])
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size() #number of cores
#offset = rank*


#list distribution for file 1
time1Dist = h5py.File('file1.h5', 'r')
times=time1Dist['timestamp1']
mytime = [i for i in xrange(len(times)) if i%(size*nbatch) >= (rank*nbatch) and i%(size*nbatch) < (rank+1)*nbatch]

ts = time1Dist['timestamp1'][mytime]
smldata = time1Dist['smalldata'][mytime]

ds = time1Dist['bigdata1']
cnEvents = 0
for i in mytime:
  evti = ds[i]
  cnEvents += 1

#for debugging
print 'Core_TIMESTAMP: ', rank, ts[0], ts[nbatch], len(ts)
print 'CORE_LARGEDATA', rank, cnEvents

if rank== 0: print 'NBATCH', nbatch 
if rank==0: print 'TOTALTIME', time.time()-start
MPI.Finalize()
