from psana import DataSource
import os

import logging
logger = logging.getLogger('psana.psexp.smdreader_manager')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

# Original data (smaller size)
#xtc_dir = '/cds/data/drpsrcf/rix/rixl1013320/xtc'

# New duplicated data
xtc_dir = '/cds/data/drpsrcf/users/monarin/rixl1013320/xtc'
max_events = 100000
ds = DataSource(exp='rixl1013320', run=93, dir=xtc_dir, max_events=max_events)
run = next(ds.runs())
for i_evt, evt in enumerate(run.events()):
    if i_evt % 1000 == 0:
        print(f'{i_evt} evt:{evt.timestamp}')
