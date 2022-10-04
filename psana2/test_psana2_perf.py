# Running this script on psffb
# PS_EB_NODES=1 PS_SMD_N_EVENTS=10000 SLURM_HOSTFILE=slurm_hosts srun -o xx --partition=anaq --exclusive python test_psana2_perf.py
# or
# `which mpirun` -n 33 --hostfile openmpi_hosts --mca btl_openib_allow_ib 1 ./run_slac.sh

from psana import DataSource
import os, time, sys
import numpy as np

from mpi4py import MPI
comm=MPI.COMM_WORLD
rank=comm.Get_rank()
size=comm.Get_size()

comm.Barrier()
st = MPI.Wtime()

max_events = 0
if len(sys.argv) > 1:
    max_events = int(sys.argv[1])
batch_size = 1000
monitor = False

if rank == 0:
    # Set to view from 25 seconds after start
    ts = int(time.time()) + 25 
    n_eb_nodes = int(os.environ.get('PS_N_EB_NODES', '1'))
    n_queries = 20
    print(f'To view performance, run:')
    print(f'./qm.sh {batch_size} {MPI.Get_processor_name()} {os.getpid()} {n_eb_nodes} {size} $(({ts})) {n_queries}', flush=True)


#import logging
#logging.basicConfig(filename='test_psana2_perf.log', filemode='w')
#logger = logging.getLogger('psana.psexp.node')
#logger.setLevel(logging.DEBUG)
#ch = logging.StreamHandler()
#ch.setLevel(logging.DEBUG)
#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#ch.setFormatter(formatter)
#logger.addHandler(ch)


def filter_fn(evt):
    return True


# Test dta
#xtc_dir = "/cds/data/drpsrcf/users/monarin/xtcdata/10M32n"  # test data
#ds = DataSource(exp='xpptut15', run=1, dir=xtc_dir, batch_size=batch_size, max_events=max_events, monitor=monitor)

# Test tmo-like data
#xtc_dir = '/cds/data/drpsrcf/users/monarin/tmolv9418/xtc8n'
#ds = DataSource(exp='xpptut15', run=175, dir=xtc_dir, batch_size=batch_size, max_events=max_events, monitor=monitor)

# SPI data (duplicate 120 events to 300k)
#xtc_dir = "/cds/data/drpsrcf/users/monarin/amo06516"        
#ds = DataSource(exp='amo06516', run=90, dir=xtc_dir, batch_size=batch_size, max_events=max_events, monitor=monitor)

# RIX data (duplicate 25k events to 20M)
xtc_dir = '/cds/data/drpsrcf/users/monarin/rixl1013320/small320x'
ds = DataSource(exp='rixl1013320', run=93, dir=xtc_dir, batch_size=batch_size, max_events=max_events, monitor=monitor)


sendbuf = np.zeros(1, dtype='i')
recvbuf = None
if rank == 0:
    recvbuf = np.empty([size, 1], dtype='i')

#import inspect
def bd_task(det, evt):
    hsd_num   = 10
    chan_num  = 0
    peaks     = det.raw.peaks(evt)
    #print(inspect.getfile(det.raw.__class__))
    #mypeak = peaks[hsd_num][chan_num][1][0] # randonly do someting
    #return np.sum(mypeak)

st_batch = time.time()
for run in ds.runs():
    #det = run.Detector('xpphsd')
    #det = run.Detector('hsd')
    
    #det = run.Detector("amopnccd")
    #pixel_position = run.beginruns[0].scan[0].raw.pixel_position
    #pixel_index_map = run.beginruns[0].scan[0].raw.pixel_index_map
    
    mysum = 0.0
    #for i_step, step in enumerate(run.steps()):
    for i_evt, evt in enumerate(run.events()):
        if sendbuf[0] == 0:
            print(f'RANK:{rank} GOT FIRST EVT AT {time.time()} ON HOST {MPI.Get_processor_name()} n_dgrams:{len(evt._dgrams)}', flush=True)
    
        #calib = det.raw.calib(evt)

        # Per run variables (amo)
        #photon_energy = det.raw.photon_energy(evt)
        #pixel_position = pp_det(evt)
        #pixel_index_map = pim_det(evt)
        
        # analysis code
        #mysum += bd_task(det, evt)
        #bd_task(det, evt)

        #peaks     = det.raw.peaks(evt)
        #print(i, len(peaks[0][0][0]), len(peaks[0][0][1]))
        
        sendbuf += 1
        if sendbuf[0] % batch_size == 0:
            en_batch = time.time()
            print(f'RANK:{rank} #events:{sendbuf[0]} rate:{(batch_size/(en_batch-st_batch))*1e-3:.2f}kHz', flush=True)
            #print((batch_size/(en_batch-st_batch))*1e-3, flush=True)
            st_batch = time.time()

comm.Gather(sendbuf, recvbuf, root=0)

en = MPI.Wtime()
if rank == 0:
    processed_events = np.sum(recvbuf)
    #processed_events = max_events # bypass run.events() loop 
    n_eb_nodes = int(os.environ.get('PS_EB_NODES', '1'))
    ps_smd_chunksize = int(os.environ.get('PS_SMD_CHUNKSIZE', '16777216'))
    ps_bd_chunksize = int(os.environ.get('PS_BD_CHUNKSIZE', '16777216'))
    print(f'#events={processed_events} #eb:{n_eb_nodes} PS_SMD_CHUNKSIZE={ps_smd_chunksize*1e-6:.2f}MB PS_BD_CHUNKSIZE:{ps_bd_chunksize*1e-6:.2f}MB time:{en-st:.2f}s rate: {processed_events/((en-st)*1e6):.5f}MHz')
