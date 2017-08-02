import psana
import numpy as np
import time
#import matplotlib.pyplot as plt
import h5py

t0 = time.time()
experimentName = 'cxid9114'
runNumber = '108'
detInfo = 'CxiDs2.0:Cspad.0'
evtNum = 0

t1 = time.time()
ds = psana.DataSource('exp='+experimentName+':run='+runNumber+':idx')
t2 = time.time()
run = ds.runs().next()
t3 = time.time()
det = psana.Detector(detInfo)
t4 = time.time()

times = run.times()
env = ds.env()
eventTotal = len(times)
t5 = time.time()

myTimes = np.zeros((1000,2))
#myEvnp.random.permutation(10)
t6 = time.time()
#mask = det.image(evt, det.mask(evt, calib=True, status=True, edges=True, central=True, unbond=True, unbondnbrs=True, unbondnbrs8=True))
#calib = np.load('/reg/data/ana14/cxi/cxitut13/scratch/yoon82/cxi10416/yoon82/psocake/r0027/cxi10416_0027_maxHits.npy')
#img = det.image(evt, calib)
for i in range(1000):
    myTimes[i,0] = time.time()
    evt = run.event(times[i])
    img = det.raw(evt)
    myTimes[i,1] = time.time()
t9 = time.time() # 0.17GB/s, theory: 10Gb/s=1.25GB/s

print t9-t6
