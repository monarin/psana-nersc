import numpy as np
import time
import torch
#import matplotlib.pyplot as plt

ctor = np 
dtype = ctor.float32
dtype_i = ctor.int32


flag_plot = False
n_samples = 50
n_blobs = 20
n_fzp_samples = 200
if ctor == torch:
    ehsd = torch.from_numpy(np.random.rand(1000).reshape((n_blobs, n_samples)))
    ihsd = torch.from_numpy(np.random.rand(1000).reshape((n_blobs, n_samples)))
    fzp = torch.from_numpy(np.random.rand(n_fzp_samples))
else:
    ehsd = np.random.rand(1000).reshape((n_blobs, n_samples)).astype(dtype)
    ihsd = np.random.rand(1000).reshape((n_blobs, n_samples)).astype(dtype)
    fzp = np.random.rand(n_fzp_samples).astype(dtype)
n_events = 10
tt = ctor.zeros((n_events,3))


# The outer product matrices are in full form (8000, 2048)
n_hsd_full = 8000
n_fzp_full = 2048
# Assign random indices to the blobs
ehsd_st = ctor.zeros(n_blobs, dtype=dtype_i)
ihsd_st = ctor.zeros(n_blobs, dtype=dtype_i)
hsd_window_size = n_hsd_full / n_blobs
for i_blobs in range(n_blobs):
    # We create a window of size n_samples within a 
    # limiting range for each blob.
    lo_limit_hsd = i_blobs * hsd_window_size 
    hi_limit_hsd = lo_limit_hsd + hsd_window_size - n_samples
    window_start = np.random.randint(lo_limit_hsd, hi_limit_hsd)
    ehsd_st[i_blobs] = window_start 
    window_start = np.random.randint(lo_limit_hsd, hi_limit_hsd)
    ihsd_st[i_blobs] = window_start 
    if flag_plot:
        plt.subplot(2,1,1)
        plt.scatter(ehsd_st[i_blobs], 1)
        plt.subplot(2,1,2)
        plt.scatter(ihsd_st[i_blobs], 1)

if flag_plot: plt.show()

# Assign random indices to fzp window
fzp_st = 800


# Allocate full result matrices
#o_ehsd_ehsd = ctor.zeros((n_blobs, n_samples, n_samples), dtype=dtype)
o_ehsd_ehsd = ctor.zeros((n_hsd_full, n_hsd_full), dtype=dtype)
o_ihsd_ihsd = ctor.zeros((n_hsd_full, n_hsd_full), dtype=dtype)
o_ehsd_ihsd = ctor.zeros((n_hsd_full, n_hsd_full), dtype=dtype)
o_ehsd_fzp = ctor.zeros((n_hsd_full, n_fzp_full), dtype=dtype) 
o_ihsd_fzp = ctor.zeros((n_hsd_full, n_fzp_full), dtype=dtype) 
o_fzp_fzp = ctor.zeros((n_fzp_full, n_fzp_full), dtype=dtype) 


# Start outer products
t0 = time.monotonic()
for i in range(n_events):
    #t0 = time.monotonic()
    for i_blob, (_ehsd, _ihsd, _ehsd_st, _ihsd_st) in enumerate(zip(ehsd, ihsd, ehsd_st, ihsd_st)):
        #o_ehsd_ehsd[i_blob,:] = ctor.outer(_ehsd, _ehsd)
        o_ehsd_ehsd[_ehsd_st:_ehsd_st+n_samples, _ehsd_st:_ehsd_st+n_samples] += ctor.outer(_ehsd, _ehsd)
        o_ihsd_ihsd[_ihsd_st:_ihsd_st+n_samples, _ihsd_st:_ihsd_st+n_samples] += ctor.outer(_ihsd, _ihsd)
        o_ehsd_ihsd[_ehsd_st:_ehsd_st+n_samples, _ihsd_st:_ihsd_st+n_samples] += ctor.outer(_ehsd, _ihsd)
        o_ehsd_fzp[_ehsd_st:_ehsd_st+n_samples, fzp_st:fzp_st+n_fzp_samples] += ctor.outer(_ehsd, fzp)
        o_ihsd_fzp[_ehsd_st:_ehsd_st+n_samples, fzp_st:fzp_st+n_fzp_samples] += ctor.outer(_ihsd, fzp)
    #t1 = time.monotonic()
    o_fzp_fzp[fzp_st:fzp_st+n_fzp_samples,fzp_st:fzp_st+n_fzp_samples] = ctor.outer(fzp, fzp)
    #t2 = time.monotonic()
    #tt[i, 0] = t1-t0
    #tt[i, 1] = t2-t1
    #tt[i, 2] = t2-t0
t1 = time.monotonic()

#print(f'{ehsd.shape=},{fzp.shape=} {dtype=}')
#mean_tt = np.mean(tt, axis=0)
#print(f'Elapsed Time (s): {n_blobs} blobs {mean_tt[0]:.5f} fzp: {mean_tt[1]:.5f} total:{mean_tt[2]:.5f}')
#rate = (n_events/np.sum(tt, axis=0))*1e-3
#print(f'Rate (kHz)      : {n_blobs} blobs {rate[0]:.2f} fzp: {rate[1]:.2f} total:{rate[2]:.2f}')
print(f'Time: {t1-t0:.5f}s Rate: {(n_events/(t1-t0))*1e-3:.2f}kHz')
