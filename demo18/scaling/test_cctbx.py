import os
from psana import DataSource
import time

"""
from mpi4py import MPI
comm = MPI.COMM_WORLD

def filter(evt):
    return True

comm.Barrier()
t_st = MPI.Wtime()
os.environ['PS_CALIB_DIR'] = "/global/cscratch1/sd/monarin/psana-nersc/demo18/cxic0415/input"
xtc_dir = "/global/cscratch1/sd/monarin/d/psdm/cxi/cxic0415/xtc2"
ds = DataSource('exp=cxic0415:run=1:dir=%s'%(xtc_dir), filter=filter, batch_size=100)

det = None
if ds.nodetype == "bd":
    det = ds.Detector("DscCsPad")

for run in ds.runs():
    t_evt_0 = time.time()
    for evt in run.events():
        if det:
            t_evt_st = time.time()
            raw = det.raw(evt)
            ped = det.pedestals(run)
            gain_mask = det.gain_mask(run, gain=1.0)
            img =gain_mask * (raw - ped)
            #print("PROFILE_EVT %f"%(t_evt_st-t_evt_0))
            t_evt_0 = time.time()

comm.Barrier()
t_en = MPI.Wtime()
if comm.Get_rank() == 0:
    print("PROFILE_ALL %f"%(t_en-t_st))
"""
from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
print(rank, size)
