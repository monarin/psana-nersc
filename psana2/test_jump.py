from psana import DataSource
import numpy as np
timestamps = np.array([4194783241933859761,4194783249723600225,4194783254218190609,4194783258712780993], dtype=np.uint64)
ds = DataSource(exp='tmoc00118', run=222, dir='/cds/data/psdm/prj/public01/xtc', 
        timestamps=timestamps)
myrun = next(ds.runs())
opal = myrun.Detector('tmo_atmopal')
for nevt, evt in enumerate(myrun.events()):
    img = opal.raw.image(evt)
    print(nevt, evt.timestamp, img.shape)
