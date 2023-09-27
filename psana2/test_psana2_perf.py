# Running this script on psffb
# PS_EB_NODES=1 PS_SMD_N_EVENTS=10000 SLURM_HOSTFILE=slurm_hosts srun -o xx --partition=anaq --exclusive python test_psana2_perf.py
# or
# `which mpirun` -n 33 --hostfile openmpi_hosts --mca btl_openib_allow_ib 1 ./run_slac.sh

from psana import DataSource
import os, time, sys
import numpy as np
import logging
from datetime import datetime

from mpi4py import MPI
comm=MPI.COMM_WORLD
rank=comm.Get_rank()
size=comm.Get_size()

import cProfile


def smd_callback(run):
    for evt in run.events():
        yield evt


def run_main(max_events, 
            batch_size, 
            flag_monitor, 
            N_images_max,
            N_images_per_rank,
            ):

    # Print out command to use in psddmmon env to view stats
    if rank == 0 and flag_monitor:
        ts = int(time.time()) + 25 
        n_eb_nodes = int(os.environ.get('PS_N_EB_NODES', '1'))
        n_queries = 20
        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        print(f'[{date_time}] To view performance, run:')
        print(f'[{date_time}] ./qm.sh {batch_size} {MPI.Get_processor_name()} {os.getpid()} {n_eb_nodes} {size} $(({ts})) {n_queries}', flush=True)

    # Record start time
    comm.Barrier()
    st = MPI.Wtime()

    # Setup DataSource
    # Test dta
    #xtc_dir = "/cds/data/drpsrcf/users/monarin/xtcdata/10M32n"  # test data
    xtc_dir = "/cds/data/drpsrcf/users/monarin/xtcdata/10M60n/xtcdata/"
    ds = DataSource(exp='xpptut15', run=1, dir=xtc_dir, batch_size=batch_size, max_events=max_events, monitor=flag_monitor, 
            #smd_callback=smd_callback,
            )
    # Test tmo-like data
    #xtc_dir = '/cds/data/drpsrcf/users/monarin/tmolv9418/xtc8n'
    #ds = DataSource(exp='xpptut15', run=175, dir=xtc_dir, batch_size=batch_size, max_events=max_events, monitor=flag_monitor)
    # SPI data (duplicate 120 events to 300k)
    #xtc_dir = "/cds/data/drpsrcf/users/monarin/amo06516"        
    #ds = DataSource(exp='amo06516', run=90, dir=xtc_dir, batch_size=batch_size, max_events=max_events, monitor=flag_monitor)
    # RIX data (duplicate 25k events to 20M)
    #xtc_dir = '/cds/data/drpsrcf/users/monarin/rixl1013320/small320x'
    #ds = DataSource(exp='rixl1013320', run=93, dir=xtc_dir, batch_size=batch_size, max_events=max_events, monitor=flag_monitor)
    # Spinifel simulated data
    #xtc_dir = "/cds/data/drpsrcf/users/monarin/spinifel_3iyf"
    #ds = DataSource(exp='xpptut15', run=1, dir=xtc_dir, batch_size=batch_size, max_events=max_events, monitor=flag_monitor)
    
    # Setup run 
    run = next(ds.runs())
    sendbuf = np.zeros(1, dtype='i')
    recvbuf = None
    if rank == 0:
        recvbuf = np.empty([size, 1], dtype='i')
    det = run.Detector('xpphsd')
    #det = run.Detector('hsd')
    #det = run.Detector("amopnccd")
    #pixel_position = run.beginruns[0].scan[0].raw.pixel_position
    #pixel_index_map = run.beginruns[0].scan[0].raw.pixel_index_map

    # Record time per batch (N_images_per_rank)
    st_batch = time.time()
    for i_evt, evt in enumerate(run.events()):
        if sendbuf[0] == 0:
            print(f'RANK:{rank} GOT FIRST EVT AT {time.time()} ON HOST {MPI.Get_processor_name()} n_dgrams:{len(evt._dgrams)}', flush=True)
        sendbuf += 1
        if sendbuf[0] % N_images_per_rank == 0:
            en_batch = time.time()
            print(f'RANK:{rank} got {sendbuf[0]} events in {en_batch-st_batch:.3f}s. rate:{(batch_size/(en_batch-st_batch))*1e-3:.2f}kHz', flush=True)
            st_batch = time.time()
        if N_images_max > 0 and sendbuf[0] == N_images_max:
            ds.terminate()

    # Record no. of events and tototal time
    comm.Gather(sendbuf, recvbuf, root=0)
    en = MPI.Wtime()
    if rank == 0:
        if max_events > 0:
            processed_events = max_events 
        else:
            processed_events = np.sum(recvbuf)
        n_eb_nodes = int(os.environ.get('PS_EB_NODES', '1'))
        ps_smd_chunksize = int(os.environ.get('PS_SMD_CHUNKSIZE', '16777216'))
        ps_bd_chunksize = int(os.environ.get('PS_BD_CHUNKSIZE', '16777216'))
        print(f'#events={processed_events} #eb:{n_eb_nodes} PS_SMD_CHUNKSIZE={ps_smd_chunksize*1e-6:.2f}MB PS_BD_CHUNKSIZE:{ps_bd_chunksize*1e-6:.2f}MB time:{en-st:.2f}s rate: {processed_events/((en-st)*1e6):.5f}MHz')

if __name__ == "__main__":
    # Parameters for DataSource
    max_events = 100000
    if len(sys.argv) > 1:
        max_events = int(sys.argv[1])
    batch_size = 1000
    flag_monitor = True

    # If not 0, call ds.terminate() when this number is reached
    N_images_max = 0
    # Report rate at this number of images
    N_images_per_rank = 1000

    # Enable cProfile
    flag_prof = int(os.environ.get('PS_FLAG_PROF', '0'))
    if flag_prof:
        pr = cProfile.Profile()
        pr.enable()
    
    run_main(max_events, 
            batch_size, 
            flag_monitor, 
            N_images_max,
            N_images_per_rank,
            )
    
    if flag_prof:
        # Disable cProfile
        pr.disable()

        # Dump results
        # - for binary dump
        pr.dump_stats('cpu_%d.prof'%rank)
        # - for text dump
        with open('cpu_%d.txt' % rank, 'w') as output_file:
            sys.stdout = output_file
            pr.print_stats(sort='time')
            sys.stdout = sys.__stdout__

