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
i = 0
#offset = rank*

#FIX ERROR MESSAGE AND INSERT HERE

#for time testing --use glob to diaply all files
comm.Barrier()
start1 = MPI.Wtime()

#list distribution for file 1
time1Dist = h5py.File('file1.h5', 'r')
times=time1Dist['timestamp1']
mytime = [i for i in xrange(len(times)) if i%(size*nbatch) >= (rank*nbatch) and i%(size*nbatch) < (rank+1)*nbatch]

ts = time1Dist['timestamp1'][mytime]
smldata = time1Dist['smalldata'][mytime]

#start = time.time()
ds = time1Dist['bigdata1']
i = 0
while i < len(mytime):
    evti = ds[i]
    i = i+1
#end = time.time()
#print 'Time:', end-start
'''
i = 1
done = False
while !done:
    bigData = time1Dist['bigdata1'][(i-1)*10:10*i, :]
    i = i + 1
    if i == len(time1Dist['bigdata1']):
        done = True
'''

#for debugging
print 'Core Number: ', rank, ' | Timestamp 1:', ts
print 'Core Number: ', rank, ' | Small Data:', smldata
print 'Core Number: ', rank, ' | Large Data 1:', i

#for time testing
comm.Barrier()
end1 = MPI.Wtime()
print 'MPI total time', end1-start1
if rank==0: print 'trank','| Rank', rank, '| Time', end-start
MPI.Finalize()
