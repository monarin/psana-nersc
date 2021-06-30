import numpy as np
from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

data_MB = 50
data_nbytes = int(data_MB*1e6)
n_sends = 100

st = MPI.Wtime()

if rank == 0:
    data = bytearray(b'b' * data_nbytes)
    rankreq = np.empty(1, dtype='i')
    for j in range(n_sends):
        req = comm.Irecv(rankreq, source=MPI.ANY_SOURCE)
        req.Wait()

        req = comm.Isend(data, dest=rankreq[0])
        
        # Overlap communication
        #sum_i = 0
        #for i in range(100000):
        #    sum_i += i

        #print(f'loop{j} rank{rank} compute sum_i={sum_i}')

        # Wait for the last send to complete
        if j == n_sends - 1:
            while not req.Test():
                pass
    
    # Terminate clients
    for i in range(size-1):
        req = comm.Irecv(rankreq, source=MPI.ANY_SOURCE)
        req.Wait()
        req = comm.Isend(bytearray(), dest=rankreq[0])
        if i == size - 1:
            while not req.Test():
                pass


else:
    while True:
        comm.Isend(np.array([rank], dtype='i'), dest=0)
        info = MPI.Status()
        comm.Probe(source=0, status=info)
        count = info.Get_elements(MPI.BYTE)
        if count == 0: 
            break
        data = bytearray(count)
        req = comm.Irecv(data, source=0)
        req.Wait()

en = MPI.Wtime()

if rank == 0:
    rate = (data_nbytes*n_sends*1e-9)/(en-st)
    print(f'#clients={size-1} #sends={n_sends} size={data_nbytes*1e-6:.2f}MB total={data_nbytes*n_sends*1e-6:.2f}MB elapsed={en-st:.2f}s rate={rate:.2f}GB/s')
