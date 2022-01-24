from psana import DataSource

import logging
logger = logging.getLogger('psana.psexp')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
xtc_dir='/cds/data/drpsrcf/tst/tstx00417/xtc'
ds = DataSource(exp='tstx00417', run=214, dir=xtc_dir, live=True)

for run in ds.runs():
    for evt in run.events():
        print(evt.timestamp)
