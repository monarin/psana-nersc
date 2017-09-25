from psana import *
import sys

exp = sys.argv[1]
runNo = sys.argv[2]
ds = DataSource('exp='+exp+':run='+runNo+':smd')
det = Detector('CxiDs2.0:Cspad.0')
nevent = 0
for evt in ds.events():
  nevent +=1 
  if nevent == 3: break
  calib = det.calib(evt)
  print calib.shape
"""
ds = DataSource('exp=cxid9114:run=108:rax')
det = Detector('CxiDs2.0:Cspad.0')
nevent = 0
for evt in ds.events():
  nevent +=1
  if nevent == 3: break
  calib = det.calib(evt)
  print calib.shape
"""

