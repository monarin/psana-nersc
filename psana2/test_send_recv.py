from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
myhost = MPI.Get_processor_name()
import numpy as np
import time

n = 10
if rank == 0:
    #data = np.arange(1000000, dtype='i')
    #data_nbytes = 100000000
    data_nbytes = int(500e3)
    data = bytearray(b'b' * data_nbytes)
    rankreq = np.empty(1, dtype='i')
    send_timings = []
    for i in range(n):
        comm.Recv(rankreq, source=MPI.ANY_SOURCE)
        st = time.monotonic()
        comm.Send(data, dest=rankreq[0])
        en = time.monotonic()
        print(f'send#{i} tot={en-st:.3}s. rate={(data_nbytes*1e-9)/(en-st):.2f}GB/s') 
        send_timings.append(en-st)


    for i in range(size-1):
        comm.Recv(rankreq, source=MPI.ANY_SOURCE)
        comm.Send(bytearray(), dest=rankreq[0])

else:
    while True:
        comm.Send(np.array([rank], dtype='i'), dest=0)

        info = MPI.Status()
        comm.Probe(source=0, status=info)
        count = info.Get_elements(MPI.BYTE)
        data = bytearray(count)
        comm.Recv(data, source=0)
        if count == 0:
            break

if rank == 0:
    tot_time = np.sum(send_timings)
    rates = (data_nbytes*1e-9) / np.asarray(send_timings)
    print(f'send timing #sends: {len(send_timings)} data: {data_nbytes/1e9:.2f}GB rate avg: {np.mean(rates):.2f}GB/s max: {np.max(rates):.2f}GB/s min: {np.min(rates):.2f}GB/s') 
    
