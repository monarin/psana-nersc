#!/usr/bin/env python
""" For testing live mode and other PSANA2 performance measurement

on drp-srcf, generate slurm_hosts then run
SLURM_HOSTFILE=slurm_hosts srun -o log.log --partition=anaq --exclusive python -u test_live.py

"""
import os
import sys
import time

import numpy as np
from mpi4py import MPI
from psana import DataSource

import vals

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
myhost = MPI.Get_processor_name()
print(f"RANK:{rank} HOSTNAME:{myhost}")


def test_standard():
    batch_size = 1000
    max_events = 0

    exp = "tmoc00221"
    runno = 20
    root_dir = "/sdf/data/lcls/drpsrcf/ffb"
    # root_dir = '/cds/data/drpsrcf'

    if len(sys.argv) > 3:
        exp = sys.argv[1]
        runno = int(sys.argv[2])
        max_events = int(sys.argv[3])
        root_dir = sys.argv[4]

    if rank == 0:
        print(f"{exp=} {runno=} {batch_size=} {max_events=}")

    hutch = exp[:3]
    xtc_dir = f"{root_dir}/{hutch}/{exp}/xtc/"

    ds = DataSource(
        exp=exp,
        run=runno,
        batch_size=batch_size,
        max_events=max_events,
        dir=xtc_dir,
        live=False,
        monitor=True,
        # detectors=detectors
    )

    sendbuf = np.zeros(1, dtype="i")
    recvbuf = None
    if rank == 0:
        recvbuf = np.empty([size, 1], dtype="i")

    st = time.time()
    for run in ds.runs():
        for nevt, evt in enumerate(run.events()):
            if nevt % 1000 == 0 and nevt > 0:
                en = time.time()
                print(
                    f"RANK: {rank:4d} EVENTS: {nevt:10d} RATE: {(1000/(en-st))*1e-3:.2f}kHz",
                    flush=True,
                )
                st = time.time()
            sendbuf += 1

    # Count total no. of events
    comm.Gather(sendbuf, recvbuf, root=0)
    if rank == 0:
        n_events = np.sum(recvbuf)
    else:
        n_events = None
    n_events = comm.bcast(n_events, root=0)
    return n_events


if __name__ == "__main__":
    comm.Barrier()
    t0 = MPI.Wtime()
    if rank == 0:
        print(f"PROMETHEUS JOBID: {os.getpid()}", flush=True)

    n_events = test_standard()

    comm.Barrier()
    t1 = MPI.Wtime()
    if rank == 0:
        n_eb_nodes = int(os.environ.get("PS_EB_NODES", "1"))
        print(
            f"TOTAL TIME:{t1-t0:.2f}s #EB: {n_eb_nodes:3d} EVENTS:{n_events:10d} RATE:{(n_events/(t1-t0))*1e-6:.2f}MHz",
            flush=True,
        )
