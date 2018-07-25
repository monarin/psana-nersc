from psana import *
import matplotlib.pyplot as plt
from xfel.cxi.cspad_ana import cspad_tbx
import numpy as np
import sys

#ds = DataSource('exp=xpptut15:run=54:smd')
exp=sys.argv[1]
detnames=sys.argv[2]
run_no = int(sys.argv[3])
dark_run = int(sys.argv[4])
ds = DataSource('exp=%s:run=%s'%(exp,run_no))
det = Detector(detnames)

"""
times = ds.runs().next().times()
eventList = [0,1,2]
for i,t in enumerate(times):
  if i > 2: break
  print t.seconds(),t.nanoseconds()

tsList = [cspad_tbx.evt_timestamp((t.seconds(),t.nanoseconds()/1e6)) for i,t in enumerate(times) if i in eventList]
strTs = ' debug.event_timestamp='.join(['']+tsList)
print tsList
print strTs
"""

for nevent,evt in enumerate(ds.events()):
    if nevent>=1: break
    # includes pedestal subtraction, common-mode correction, bad-pixel
    # suppresion, and uses geometry to position the multiple CSPAD panels
    # into a 2D image
    print 'Fetching event number: %d from run %d write out dark_run: %d'%(nevent, run_no, dark_run)
    img = det.image(evt)
    
    run = evt.run()
    dark = det.pedestals(run)
    dark.dump('%s-end.npy'%dark_run)
    #plt.imshow(img,vmin=-2,vmax=2)
    #plt.show()
print 'Done.'
