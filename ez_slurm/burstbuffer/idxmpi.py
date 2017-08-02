from psana import *
import numpy as np
import time

from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

t0 = time.time()
experimentName = 'cxid9114'
runNumber = '108'          
detInfo = 'CxiDs2.0:Cspad.0'

#experimentName = 'cxi10416'
#runNumber = '27'
#detInfo = 'DscCsPad'
evtNum = 0                  

t1 = time.time()
ds = DataSource('exp='+experimentName+':run='+runNumber+':idx')
t2 = time.time()                                                     
run = ds.runs().next()                                               
t3 = time.time()                                                     
det = Detector(detInfo)                                        
t4 = time.time()                                                     

times = run.times()
env = ds.env()
eventTotal = len(times)
t5 = time.time()

nEvents = 1000
nAllEvents = nEvents * size
selTimes = times[:nAllEvents]
myTimeStamp = [selTimes[i] for i in xrange(len(selTimes)) if (i+rank)%size == 0]
myTimes = np.zeros((nEvents,2))
#myEvnp.random.permutation(10)
t6 = time.time()
#mask = det.image(evt, det.mask(evt, calib=True, status=True, edges=True, central=True, unbond=True, unbondnbrs=True, unbondnbrs8=True))
#calib = np.load('/reg/data/ana14/cxi/cxitut13/scratch/yoon82/cxi10416/yoon82/psocake/r0027/cxi10416_0027_maxHits.npy')
#img = det.image(evt, calib)
for i,timestamp in enumerate(myTimeStamp):
    myTimes[i,0] = time.time()
    evt = run.event(timestamp)
    img = det.raw(evt)
    myTimes[i,1] = time.time()
t9 = time.time() # 0.17GB/s, theory: 10Gb/s=1.25GB/s

readRate = (4.5*nEvents/1000)/(t9-t6)
print 'Rank:%d'%(rank)+' Exp:'+experimentName+' Run:'+runNumber+' %d Events %6.2f s %6.2f GB/s'%(nEvents, t9-t6, readRate)
txtElapsed = '\n'.join(map(str, myTimes[:,1]-myTimes[:,0]))
with open('rank_%d.txt'%(rank),'w') as f:
  f.write(txtElapsed)
 
#from IPython import embed
#embed()
