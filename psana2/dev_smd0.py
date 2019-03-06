import os, time, glob, sys
import pstats, cProfile
import pyximport
pyximport.install()
from psana.smdreader import SmdReader
from psana.dgram import Dgram

def run_smd0():
    filenames = glob.glob('/reg/d/psdm/xpp/xpptut15/scratch/mona/xtc2/smalldata/*.smd.xtc2')
    epics_file = '/reg/d/psdm/xpp/xpptut15/scratch/mona/xtc2/data-r0001-epc.xtc2'
    #filenames = glob.glob('/u1/mona/smalldata/*.smd.xtc2')
    #filenames = glob.glob('.tmp/smalldata/*r0001*.xtc2')
    fds = [os.open(filename, os.O_RDONLY) for filename in filenames]
    epics_fd = os.open(epics_file, os.O_RDONLY)

    # Move file ptrs to datagram part
    configs = [Dgram(file_descriptor=fd) for fd in fds]
    epics_config = Dgram(file_descriptor=epics_fd)
    
    limit = len(filenames)
    if len(sys.argv) > 1:
        limit = int(sys.argv[1])
    
    st = time.time()
    smdr = SmdReader(fds[:limit])
    got_events = -1
    n_events = 1000
    processed_events = 0
    while got_events != 0:
        smdr.get(n_events)
        got_events = smdr.got_events
        processed_events += got_events
    #print("processed_events: %d"%processed_events)
    en = time.time()
    print("#Events: %d Elapsed Time (s): %f Rate (MHz): %f"%(processed_events, (en-st), processed_events/((en-st)*1e6)))

if __name__ == "__main__":
    run_smd0()
    #cProfile.runctx("run_smd0()", globals(), locals(), "Profile.prof")
    #s = pstats.Stats("Profile.prof")
    #s.strip_dirs().sort_stats("time").print_stats()
