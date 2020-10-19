import os, time, glob, sys
import pstats, cProfile
import pyximport
pyximport.install()
from psana.smdreader import SmdReader
from psana.dgram import Dgram
import numpy as np

chunksize = 0x1000000
max_events = 0
smd0_batch_size = 1000

import logging
logging.basicConfig(level=logging.DEBUG,
                format='(%(threadName)-10s) %(message)s',
                        )

os.environ['PS_SMD_MAX_RETRIES'] = '0'
def run_smd0():
    #filenames = glob.glob('/reg/neh/home/monarin/lcls2/psana/psana/tests/.tmp/smalldata/*.xtc2')
    #filenames = glob.glob('/ffb01/mona/xtc2/.tmp/smalldata/*.xtc2')
    #filenames = glob.glob('/ffb01/mona/xtc2/.tmp/smalldata/*.xtc2')
    filenames = glob.glob('/gpfs/alpine/scratch/monarin/chm137/data/.tmp/smalldata/*.xtc2')

    fds = np.array([os.open(filename, os.O_RDONLY) for filename in filenames], dtype=np.int32)

    # Move file ptrs to datagram part
    configs = [Dgram(file_descriptor=fd) for fd in fds]
    beginRun = [Dgram(config=config) for config in configs]
    
    limit = len(filenames)
    if len(sys.argv) > 1:
        limit = int(sys.argv[1])
    
    st = time.time()
    smdr = SmdReader(fds[:limit], chunksize)
    processed_events = 0
    is_done = False
    while not is_done:
        if smdr.is_complete():
            mmrv_bufs, mmrv_step_bufs = smdr.view(batch_size=smd0_batch_size)
            processed_events += smdr.view_size
        else:
            smdr.get()
            if not smdr.is_complete():
                is_done = True

        #print(f'processed events={processed_events}')
        if processed_events >= max_events and max_events > 0:
            is_done = True

    
    en = time.time()
    print("#Events: %d Elapsed Time (s): %f Rate (MHz): %f"%(processed_events, (en-st), processed_events/((en-st)*1e6)))

if __name__ == "__main__":
    run_smd0()
    #cProfile.runctx("run_smd0()", globals(), locals(), "Profile.prof")
    #s = pstats.Stats("Profile.prof")
    #s.strip_dirs().sort_stats("time").print_stats()
