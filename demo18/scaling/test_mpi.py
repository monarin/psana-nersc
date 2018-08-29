from mpi4py import MPI
comm=MPI.COMM_WORLD
rank=comm.Get_rank()
size=comm.Get_size()

data = rank
data = comm.gather(data, root=0)
if rank == 0:
  for i in range(size):
    assert data[i] == i
else:
  assert data is None

if rank == 0:
  print(data)
