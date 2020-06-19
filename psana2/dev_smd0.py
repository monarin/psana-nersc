import os, time, glob, sys
import pstats, cProfile
import pyximport
pyximport.install()
from psana.smdreader import SmdReader
from psana.dgram import Dgram
import numpy as np

chunksize = 0x1000000
max_events = 10
smd0_batch_size = 1

def run_smd0():
    filenames = glob.glob('/reg/neh/home/monarin/tmp/data/smalldata/*.xtc2')
    #filenames = glob.glob('/ffb01/mona/.tmp/smalldata/*.xtc2')

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

    while smdr.get():
        mmrv_bufs, mmrv_step_bufs = smdr.view()
    
    en = time.time()
    print("#Events: %d Elapsed Time (s): %f Rate (MHz): %f"%(processed_events, (en-st), processed_events/((en-st)*1e6)))

if __name__ == "__main__":
    run_smd0()
    #cProfile.runctx("run_smd0()", globals(), locals(), "Profile.prof")
    #s = pstats.Stats("Profile.prof")
    #s.strip_dirs().sort_stats("time").print_stats()
