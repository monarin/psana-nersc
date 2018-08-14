import os
from psana import DataSource
import time
from mpi4py import MPI
comm = MPI.COMM_WORLD

def filter(evt):
    return True

# Usecase#1 : two iterators
xtc_dir = "/global/cscratch1/sd/monarin/testxtc2"

comm.Barrier()
t_st = MPI.Wtime()
ds = DataSource('exp=xpptut13:dir=%s'%(xtc_dir), filter=filter, batch_size=100)
#beginJobCode
for run in ds.runs():
    #beginRunCode
    t_evt_0 = time.time()
    for i, evt in enumerate(run.events()):
        if i >= 20000: break
        t_evt_st = time.time()
        for d in evt:
            pass
        t_evt_en = time.time()
        print("PROFILE_EVT %f"%(t_evt_st - t_evt_0))
        t_evt_0 = time.time()
    #endRunCode
#endJobCode

comm.Barrier()
t_en =MPI.Wtime()
if comm.Get_rank() == 0:
    print("PROFILE_ALL %f"%(t_en-t_st))
