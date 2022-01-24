import sys
import os
import numpy as np
from psana import DataSource
from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
# comm.Barrier()
st = MPI.Wtime() # el start time
print(rank, st)
