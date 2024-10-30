import random
import time

import h5py
import numpy as np
from mpi4py import MPI

n_rows = 1000000
start_ts = 4413094745433570639


# Create a random no. identifier for each image in all datasets
t0 = time.monotonic()
print(f"Generating random indices", flush=True)
rand_ids = random.sample(range(start_ts, start_ts + n_rows), n_rows)
assert len(rand_ids) == np.unique(rand_ids).shape[0]
print(f"{rand_ids[:3]=}")
t1 = time.monotonic()
print(f"Create random indices for {n_rows} done in {t1-t0:.2f}s.", flush=True)


# Write data in parallel
t0 = time.monotonic()
rank = MPI.COMM_WORLD.rank
f = h5py.File(
    "/sdf/home/m/monarin/tmp/my1m.h5", "w", driver="mpio", comm=MPI.COMM_WORLD
)
f.create_dataset("timestamp", data=rand_ids)
calib_dset = f.create_dataset("calib", (n_rows, 10), dtype=np.int64)
calib_dset[:, rank] = rank
f.close()
t1 = time.monotonic()
print(f"Write to h5 file took {t1-t0:.2f}s.", flush=True)
