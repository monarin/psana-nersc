# Running this script on psffb
# PS_EB_NODES=1 PS_SMD_N_EVENTS=10000 SLURM_HOSTFILE=slurm_hosts srun -o xx --partition=anaq --exclusive python test_psana2_perf.py
# or
# `which mpirun` -n 33 --hostfile openmpi_hosts --mca btl_openib_allow_ib 1 ./run_slac.sh
#
# Test read while write:
# 1. From a drp node, go to /sdf/data/lcls/drpsrcf/ffb/users/monarin/tmolv9418/inprogress
# 2. Remove the data file then run:
#    > dd if=/sdf/data/lcls/drpsrcf/ffb/users/monarin/tmolv9418/xtc/tmolv9418-r0175-s000-c000.xtc2 of=xpptut15-r0001-s000-c000.xtc2 oflag=nocache bs=1MB status=progress
# 3. Use ctrl-z to suspend the process (pause writing) and fg when start seeing bd cores are waiting for the data
# 4. From s3df, allocate three nodes (use xpptut15 run 1), run
#    > PS_VERBOSITY=1 PS_EB_NODES=8 mpirun -n 137 --hostfile slurm_host_test python -u test_psana2_perf.py
#    In slurm_host_test,
#    sdfmilan220 slots=1
#    sdfmilan221 slots=68
#    sdfmilan223 slots=68

import logging
import os
import sys
import time
from datetime import datetime

import numpy as np
from mpi4py import MPI
from psana import DataSource

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

import cProfile


def smd_callback(run):
    for evt in run.events():
        yield evt


