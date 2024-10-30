""" Test pushing data to Prometheus server.

"""

import os
import threading
import time

from mpi4py import MPI
from psana.psexp import PrometheusManager

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if __name__ == "__main__":
    # Use rank 0 processid and jobid - we'll need to broadcast this.
    if rank == 0:
        jobid = os.getpid()
    else:
        jobid = None

    jobid = comm.bcast(jobid, root=0)

    if rank == 0:
        print(f"jobid={jobid}", flush=True)

    # Setup Prometheus client thread for pushing data every 15 s.
    prom_man = PrometheusManager(jobid)
    e = threading.Event()
    t = threading.Thread(
        name="PrometheusThread%s" % (rank),
        target=prom_man.push_metrics,
        args=(e, rank),
        daemon=True,
    )
    t.start()

    # Setup a random metric
    bd_wait_eb = PrometheusManager.get_metric("psana_bd_wait_eb")
    n_loops = 30
    st_req = time.monotonic()
    for i in range(n_loops):
        time.sleep(1)
        en_req = time.monotonic()
        bd_wait_eb.labels("seconds", rank).inc(en_req - st_req)
        print(f"rank: {rank:4d} push {en_req - st_req:.2f} s", flush=True)
        st_req = time.monotonic()
