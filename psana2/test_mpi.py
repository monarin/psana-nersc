#!/usr/bin/env python

from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
myhost = MPI.Get_processor_name()
print(f'RANK{rank}x size:{size} {myhost}')

#from psana import DataSource


