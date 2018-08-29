import os
from psana import DataSource
import time
from mpi4py import MPI
comm = MPI.COMM_WORLD

def filter(evt):
    return True

xtc_dir = "/global/cscratch1/sd/monarin/d/psdm/cxi/cxid9114/xtc2" 

comm.Barrier()
t_st = MPI.Wtime()
ds = DataSource('exp=xpptut13:run=1:dir=%s'%(xtc_dir), filter=filter, batch_size=100)

#print("PROFILE_GOT_DS")

det = None
if ds.nodetype == "bd":
    det = ds.Detector("CxiDs2")
    #print("PROFILE_GOT_DET")

for run in ds.runs():
    t_evt_0 = time.time()
    for i, evt in enumerate(run.events()):
        #print("PROFILE_GOT_1_EVT %d"%i)
        t_evt_st = time.time()
        if det:
            raw = det.raw(evt)
            #if raw is None:
	    #   print("PROFILE_GOT_NONE_RAW")
        t_evt_en = time.time()
        #print("PROFILE_EVT %d %f"%(i, t_evt_st - t_evt_0))
        t_evt_0 = time.time()

comm.Barrier()
t_en =MPI.Wtime()
#if comm.Get_rank() == 0:
#    print("PROFILE_ALL %f"%(t_en-t_st))

#print("PROFILE_DONE")
