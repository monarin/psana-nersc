from mpi4py import MPI
import numpy as np
import os

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

comm.Barrier()
t_st = MPI.Wtime()

sendbuf = np.zeros(1, dtype='i') + 1
recvbuf = None
if rank == 0:
    recvbuf = np.empty([size, 1], dtype='i')
comm.Gather(sendbuf, recvbuf, root=0)

comm.Barrier()
t_en = MPI.Wtime()
if rank == 0:
    open(os.path.join(os.environ.get('SCRATCH'), "logc_%s.txt"%os.environ.get('SLURM_JOB_ID')), "wb").write('%d %f %f %f'%(np.sum(recvbuf), t_st, t_en, t_en-t_st))

