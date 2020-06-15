import time


from mpi4py import MPI
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()


comm.Barrier()
ts = time.time()
if rank == 0:
    print(f'{ts:.0f}')
