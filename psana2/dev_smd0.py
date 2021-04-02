import os, time, glob, sys
import numpy as np
from psana.psexp import SmdReaderManager, PrometheusManager
from psana.psexp.ds_base import DsParms

max_events = 0
os.environ['PS_SMD_MAX_RETRIES'] = '0'
os.environ['PS_SMD_N_EVENTS'] = '10000'
os.environ['PS_SMD_CHUNKSIZE'] = '16777216'

def run_smd0():
    #filenames = glob.glob('/cds/data/drpsrcf/users/monarin/xtcdata/smalldata/*.xtc2')
    filenames = glob.glob('/cds/data/drpsrcf/users/monarin/xtcdata/100M/xtcdata/smalldata//*.xtc2')

    smd_fds = np.array([os.open(filename, os.O_RDONLY) for filename in filenames], dtype=np.int32)

    n_files = len(filenames)
    if len(sys.argv) > 1:
        n_files = int(sys.argv[1])
    
    st = time.time()
    prom_man = PrometheusManager(os.getpid())
    dsparms = DsParms(batch_size=1, # bigdata batch size 
            max_events=max_events, 
            filter=0, 
            destination=0, 
            prom_man=prom_man, 
            max_retries=0)
    smdr_man = SmdReaderManager(smd_fds[:n_files], dsparms)
    for i, (smd_chunk, step_chunk) in enumerate(smdr_man.chunks()):
        if not (smd_chunk or step_chunk): break
        found_endrun = smdr_man.smdr.found_endrun()
        if found_endrun:
            print(f'found EndRun')
            break
    
    en = time.time()
    processed_events = smdr_man.processed_events
    print("#Events: %d Elapsed Time (s): %f Rate (MHz): %f"%(processed_events, (en-st), processed_events/((en-st)*1e6)))

if __name__ == "__main__":
    run_smd0()
