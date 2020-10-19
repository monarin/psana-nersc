from psana.psexp import SmdReaderManager, PrometheusManager
from psana.dgram import Dgram
import numpy as np
import glob, sys, os, time

#import logging
#logging.basicConfig(level=logging.DEBUG,
#                format='(%(threadName)-10s) %(message)s',
#                        )

chunksize = 0x1000000
max_events = 0

class Run(object):
    def __init__(self, fds):
        self.max_events = 0
        self.prom_man = PrometheusManager(0)
        self.batch_size = 1000
        self.filter_callback = None
        self.destination = None
        self.smd_fds = fds

def run_smd0():
    filenames = glob.glob('/gpfs/alpine/scratch/monarin/chm137/data/.tmp/smalldata/*.xtc2')

    fds = np.array([os.open(filename, os.O_RDONLY) for filename in filenames], dtype=np.int32)

    run = Run(fds)
    smdr_man = SmdReaderManager(run)
    run.configs = smdr_man.get_next_dgrams()
    run.beginruns = smdr_man.get_next_dgrams(configs=run.configs)
    
    st = time.time()
    processed_events = 0
    for i, chunk in enumerate(smdr_man.chunks()):
    #for i, batch in enumerate(smdr_man):
        processed_events += smdr_man.got_events

    en = time.time()
    print("#Events: %d Elapsed Time (s): %f Rate (MHz): %f"%(processed_events, (en-st), processed_events/((en-st)*1e6)))

if __name__ == "__main__":
    run_smd0()
