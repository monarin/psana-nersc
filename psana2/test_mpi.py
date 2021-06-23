

from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
myhost = MPI.Get_processor_name()

#from psana import DataSource


print(rank, size, myhost)
