from psana import DataSource
import os
import numpy as np
from mpi4py import MPI
comm=MPI.COMM_WORLD
rank=comm.Get_rank()
size=comm.Get_size()

from psana.psexp.tools import show_log
show_log()

def filter_fn(evt):
    return True

def test_select_detectors():
    #xtc_dir = "/cds/data/psdm/prj/public01/xtc/"
    #ds = DataSource(exp='tmoc00118', run=222, dir=xtc_dir, as_smds=['hsd'], max_events=4)
    #xtc_dir = "./.tmp"
    xtc_dir = "/cds/data/drpsrcf/users/monarin/xtcdata/"
    batch_size = 100
    max_events = 0
    ds = DataSource(exp='xpptut15', run=1, dir=xtc_dir, batch_size=batch_size, max_events=max_events, monitor=True)
    sendbuf = np.zeros(1, dtype='i')
    recvbuf = None
    if rank == 0:
        recvbuf = np.empty([size, 1], dtype='i')

    for run in ds.runs():
        #det = run.Detector('hsd')
        for evt in run.events():
            sendbuf += 1
    comm.Gather(sendbuf, recvbuf, root=0)
    return recvbuf


st = MPI.Wtime()
recvbuf = test_select_detectors()
en = MPI.Wtime()
if rank == 0:
    processed_events = np.sum(recvbuf)
    print(f'#events={processed_events} time: {en-st}s rate: {processed_events/((en-st)*1e6)}MHz')
