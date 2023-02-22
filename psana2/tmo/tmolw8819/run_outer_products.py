import numpy as np
import psana as ps
import time
import matplotlib.pyplot as plt


########################################################
from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

########################################################
# Original script from Taran Driver
# Modified for timing and reducing the size of these ary
# vls  1000
# inner outer 10000
import sys
flag_torch = int(sys.argv[1])
if flag_torch:
    import torch
flag_reduce = int(sys.argv[2])
max_vls_len = 2048
max_wf_len = 59400
sigma_thres = 0 
if flag_reduce==1:
    max_vls_len = int(sys.argv[3])
    max_wf_len = int(sys.argv[4])
elif flag_reduce==2:
    sigma_thres = float(sys.argv[3])

t0 = time.monotonic()
########################################################
# this script fetches data and calculates the A^{T}A and A^{T}b
exp = 'tmolw8819' # specify experiment here
run = 300 # 10 fs, 523 eV
save_path = '/reg/d/psdm/tmo/tmolw8819/results/monarin/outer-prod-test-20221006' # '/reg/d/psdm/tmo/tmolw8819/results/taran/outer-prod-test-20221005'
max_events=100  # total no. of events = 42109
# parameters hard-coded in, including array sizes
chan_inner = 9
chan_outer = 11
ata = np.zeros((max_vls_len, max_vls_len)) # A^{T}A
atb_inner = np.zeros((max_vls_len, max_wf_len)) # A^{T}b for inner anode
atb_outer = np.zeros((max_vls_len, max_wf_len)) # A^{T}b for outer anode
a_sum = np.zeros(max_vls_len)
b_sum_inner = np.zeros(max_wf_len)
b_sum_outer = np.zeros(max_wf_len)
# these shift-and-scale parameters are also hard-coded in to stop the outer products blowing up
a_shift, a_scale = 300, 50
b_shift, b_scale = 2050, 13
########################################################
ds = ps.DataSource(exp=exp, run=run, max_events=max_events)
run = next(ds.runs())
# initialize detectors
timing = run.Detector('timing')
hsd = run.Detector('hsd')
andor = run.Detector('andor') # Piranha 4 camera is also going to read out at max_vls_len pix
# it's max_vls_lenx2 but to first order we can just sum down
########################################################
st = time.monotonic()
tt = 0
cn_events = 0
flag_plot = False
########################################################
for nevent, event in enumerate(run.events()): # loop over events
    
    evrs = timing.raw.eventcodes(event)
    if evrs is None:
        print("Bad EVRs: %d" % nevent)
        Nbad += 1
        continue
    evrs = np.array(evrs)
    if evrs[161]: pass # do nothing here 
    hsd_data = hsd.raw.waveforms(event)
    if hsd_data is None:
        print("Bad HSD: %d" % nevent)
        Nbad += 1
        continue
        
    vls = andor.raw.value(event)
    if vls is None:
        print("Bad VLS: %d" % nevent)
        Nbad += 1
        continue
    
    # x-ray spectrum is A
    vls=(vls[0].astype('float') - a_shift)/a_scale
    
    # get MBES waveforms (b)
    wf_MBES_inner = (hsd_data[chan_inner][0].astype('float') - b_shift) / b_scale
    wf_MBES_outer = (hsd_data[chan_outer][0].astype('float') - b_shift) / b_scale

    ########################################################
    if flag_plot:
        plt.subplot(2,1,1)
        plt.plot(wf_MBES_inner)
        plt.title(f'mean:{np.average(wf_MBES_inner)} std:{np.std(wf_MBES_inner)}')
        plt.subplot(2,1,2)
        plt.plot(wf_MBES_outer)
        plt.title(f'mean:{np.average(wf_MBES_outer)} std:{np.std(wf_MBES_outer)}')
        plt.show()
    
    t1 = time.monotonic()
    # now calculations
    ########################################################
    if flag_reduce==1:
        vls = vls[:max_vls_len]
        wf_MBES_inner = wf_MBES_inner[:max_wf_len]
        wf_MBES_outer = wf_MBES_outer[:max_wf_len]
    elif flag_reduce==2:
        vls = vls[:1000]
        wf_MBES_inner = wf_MBES_inner[wf_MBES_inner > np.average(wf_MBES_inner) + (np.std(wf_MBES_inner)*sigma_thres)]
        wf_MBES_outer = wf_MBES_outer[wf_MBES_outer > np.average(wf_MBES_outer) + (np.std(wf_MBES_outer)*sigma_thres)]
        
    if flag_torch:
        vls_t = torch.from_numpy(vls)
        wf_MBES_inner_t = torch.from_numpy(wf_MBES_inner)
        wf_MBES_outer_t = torch.from_numpy(wf_MBES_outer)
        ata += torch.outer(vls_t, vls_t).numpy()
        atb_inner += torch.outer(vls_t, wf_MBES_inner_t).numpy()
        atb_outer += torch.outer(vls_t, wf_MBES_outer_t).numpy()
    else:
        if flag_reduce == 2:
            # just calculating it because the reduced dimensions aren't the same for all events
            ata = np.outer(vls, vls)
            atb_inner = np.outer(vls, wf_MBES_inner)
            atb_outer = np.outer(vls, wf_MBES_outer)
        else:
            ata += np.outer(vls, vls)
            atb_inner += np.outer(vls, wf_MBES_inner)
            atb_outer += np.outer(vls, wf_MBES_outer)
    ########################################################
    if flag_reduce != 2:
        a_sum += vls
        b_sum_inner += wf_MBES_inner
        b_sum_outer += wf_MBES_outer
    
    ########################################################
    en = time.monotonic()
    tt += en - st
    print(f'nevent: {nevent+1} vls: {vls.shape} inner: {wf_MBES_inner.shape} outer: {wf_MBES_outer.shape} dt:{en-st:.3f}s. load:{t1-st:.3f}s./{((t1-st)/(en-st))*100:.2f}% calc:{en-t1:.3f}s./{((en-t1)/(en-st))*100:.2f}% tt:{tt:.3f}s. rate:{(nevent+1)/tt:.2f}Hz')
    st = time.monotonic()
    cn_events += 1
    ########################################################
    
#np.savez(save_path, {'ata': ata, 'atb_inner': atb_inner, 'atb_outer': atb_outer, 'a_sum': a_sum, 'b_sum_inner': b_sum_inner, 'b_sum_outer': b_sum_outer})

tn = time.monotonic()
if rank == 2:
    print(f'nevent: {cn_events} tt:{tn-t0:.5f}s. rate:{((tn-t0)/cn_events)*1e-3}kHz')
