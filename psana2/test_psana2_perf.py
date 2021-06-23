from psana import DataSource
import os, time
import numpy as np
from mpi4py import MPI
comm=MPI.COMM_WORLD
rank=comm.Get_rank()
size=comm.Get_size()

comm.Barrier()
if rank == 0:
    print(f'DONE IMPORT AT: {time.time()} RANK 0 PID={os.getpid()} on HOST  {MPI.Get_processor_name()}')


import logging
logger = logging.getLogger('psana.psexp.node')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
max_events = 0

def filter_fn(evt):
    return True

def test_select_detectors():
    #xtc_dir = "/cds/data/psdm/prj/public01/xtc/"
    #ds = DataSource(exp='tmoc00118', run=222, dir=xtc_dir, as_smds=['hsd'], max_events=4)
    #xtc_dir = '/cds/home/m/monarin/lcls2/psana/psana/tests/.tmp'
    #xtc_dir = '/cds/home/m/monarin/lcls2/psana/psana/tests/test_data/mixed_rate'
    #xtc_dir = "/cds/data/drpsrcf/users/monarin/xtcdata/10M32n/"
    xtc_dir = "/cds/data/drpsrcf/users/monarin/xtcdata/10M60n/xtcdata/"
    batch_size = 1000
    ds = DataSource(exp='xpptut15', run=1, dir=xtc_dir, batch_size=batch_size, max_events=max_events, monitor=False)
    sendbuf = np.zeros(1, dtype='i')
    recvbuf = None
    if rank == 0:
        recvbuf = np.empty([size, 1], dtype='i')

    st = 0
    for run in ds.runs():
        #det = run.Detector('hsd')
        for i, evt in enumerate(run.events()):
            if i == 0:
                print(f'RANK:{rank} GOT FIRST EVT AT {time.time()} ON HOST {MPI.Get_processor_name()}')
            sendbuf += 1
            #if i % batch_size == 0:
            #    en = time.time()
            #    if st:
            #        # skip the first batch 
            #        print(f'RANK:{rank} GOT {batch_size} IN {en-st:.2f}s RATE: {batch_size/(en-st):.2f}Hz')
            #    st = time.time()
    comm.Gather(sendbuf, recvbuf, root=0)
    return recvbuf


st = MPI.Wtime()
recvbuf = test_select_detectors()
en = MPI.Wtime()
if rank == 0:
    #processed_events = np.sum(recvbuf)
    processed_events = max_events
    print(f'#events={processed_events} time: {en-st}s rate: {processed_events/((en-st)*1e6)}MHz')
