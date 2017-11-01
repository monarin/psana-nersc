from psana import *
import pickle

from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
assert size>1, 'Dealer mode requires at least 2 ranks.'

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("exprun", help="psana experiment/run string (e.g. exp=xppd7114:run=43)")
parser.add_argument("-n","--noe",help="number of events, all events=1e10",default=-1, type=int)
args = parser.parse_args()

class ConvertToPyObj():
    def __init__(self,psanaOffset):
        self.filenames = psanaOffset.filenames()
        self.offsets = psanaOffset.offsets()
        self.lastBeginCalibCycleDgram = psanaOffset.lastBeginCalibCycleDgram()

def master():
    setOption('PSXtcInput.XtcInputModule.liveDbConn', 'Server=scidb1.nersc.gov;Database=lclsdb;Uid=lclsdb_user')
    start_ds = MPI.Wtime()
    ds = DataSource(args.exprun+':smd:live:dir=/global/cscratch1/sd/monarin/d/psdm/cxi/cxid9114/xtc')
    end_ds = MPI.Wtime()
    print "PROFILEDS", rank, start_ds, end_ds, end_ds - start_ds
    for nevt, evt in enumerate(ds.events()):
        if nevt==args.noe: break
        offset = evt.get(EventOffset)
        rankreq = comm.recv(source=MPI.ANY_SOURCE)
        comm.send(ConvertToPyObj(offset),dest=rankreq)
    end_master = MPI.Wtime()
    print "PROFILEMASTER", end_ds, end_master, end_master - end_ds
    for rankreq in range(size-1):
        rankreq = comm.recv(source=MPI.ANY_SOURCE)
        comm.send('endrun',dest=rankreq)

def client():
    start_ds = MPI.Wtime()
    ds = DataSource(args.exprun+':rax')
    end_ds = MPI.Wtime()
    print "PROFILEDS", rank, start_ds, end_ds, end_ds - start_ds
    det = Detector('CxiDs2.0:Cspad.0')
    while True:
        comm.send(rank,dest=0)
        offset = comm.recv(source=0)
        if offset == 'endrun': break
        start_jump = MPI.Wtime()
        evt = ds.jump(offset.filenames, offset.offsets, offset.lastBeginCalibCycleDgram)
        end_jump = MPI.Wtime()
        print "PROFILEJUMP", rank, start_jump, end_jump, end_jump-start_jump
        img = det.raw(evt)

comm.Barrier()
start = MPI.Wtime()
if rank==0:
    master()
else:
    client()
comm.Barrier()
end = MPI.Wtime()
if rank == 0: print "PROFILEPROC", start, end, end-start

print '*** Rank',rank,'completed ***'

