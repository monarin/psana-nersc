from psana import DataSource
import os

xtc_dir = '/cds/data/drpsrcf/rix/rixl1013320/xtc'
ds = DataSource(exp='rixl1013320', run=93, dir=xtc_dir)
#ds = DataSource(files='/cds/data/drpsrcf/rix/rixl1013320/xtc/smalldata/rixl1013320-r0093-s000-c000.smd.xtc2')
run = next(ds.runs())
for i_evt, evt in enumerate(run.events()):
    print(f'{i_evt} evt:{evt.timestamp}')
