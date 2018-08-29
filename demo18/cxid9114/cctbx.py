# NOTE:
# This example only works with psana2-python2.7 environment

import os
from psana import DataSource

def filter(evt):
        return True

os.environ['PS_CALIB_DIR'] = "/global/cscratch1/sd/monarin/psana-nersc/demo18/cxid9114/input"
os.environ['PS_SMD_NODES'] = '3'
os.environ['PS_SMD_N_EVENTS'] = '100'
xtc_dir = "/global/cscratch1/sd/monarin/d/psdm/cxi/cxid9114/xtc2"
ds = DataSource('exp=cxid9114:run=1:dir=%s'%(xtc_dir), filter=filter, max_events=2700)
det = None
if ds.nodetype == "bd":
    det = ds.Detector("DsdCsPad")

for run in ds.runs():
    for evt in run.events():
        if det:
            raw = det.raw(evt)
            ped = det.pedestals(run)
            gain_mask = det.gain_mask(run, gain=6.85)
            print("GOT_EVT")#print(raw.shape, ped.shape, gain_mask.shape)
