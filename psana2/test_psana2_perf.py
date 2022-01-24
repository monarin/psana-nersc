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
print(f'DONE IMPORT AT: {time.time()} RANK {rank} PID={os.getpid()} on HOST  {MPI.Get_processor_name()}', flush=True)


#import logging
#logging.basicConfig(filename='test_psana2_perf.log', filemode='w')
#logger = logging.getLogger('psana.psexp.event_manager')
#logger.setLevel(logging.DEBUG)
#ch = logging.StreamHandler()
#ch.setLevel(logging.DEBUG)
#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#ch.setFormatter(formatter)
#logger.addHandler(ch)

max_events = 0

def filter_fn(evt):
    return True

st = MPI.Wtime()

#xtc_dir = "/cds/data/drpsrcf/users/monarin/xtcdata/10M4n"
xtc_dir = '/cds/data/drpsrcf/users/monarin/tmolv9418/xtc32n'
batch_size = 1000
monitor = False
#ds = DataSource(exp='xpptut15', run=1, dir=xtc_dir, batch_size=batch_size, max_events=max_events, monitor=False)
ds = DataSource(exp='tmolv9418', run=175, dir=xtc_dir, batch_size=batch_size, max_events=max_events, monitor=False)
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
    #det = run.Detector('hsd')
    mysum = 0.0
    for i, evt in enumerate(run.events()):
        if i == 0:
            print(f'RANK:{rank} GOT FIRST EVT AT {time.time()} ON HOST {MPI.Get_processor_name()} n_dgrams:{len(evt._dgrams)}', flush=True)
        
        # analysis code
        #mysum += bd_task(det, evt)
        #bd_task(det, evt)

        #peaks     = det.raw.peaks(evt)
        #print(i, len(peaks[0][0][0]), len(peaks[0][0][1]))
        
        sendbuf += 1
        if i % batch_size == 0:
            en_batch = time.time()
            #print(f'RANK:{rank} processed {i} events rate:{(batch_size/(en_batch-st_batch))*1e-3:.2f}kHz mysum={mysum:.2f}', flush=True)
            print((batch_size/(en_batch-st_batch))*1e-3, flush=True)
            st_batch = time.time()


comm.Gather(sendbuf, recvbuf, root=0)

en = MPI.Wtime()
if rank == 0:
    processed_events = np.sum(recvbuf)
    #processed_events = max_events # bypass run.events() loop 
    n_eb_nodes = int(os.environ.get('PS_EB_NODES', '1'))
    print(f'#events={processed_events} #eb:{n_eb_nodes} time: {en-st}s rate: {processed_events/((en-st)*1e6):.5f}MHz')
