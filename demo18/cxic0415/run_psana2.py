import os, time
from psana import DataSource
from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()

def filter(evt):
    return True

os.environ['PS_CALIB_DIR'] = "/global/cscratch1/sd/monarin/psana-nersc/demo18/cxic0415/input"
os.environ['PS_SMD_NODES'] = '32'
os.environ['PS_SMD_N_EVENTS'] = '1000'
xtc_dir = "/global/cscratch1/sd/monarin/d/psdm/cxi/cxic0415/xtc2"
ds = DataSource('exp=cxic0415:run=50:dir=%s'%(xtc_dir), filter=filter, det_name='DscCsPad')

mylog = ""
for run in ds.runs():
    det = ds.Detector(ds.det_name)
    for evt in run.events():
        raw = det.raw(evt)
        ped = det.pedestals(run)
        gain_mask = det.gain_mask(run, gain=6.85)
        calib = det.calib(evt)
        raw_data = det.raw_data(evt)
	mylog += "%s\n"%(time.time())

with open('/global/cscratch1/sd/monarin/psana-nersc/demo18/cxic0415/out/%d_debug.txt'%(rank), 'w') as f:
    f.write(mylog)

