import os, time                                                                       
from psana import DataSource                                                          
import numpy as np                                                                    
import vals
from mpi4py import MPI                                                                
comm = MPI.COMM_WORLD                                                                 
size = comm.Get_size()                                                                
rank = comm.Get_rank()                                                                

def filter_fn(evt):
    return True    

comm.Barrier()
st = MPI.Wtime()
max_events = 10000
batch_size = 1000
os.environ['PS_SMD_N_EVENTS'] = str(batch_size)
#xtc_dir = "/ffb01/mona/xtc2"
xtc_dir = "/reg/d/psdm/xpp/xpptut15/scratch/mona/xtc2"
#xtc_dir = os.path.join(os.environ['DW_PERSISTENT_STRIPED_psana2_hsd'],'hsd')
ds = DataSource('exp=xpptut13:run=1:dir=%s'%(xtc_dir), filter=0, max_events=max_events, batch_size=batch_size)

sendbuf = np.zeros(1, dtype='i')
recvbuf = None
if rank == 0:
    recvbuf = np.empty([size, 1], dtype='i')

for run in ds.runs():
    det = run.Detector('xppcspad')
    edet = run.Detector('XPP:VARS:FLOAT:02')
    for evt in run.events():
        padarray = vals.padarray
        assert(np.array_equal(det.raw.calib(evt),np.stack((padarray,padarray))))
        assert edet(evt) == 41.0
        sendbuf += 1

comm.Gather(sendbuf, recvbuf, root=0)

comm.Barrier()
en = MPI.Wtime()
if rank == 0:
    n_events = np.sum(recvbuf)
    smd0 = 1
    evtbuilder = int(os.environ.get('PS_SMD_NODES', 1))
    print('#smd0threads: %d #evtbuilder: %d #events: %d total elapsed (s): %6.2f rate (kHz): %6.2f'%(smd0, evtbuilder, n_events, en-st, n_events/((en-st)*1000)))
    #print('#evts per bd mean: %6.1f min:%6.1f max: %6.1f std: %6.1f'%(np.mean(recvbuf[smd0+evtbuilder:]), np.min(recvbuf[smd0+evtbuilder:]), np.max(recvbuf[smd0+evtbuilder:]), np.std(recvbuf[smd0+evtbuilder:])))
