from psana import dgram
from psana.psexp.smdreader_manager import SmdReaderManager
from psana.psexp.eventbuilder_manager import EventBuilderManager
from psana.psexp.packet_footer import PacketFooter
import os, time, glob, sys
import numpy as np
from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
assert size > 1

max_events = 1000

def filter(evt):
    return True

def destination(timestamp):
    n_destinations = 10
    return (timestamp % n_destinations) + 1

def smd_0(fds, n_smd_nodes):
    assert len(fds) > 0
    smdr_man = SmdReaderManager(fds, max_events)
    rankreq = np.empty(1, dtype='i')

    for chunk in smdr_man.chunks():
        comm.Recv(rankreq, source=MPI.ANY_SOURCE)
        comm.Send(chunk, dest=rankreq[0], tag=12)

    for i in range(n_smd_nodes):
        comm.Recv(rankreq, source=MPI.ANY_SOURCE)
        comm.Send(bytearray(), dest=rankreq[0], tag=12)    
    
def smd_node(configs, batch_size=1, filter=0, destination=0, sendbuf=None):
    eb_man = EventBuilderManager(configs, batch_size=batch_size, filter_fn=filter, destination=destination)
    rankreq = np.empty(1, dtype='i')
    
    while True:
        # handles requests from smd_0
        comm.Send(np.array([rank], dtype='i'), dest=0)
        info = MPI.Status()
        comm.Probe(source=0, tag=12, status=info)
        count = info.Get_elements(MPI.BYTE)
        view = bytearray(count)
        comm.Recv(view, source=0, tag=12)
        if count == 0:
            break
        
        # build batch of events
        for batch_dict in eb_man.batches(view):

            #for dest, (batch, evt_sizes) in batch_dict.items():
            #    d = dgram.Dgram(view=batch, config=configs[0], offset=0)
            #    pf = PacketFooter(view=batch)
            sendbuf += 1
    

if __name__ == "__main__":
    comm.Barrier()
    ts0 = MPI.Wtime()
    nfiles = 13
    if len(sys.argv) > 1:
        nfiles = int(sys.argv[1])
    batch_size = 1
    
    # broadcast smd files
    if rank == 0:
        #smd_files = np.asarray(glob.glob('/ffb01/monarin/hsd/smalldata/*.smd.xtc'))[:nfiles]
        #smd_files = np.asarray(glob.glob('/global/cscratch1/sd/monarin/testxtc2/hsd/smalldata/*.smd.xtc'))[:nfiles]
        #smd_files = np.asarray(glob.glob(os.path.join(os.environ['DW_PERSISTENT_STRIPED_psana2_hsd'],'hsd','smalldata','*.smd.xtc')))[:nfiles]
        #smd_files = np.asarray(glob.glob('/reg/d/psdm/xpp/xpptut15/scratch/mona/xtc2/smalldata/*.smd.xtc2'))[:nfiles]
        smd_files = np.asarray(glob.glob('/ffb01/mona/xtc2/smalldata/*.smd.xtc2'))[:nfiles]
    else:
        smd_files = None
    smd_files = comm.bcast(smd_files, root=0)

    # broadcast config size (mpich needs this for Bcast)
    if rank == 0:
        fds = [os.open(smd_file, os.O_RDONLY) for smd_file in smd_files]
        configs = [dgram.Dgram(file_descriptor=fd) for fd in fds]
        nbytes = np.array([memoryview(config).shape[0] for config in configs], dtype='i')
    else:
        nbytes = np.empty(nfiles, dtype='i')
    comm.Bcast(nbytes, root=0) 

    # broadcast configs
    if rank > 0:
        configs = [np.empty(nbyte, dtype='b') for nbyte in nbytes] 

    for i in range(nfiles):
        comm.Bcast([configs[i], nbytes[i], MPI.BYTE], root=0)

    configs = [dgram.Dgram(view=config, offset=0) for config in configs]
    
    comm.Barrier()
    ts1 = MPI.Wtime()
    
    # start smd-bd nodes
    sendbuf = np.zeros(1, dtype='i')
    recvbuf = None
    n_smd_nodes = size - 1
    if rank == 0:
        recvbuf = np.empty([size, 1], dtype='i')
        smd_0(fds, n_smd_nodes)
    else:
        smd_node(configs, batch_size=batch_size, filter=filter, destination=destination, sendbuf=sendbuf)
    comm.Gather(sendbuf, recvbuf, root=0)
    
    comm.Barrier()
    ts2 = MPI.Wtime()
    if rank == 0:
        print("#Files: %d #Evts: %d Total: %6.2f s Bcast: %6.2f s Rate: %6.2f MHz"%(nfiles, np.sum(recvbuf), ts2-ts0, ts1-ts0, np.sum(recvbuf)/((ts2-ts0)*1e6)))
        print(recvbuf)
