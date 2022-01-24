import os, time, glob, sys
import numpy as np
from psana.psexp import SmdReaderManager, PrometheusManager
from psana.psexp.ds_base import DsParms

#import logging
#logging.basicConfig(filename='dev_smd0.log')
#logger = logging.getLogger('psana.psexp.smdreader_manager')
#logger.setLevel(logging.DEBUG)
#ch = logging.StreamHandler()
#ch.setLevel(logging.DEBUG)
#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#ch.setFormatter(formatter)
#logger.addHandler(ch)

max_events = 0
os.environ['PS_SMD_MAX_RETRIES'] = '0'
os.environ['PS_SMD_N_EVENTS'] = '10000'
os.environ['PS_SMD_CHUNKSIZE'] = '16777216'
os.environ['PS_SMD0_NUM_THREADS'] = '32'

def run_smd0():
    smd_dir = '/cds/data/drpsrcf/users/monarin/xtcdata/10M60n/xtcdata/smalldata'
    #smd_dir = '/cds/data/drpsrcf/users/monarin/tmoc00118/xtc/smalldata'
    filesize = 760057400
    n_files = int(sys.argv[1])
    filenames = [None] * n_files
    for i in range(n_files):
        filenames[i] = os.path.join(smd_dir,f'data-r0001-s{str(i).zfill(2)}.smd.xtc2')
        #filenames[i] = os.path.join(smd_dir,f'tmoc00118-r0463-s{str(i).zfill(3)}-c000.smd.xtc2')
        #filenames[i] = os.path.join(smd_dir,f'tmolv9418-r0175-s{str(i).zfill(3)}-c000.smd.xtc2')

    smd_fds = np.array([os.open(filename, os.O_DIRECT) for filename in filenames], dtype=np.int32)

    st = time.time()
    prom_man = PrometheusManager(os.getpid())
    dsparms = DsParms(batch_size=1, # bigdata batch size 
            max_events=max_events, 
            filter=0, 
            destination=0, 
            prom_man=prom_man, 
            max_retries=0,
            live=False,
            found_xtc2_callback=0,
            timestamps  = np.empty(0, dtype=np.uint64)         
            )
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
    print(f"#Smdfiles: {n_files} #Events: {processed_events} Elapsed Time (s): {en-st:.2f} Rate (MHz): {processed_events/((en-st)*1e6):.2f} Bandwidth(GB/s):{filesize*n_files*1e-9/(en-st):.2f}")

if __name__ == "__main__":
    run_smd0()
