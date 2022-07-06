from mpi4py import MPI
comm = MPI.COMM_WORLD

# For mpirun -n 5
rank = comm.Get_rank()
size = comm.Get_size()
group = comm.Get_group()

# Only for rank 0, 1, 2 (exclude rank 3, 4)
smd_group = group.Excl([3,4])
smd_comm = comm.Create(smd_group)

# Two bd groups: (1,3) and (2,4)
bd_group_1 = group.Excl([0,2,4])
bd_comm_1 = comm.Create(bd_group_1)
bd_group_2 = group.Excl([0,1,3])
bd_comm_2 = comm.Create(bd_group_2)

import numpy as np

def wait_for(requests):
    status = [MPI.Status() for i in range(len(requests))]
    MPI.Request.Waitall(requests, status)


if rank == 0:
    # Rank 0 waits on Terminate signal
    t_rankreq = np.empty(1, dtype='i')
    t_req = comm.Irecv(t_rankreq, source=MPI.ANY_SOURCE)

    # Rank 0 sends data to rank 1 and 2 
    data = np.ones([10,3], dtype=float)
    rankreq = np.empty(1, dtype='i')
    mpi_requests = [MPI.REQUEST_NULL for i in range(smd_comm.Get_size() - 1)]
    for d in data:
        req = smd_comm.Irecv(rankreq, source=MPI.ANY_SOURCE)
        req.Wait()
        mpi_requests[rankreq[0]-1] = smd_comm.Isend(d, dest=rankreq[0])
        print(f'Rank 0 sent {d} to rank {rankreq[0]}')

        t_req_test = t_req.Test()
        if t_req_test: 
            print(f'Rank 0 got terminating signal from {t_rankreq[0]} t_req_test:{t_req_test}')
            break
     
    wait_for(mpi_requests)

    # Kills waiting ebs
    mpi_requests = [MPI.REQUEST_NULL for i in range(smd_comm.Get_size() - 1)]
    for i in range(smd_comm.Get_size()-1):
        req = smd_comm.Irecv(rankreq, source=MPI.ANY_SOURCE)
        req.Wait()
        mpi_requests[rankreq[0]-1] = smd_comm.Isend(bytearray(), dest=rankreq[0])
        print(f'Rank 0 sent kill to rank {rankreq[0]}')
    wait_for(mpi_requests)

elif rank in (1,2):
    # Get the correct comm for each bd
    if rank == 1:
        my_comm = bd_comm_1
    else:
        my_comm = bd_comm_2

    rankreq = np.empty(1, dtype='i')
    mpi_requests = [MPI.REQUEST_NULL for i in range(my_comm.Get_size() - 1)]
    while True:
        # Receives data from Rank 0
        smd_comm.Isend(np.array([smd_comm.Get_rank()], dtype='i'), dest=0)
        info = MPI.Status()
        smd_comm.Probe(source=0, status=info)
        count = info.Get_elements(MPI.BYTE)
        d = bytearray(count)
        req = smd_comm.Irecv(d, source=0)
        req.Wait()
        
        print(f'EBRank {rank} got {count} bytes from Rank 0')
        if count == 0: break
        
        req = my_comm.Irecv(rankreq, source=MPI.ANY_SOURCE)
        req.Wait()
        mpi_requests[rankreq[0]-1] = my_comm.Isend(d, dest=rankreq[0])
        print(f'EBRank {rank} sent {count} bytes to rank {rankreq[0]}')
    wait_for(mpi_requests)
    
    # Kills waiting ebs
    mpi_requests = [MPI.REQUEST_NULL for i in range(my_comm.Get_size() - 1)]
    for i in range(my_comm.Get_size()-1):
        req = my_comm.Irecv(rankreq, source=MPI.ANY_SOURCE)
        req.Wait()
        mpi_requests[rankreq[0]-1] = my_comm.Isend(bytearray(), dest=rankreq[0])
        print(f'EBRank {rank} sent kill to rankreq {rankreq[0]}')
    wait_for(mpi_requests)

elif rank in (3,4):
    if rank == 3:
        my_comm = bd_comm_1
    else:
        my_comm = bd_comm_2

    cn_recvs = 0
    while True:
        # Receives data from Eb
        my_comm.Isend(np.array([my_comm.Get_rank()], dtype='i'), dest=0)
        info = MPI.Status()
        my_comm.Probe(source=0, status=info)
        count = info.Get_elements(MPI.BYTE)
        d = bytearray(count)
        req = my_comm.Irecv(d, source=0)
        req.Wait()

        print(f'BDRank {rank} got {count} bytes')
        if count == 0: break

        cn_recvs += 1
        if cn_recvs == 3:
            print(f'BDRank {rank} got {cn_recvs} packages. Exit.')
            comm.Isend(np.array([rank], dtype='i'), dest=0)



