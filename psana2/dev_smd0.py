import os, time, glob, sys
import pstats, cProfile
import pyximport
pyximport.install()
from psana.smdreader import SmdReader
from psana.dgram import Dgram
import numpy as np

chunksize = 0x1000000
max_events = 100
smd0_batch_size = 1

def run_smd0():
    filenames = glob.glob('/reg/neh/home/monarin/psana-nersc/psana2/.tmp/smalldata/*.xtc2')
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
    got_events = -1
    processed_events = 0
    offsets = np.zeros(limit,dtype=np.uint64)


    how_many = smd0_batch_size
    to_be_read = max_events - processed_events
    if to_be_read < how_many:
        how_many = to_be_read

    smdr.get(how_many)
    while smdr.got_events > 0:
#        for i in range(limit):
#            view = smdr.view(i)
#            """
#            if view:
#                cn_dgrams = 0
#                while offsets[i] < view.shape[0]:
#                    d = Dgram(config=configs[i], view=view, offset=offsets[i])
#                    print(f' buf{i} d_id: {cn_dgrams} d_ts {d.timestamp() & 0xffffffff}')
#                    offsets[i] += d._size
#                    cn_dgrams += 1
#                #print(f'smdr_man got {memoryview(view).nbytes}')
#            else:
#                #print(f' buf[{i} empty')
#                pass
#            """
#
#
#
        processed_events += smdr.got_events
        if processed_events >= max_events:
            break
        
        how_many = smd0_batch_size
        to_be_read = max_events - processed_events
        if to_be_read < how_many:
            how_many = to_be_read

        smdr.get(how_many)
        
        offsets[:] = 0
    """
    while smdr.got_events != 0:
        if smdr.got_events > 0:
            processed_events += smdr.got_events
            if processed_events >= max_events:
                break
        for i in range(limit):
            smdr.view(i)

        smdr.get(n_events)
        print(f'smdr.got_events={smdr.got_events}')
    """
    en = time.time()
    print("#Events: %d Elapsed Time (s): %f Rate (MHz): %f"%(processed_events, (en-st), processed_events/((en-st)*1e6)))

if __name__ == "__main__":
    run_smd0()
    #cProfile.runctx("run_smd0()", globals(), locals(), "Profile.prof")
    #s = pstats.Stats("Profile.prof")
    #s.strip_dirs().sort_stats("time").print_stats()
