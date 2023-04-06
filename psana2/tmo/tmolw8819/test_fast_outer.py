import numpy as np
import time
#import torch

dtype = np.float32

ctor = np

n_samples = 50
n_blobs = 20
n_fzp_samples = 200
ehsd = ctor.random.rand(1000).reshape((n_blobs, n_samples)).astype(dtype)
ihsd = ctor.random.rand(1000).reshape((n_blobs, n_samples)).astype(dtype)
fzp = ctor.random.rand(n_fzp_samples).astype(dtype)

n_events = 10
tt = ctor.zeros((n_events,3))
o_ehsd_ehsd = ctor.zeros((n_blobs, n_samples, n_samples), dtype=dtype)
o_ihsd_ihsd = ctor.zeros((n_blobs, n_samples, n_samples), dtype=dtype)
o_ehsd_ihsd = ctor.zeros((n_blobs, n_samples, n_samples), dtype=dtype)
o_ehsd_fzp = ctor.zeros((n_blobs, n_samples, n_fzp_samples), dtype=dtype) 
o_ihsd_fzp = ctor.zeros((n_blobs, n_samples, n_fzp_samples), dtype=dtype) 
o_fzp_fzp = ctor.zeros((n_fzp_samples, n_fzp_samples), dtype=dtype) 
for i in range(n_events):
    t0 = time.monotonic()
    for i_blob, (_ehsd, _ihsd) in enumerate(zip(ehsd, ihsd)):
        o_ehsd_ehsd[i_blob,:] = ctor.outer(_ehsd, _ehsd)
        o_ihsd_ihsd[i_blob,:] = ctor.outer(_ihsd, _ihsd)
        o_ehsd_ihsd[i_blob,:] = ctor.outer(_ehsd, _ihsd)
        o_ehsd_fzp[i_blob,:] = ctor.outer(_ehsd, fzp)
        o_ihsd_fzp[i_blob,:] = ctor.outer(_ihsd, fzp)
    t1 = time.monotonic()
    o_fzp_fzp[:] = ctor.outer(fzp, fzp)
    t2 = time.monotonic()
    tt[i, :] = [t1-t0, t2-t1, t2-t0]
    

print(f'{ehsd.shape=},{fzp.shape=} {dtype=}')
mean_tt = np.mean(tt, axis=0)
print(f'Elapsed Time (s): {n_blobs} blobs {mean_tt[0]:.5f} fzp: {mean_tt[1]:.5f} total:{mean_tt[2]:.5f}')
rate = (n_events/np.sum(tt, axis=0))*1e-3
print(f'Rate (kHz)      : {n_blobs} blobs {rate[0]:.2f} fzp: {rate[1]:.2f} total:{rate[2]:.2f}')

