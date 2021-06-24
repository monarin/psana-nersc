import os, time, glob, sys
import numpy as np
<<<<<<< Updated upstream
from psana.psexp import SmdReaderManager, PrometheusManager
from psana.psexp.ds_base import DsParms

#import logging
#logger = logging.getLogger('psana.psexp.ds_base')
#logger.setLevel(logging.DEBUG)
#ch = logging.StreamHandler()
#ch.setLevel(logging.DEBUG)
#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#ch.setFormatter(formatter)
#logger.addHandler(ch)

max_events = 0
os.environ['PS_SMD_MAX_RETRIES'] = '0'
os.environ['PS_SMD_N_EVENTS'] = '1000'
os.environ['PS_SMD_CHUNKSIZE'] = '16777216'

def run_smd0():
    #smd_dir = '/cds/data/drpsrcf/users/monarin/xtcdata/10M60n/xtcdata/smalldata'
    smd_dir = '/reg/d/psdm/rix/rixx43518/xtc/smalldata/'
    n_files = int(sys.argv[1])
    filenames = [None] * n_files
    for i in range(n_files):
        #filenames[i] = os.path.join(smd_dir,f'data-r0001-s{str(i).zfill(2)}.smd.xtc2')
        filenames[i] = os.path.join(smd_dir,f'rixx43518-r0319-s{str(i).zfill(3)}-c000.smd.xtc2')
        print(i, filenames[i])

    smd_fds = np.array([os.open(filename, os.O_RDONLY) for filename in filenames], dtype=np.int32)

    st = time.time()
    prom_man = PrometheusManager(os.getpid())
    dsparms = DsParms(batch_size=1, # bigdata batch size 
            max_events=max_events, 
            filter=0, 
            destination=0, 
            prom_man=prom_man, 
            max_retries=0,
            live=False,
            found_xtc2_callback=0)
    smdr_man = SmdReaderManager(smd_fds[:n_files], dsparms)
    for i_chunk in enumerate(smdr_man.chunks()):
        if not smdr_man.got_events: break
        found_endrun = smdr_man.smdr.found_endrun()
        if found_endrun:
            print(f'found EndRun')
            break
    
    print(f'total search time: {smdr_man.smdr.total_time}')
    en = time.time()
    processed_events = smdr_man.processed_events
    print("#Smdfiles: %d #Events: %d Elapsed Time (s): %f Rate (MHz): %f"%(n_files,processed_events, (en-st), processed_events/((en-st)*1e6)))

if __name__ == "__main__":
    run_smd0()
