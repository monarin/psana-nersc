
from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
myhost = MPI.Get_processor_name()
import numpy as np
import time
import sys

n = 5000
data_MB = float(sys.argv[1])
data_nbytes = int(data_MB*1e6)
st_init = MPI.Wtime()
if rank == 0:
    data = bytearray(b'b' * data_nbytes)
    data2 = bytearray(b'b' * data_nbytes)
    send_timings = []
    
    comm.Barrier()
    st = time.time()
    for i in range(n):
        comm.Send(data,dest=1) 

    for i in range(n):
        comm.Recv(data2, source=MPI.ANY_SOURCE)

    comm.Barrier()
    en = time.time()

else:
    data = bytearray(b'b' * data_nbytes)
    data2 = bytearray(b'b' * data_nbytes)
    comm.Barrier()
    for i in range(n):
        comm.Recv(data, source=MPI.ANY_SOURCE)

    for i in range(n):
        comm.Send(data2,dest=0) 
    comm.Barrier()

if rank == 0:
    rate = data_nbytes*n*2*1e-9/(en-st)
    print(f'data size (1 send): {data_nbytes*1e-6:.2f}MB total={en-st:.5f}s. rate={rate:.2f}GB/s')

