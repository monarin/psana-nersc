import os
from psana import DataSource
import time
from mpi4py import MPI
comm = MPI.COMM_WORLD

def filter(evt):
    return True

xtc_dir = "/global/cscratch1/sd/monarin/d/psdm/cxi/cxic0415/xtc2" 

comm.Barrier()
t_st = MPI.Wtime()
ds = DataSource('exp=xpptut13:run=1:dir=%s'%(xtc_dir), filter=filter, batch_size=1)

det = None
if ds.nodetype == "bd":
    det = ds.Detector("DscCsPad")

for run in ds.runs():
    t_evt_0 = time.time()
    for evt in run.events():
        t_evt_st = time.time()
        if det:
            raw = det.raw(evt)
        t_evt_en = time.time()
        print("PROFILE_EVT %f"%(t_evt_st - t_evt_0))
        t_evt_0 = time.time()

comm.Barrier()
t_en =MPI.Wtime()
if comm.Get_rank() == 0:
    print("PROFILE_ALL %f"%(t_en-t_st))
