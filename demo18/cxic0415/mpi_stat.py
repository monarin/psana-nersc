from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

import os, glob, sys
path = sys.argv[1]
if rank == 0:
  debug_files = glog.glob(path+'/*.txt')
  for f in debug_files:
    rankreq = comm.recv(source=MPI.ANY_SOURCE)
    comm.send(f, dest=rankreq)

  for rankreq in range(size-1):
    rankreq = comm.recv(source=MPI.ANY_SOURCE)
    comm.send('endrun', dest=rankreq)
else:
  while True:
    comm.send(rank, dest=0)
    f = comm.recv(source=0)
    if f == 'endrun': break
    cn_start = 0
    with open(f, 'r') as d:
       for line in d:
         if line.find(',start') > -1: cn_start += 1
         if line.find(',