def run_main(
    max_events,
    batch_size,
    flag_monitor,
    N_images_max,
    N_images_per_rank,
):

    # Print out command to use in psddmmon env to view stats
    if rank == 0 and flag_monitor:
        ts = int(time.time()) + 25
        n_eb_nodes = int(os.environ.get("PS_N_EB_NODES", "1"))
        n_queries = 20
        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        print(f"[{date_time}] To view performance, run:")
        print(
            f"[{date_time}] ./qm.sh {batch_size} {MPI.Get_processor_name()} {os.getpid()} {n_eb_nodes} {size} $(({ts})) {n_queries}",
            flush=True,
        )

    # Record start time
    comm.Barrier()
    st = MPI.Wtime()

    # Setup DataSource
    # Test dta
    # xtc_dir = "/cds/data/drpsrcf/users/monarin/xtcdata/10M32n"  # test data
    # xtc_dir = "/cds/data/drpsrcf/users/monarin/xtcdata/10M60n/xtcdata/"
    # xtc_dir = "/sdf/data/lcls/drpsrcf/ffb/users/monarin/xtcdata/10M16n"
    # xtc_dir = "/sdf/data/lcls/drpsrcf/ffb/users/monarin/tmoc00118/xtc"
    # ds = DataSource(exp='tmoc00118', run=463, batch_size=batch_size, dir=xtc_dir, max_events=max_events, monitor=flag_monitor, )
    # ds = DataSource(exp='xpptut15', run=1, dir=xtc_dir, batch_size=batch_size, max_events=max_events, monitor=flag_monitor,
    # smd_callback=smd_callback,
    #        )

    # Test tmo-like data
    xtc_dir = '/sdf/data/lcls/drpsrcf/ffb/users/monarin/tmolv9418/inprogress'
    ds = DataSource(exp='xpptut15', run=1, dir=xtc_dir, live=True)
    # ds = DataSource(exp='rixc00122', run=211, batch_size=batch_size, max_events=max_events, monitor=flag_monitor)
    # ds = DataSource(exp='tmoc00122', run=569, batch_size=batch_size, max_events=max_events, monitor=flag_monitor, )
    #ds = DataSource(
    #    exp="tmox1009422",
    #    run=26,
    #    batch_size=batch_size,
    #    max_events=max_events,
    #    monitor=flag_monitor,
    #)
    # ds = DataSource(exp='tmox1009422', run=61, batch_size=batch_size, max_events=max_events, monitor=flag_monitor, )
    # SPI data (duplicate 120 events to 300k)
    # xtc_dir = "/cds/data/drpsrcf/users/monarin/amo06516"
    # ds = DataSource(exp='amo06516', run=90, dir=xtc_dir, batch_size=batch_size, max_events=max_events, monitor=flag_monitor)
    # RIX data (duplicate 25k events to 20M)
    # xtc_dir = '/cds/data/drpsrcf/users/monarin/rixl1013320/small320x'
    # ds = DataSource(exp='rixl1013320', run=93, dir=xtc_dir, batch_size=batch_size, max_events=max_events, monitor=flag_monitor)
    # Spinifel simulated data
    # xtc_dir = "/cds/data/drpsrcf/users/monarin/spinifel_3iyf"
    # ds = DataSource(exp='xpptut15', run=1, dir=xtc_dir, batch_size=batch_size, max_events=max_events, monitor=flag_monitor)
    # rixc00122 r0211
    # ds = DataSource(exp='rixc00122', run=211, batch_size=batch_size, max_events=max_events, monitor=flag_monitor)

    # Setup smalldata server (if needed)
    smd = None
    # smd = ds.smalldata(filename='/sdf/data/lcls/drpsrcf/ffb/users/monarin/h5/mysmallh5.h5', batch_size=5)
    # Setup run
    run = next(ds.runs())
    sendbuf = np.zeros(1, dtype="i")
    recvbuf = None
    if rank == 0:
        recvbuf = np.empty([size, 1], dtype="i")
    det1 = run.Detector('hsd')
    #det1 = run.Detector("tmo_atmopal")
    #det2 = run.Detector("tmo_fzppiranha")
    #det3 = run.Detector("mbes_hsd")

    # Record time per batch (N_images_per_rank)
    st_batch = time.time()
    for i_evt, evt in enumerate(run.events()):
        data1 = det1.raw.waveforms(evt)
        #data1 = det1.raw.calib(evt)
        #data2 = det1.raw.raw(evt)
        #data3 = det3.raw.waveforms(evt)

        if sendbuf[0] == 0:
            print(
                f"RANK:{rank} GOT FIRST EVT AT {time.time()} ON HOST {MPI.Get_processor_name()} n_dgrams:{len(evt._dgrams)}",
                flush=True,
            )
        sendbuf += 1

        if sendbuf[0] % N_images_per_rank == 0:
            en_batch = time.time()
            print(
                f"RANK:{rank} got {sendbuf[0]} events in {en_batch-st_batch:.3f}s. rate:{(batch_size/(en_batch-st_batch))*1e-3:.2f}kHz",
                flush=True,
            )
            st_batch = time.time()

        if data1 is not None and smd is not None:
            smd.event(evt, calib=data1)
        if N_images_max > 0 and sendbuf[0] == N_images_max:
            ds.terminate()

    if smd is not None:
        smd.done()

    # Record no. of events and tototal time
    comm.Gather(sendbuf, recvbuf, root=0)
    en = MPI.Wtime()
    if rank == 0:
        if max_events > 0:
            processed_events = max_events
        else:
            processed_events = np.sum(recvbuf)
        n_eb_nodes = int(os.environ.get("PS_EB_NODES", "1"))
        n_bd_nodes = comm.Get_size() - n_eb_nodes - 1
        ps_smd_chunksize = int(os.environ.get("PS_SMD_CHUNKSIZE", "16777216"))
        ps_bd_chunksize = int(os.environ.get("PS_BD_CHUNKSIZE", "16777216"))
        print(
            f"#events={processed_events} #eb:{n_eb_nodes} #bd:{n_bd_nodes} PS_SMD_CHUNKSIZE={ps_smd_chunksize*1e-6:.2f}MB PS_BD_CHUNKSIZE:{ps_bd_chunksize*1e-6:.2f}MB time:{en-st:.2f}s rate: {processed_events/((en-st)*1e6):.5f}MHz"
        )


if __name__ == "__main__":
    # Parameters for DataSource
    max_events = 0

    if len(sys.argv) > 1:
        max_events = int(sys.argv[1])
    batch_size = 1000
    flag_monitor = True

    # If not 0, call ds.terminate() when this number is reached
    N_images_max = 0
    # Report rate at this number of images
    N_images_per_rank = 1000

    # Enable cProfile
    flag_prof = int(os.environ.get("PS_FLAG_PROF", "0"))
    if flag_prof:
        pr = cProfile.Profile()
        pr.enable()

    run_main(
        max_events,
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
        pr.dump_stats("cpu_%d.prof" % rank)
        # - for text dump
        with open("cpu_%d.txt" % rank, "w") as output_file:
            sys.stdout = output_file
            pr.print_stats(sort="time")
            sys.stdout = sys.__stdout__
