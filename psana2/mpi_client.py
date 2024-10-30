import time

import numpy as np
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
myhost = MPI.Get_processor_name()
print(f"rank{rank} size:{size} on host:{myhost}")

data_MB = 50
data_nbytes = int(data_MB * 1e6)
n_sends = 200

st = MPI.Wtime()

if rank == 0:
    data = bytearray(b"b" * data_nbytes)
    rankreq = np.empty(1, dtype="i")
    for j in range(n_sends):
        comm.Recv(rankreq, source=MPI.ANY_SOURCE)

        comm.Send(data, dest=rankreq[0])

        # Overlap communication
        st_compute = time.time()
        sum_i = 0
        for i in range(10000):
            sum_i += i
        en_compute = time.time()
        # print(f'loop{j} rank{rank} compute sum_i={sum_i} took={(en_compute-st_compute)*1e3:.2f}ms')

    # Terminate clients
    for i in range(size - 1):
        comm.Recv(rankreq, source=MPI.ANY_SOURCE)
        comm.Send(bytearray(), dest=rankreq[0])

else:
    while True:
        comm.Send(np.array([rank], dtype="i"), dest=0)
        info = MPI.Status()
        comm.Probe(source=0, status=info)
        count = info.Get_elements(MPI.BYTE)
        if count == 0:
            break
        data = bytearray(count)
        comm.Recv(data, source=0)

en = MPI.Wtime()

if rank == 0:
    rate = (data_nbytes * n_sends * 1e-9) / (en - st)
    print(
        f"#clients={size-1} #sends={n_sends} size={data_nbytes*1e-6:.2f}MB total={data_nbytes*n_sends*1e-6:.2f}MB elapsed={en-st:.2f}s rate={rate:.2f}GB/s"
    )
