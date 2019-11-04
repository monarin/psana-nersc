import os, time, glob, sys
import pstats, cProfile
import pyximport
pyximport.install()
from psana.smdreader import SmdReader
from psana.dgram import Dgram

max_events = 10000000
def run_smd0():
    filenames = glob.glob('/ffb01/mona/xtc2/.tmp/smalldata/*.xtc2')
    fds = [os.open(filename, os.O_RDONLY) for filename in filenames]

    # Move file ptrs to datagram part
    configs = [Dgram(file_descriptor=fd) for fd in fds]
    
    limit = len(filenames)
    if len(sys.argv) > 1:
        limit = int(sys.argv[1])
    
    st = time.time()
    smdr = SmdReader(fds[:limit])
    got_events = -1
    n_events = 10000
    processed_events = 0
    smdr.get(n_events)
    while smdr.got_events != 0:
        processed_events += smdr.got_events
        if processed_events >= max_events:
            break
        
        smdr.get(n_events)

    en = time.time()
    print("#Events: %d Elapsed Time (s): %f Rate (MHz): %f"%(processed_events, (en-st), processed_events/((en-st)*1e6)))

if __name__ == "__main__":
    run_smd0()
    #cProfile.runctx("run_smd0()", globals(), locals(), "Profile.prof")
    #s = pstats.Stats("Profile.prof")
    #s.strip_dirs().sort_stats("time").print_stats()
