import h5py, time        
import numpy as np

chunk = np.array([range(250000) for i in range(10)])
row_count = chunk.shape[0]

with h5py.File('test.h5', 'w') as f:
  maxshape = (None,) + chunk.shape[1:]
  dset = f.create_dataset('data', shape=chunk.shape, maxshape=maxshape,
    chunks=chunk.shape, dtype=chunk.dtype)
  dset[:] = chunk

  for i in range(2000):
    start = time.time()
    dset.resize(row_count + chunk.shape[0], axis=0)
    dset[row_count:] = chunk
    row_count += chunk.shape[0]
    print  i, time.time()-start

