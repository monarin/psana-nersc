from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
myhost = MPI.Get_processor_name()
import numpy as np

n = 100000
if rank == 0:
    data = np.arange(1000000, dtype='i')
    for i in range(n):
        comm.send(data, dest=1)
    comm.send(np.zeros(1000000, dtype='i'), dest=1)
else:
    while True:
        data = comm.recv(source=0)
        print(f'rank{rank} recv {data.shape} {np.sum(data)}')
        if np.sum(data) == 0:
            break

print(f'rank{rank} on host {myhost} done')
    
