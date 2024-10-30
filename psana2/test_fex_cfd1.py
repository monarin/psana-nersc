import os

import matplotlib.pyplot as plt
import numpy as np
from mpi4py import MPI
from psana import *
from psana.hexanode.PyCFD import PyCFD

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

txt_ana = ""
txt_det = ""
txt_tot = ""
txt_pks = ""
cn_with_peaks = 0
cn_evts = 0

comm.Barrier()
t0 = MPI.Wtime()

max_events = 25600000
batch_size = 1000
xtc_dir = "/cds/data/drpsrcf/users/monarin/tmolv9418/xtc4n"
ds = DataSource(
    exp="tmolv9418", run=175, dir=xtc_dir, batch_size=batch_size, max_events=max_events
)
# ds = DataSource(exp='tmolv9418', run=175, batch_size=batch_size, max_events=max_events)

# Create Srv nodes for data writing
smd_batch_size = 1000
# smd = ds.smalldata(filename='/cds/data/drpsrcf/users/monarin/tmolv9418/out/mysmallh5.h5', batch_size=smd_batch_size, )
# max_peaks = 100 # maximum no. of peaks saved per event

myrun = next(ds.runs())
sample_period = 1000e-9 / 6400 * 14.0 / 13.0
showFex = True

det = myrun.Detector("hsd")

if det:
    hsd = det.raw  # This causes problem w/o an event loop (non bd node see None)

    seg_chans = hsd._seg_chans()
    print("seg_chans {:}".format(seg_chans))

    # dump_det_config(det, args.detname)

    # lookup constants by segment number
    lookup = False
    if lookup:
        raw_sz = 0
        fex_sz = 0
        for config in det._configs:
            if not "hsd" in config.__dict__:
                print("Skipping config {:}".format(config.__dict__))
                continue
            scfg = getattr(config, "hsd")
            for seg, segcfg in scfg.items():
                if segcfg.config.user.raw.prescale > 0:
                    _raw_sz = segcfg.config.user.raw.gate_ns * 6.4 * 13 / 14
                    if _raw_sz > raw_sz:
                        raw_sz = _raw_sz
                if segcfg.config.user.fex.prescale > 0:
                    _fex_sz = segcfg.config.user.fex.gate_ns * 6.4 * 13 / 14
                    if _fex_sz > fex_sz:
                        fex_sz = _fex_sz
                    print(f"ymin[{seg}] = {segcfg.config.user.fex.ymin}")
                    print(f"ymax[{seg}] = {segcfg.config.user.fex.ymax}")

        # Get this from the configuration
        # max_size = int((raw_sz + fex_sz)*40*1.05)  # 20 rows * 40 samples/row * raw,sparse
        max_size = int(
            (raw_sz + fex_sz) * 1.05
        )  # 20 rows * 40 samples/row * raw,sparse
        print(
            "raw_sz {:}R  fex_sz {:}R  max_size {:}S".format(raw_sz, fex_sz, max_size)
        )

# end if det

CFD_params = {
    "sample_interval": 1.68269e-10,
    "fraction": 0.35,
    "delay": 0.35e-09,
    "polarity": "Negative",
    "threshold": 5,
    "walk": 0,
    "timerange_low": 0,
    "timerange_high": 100e-05,
    "offset": 2049,
}

CFD = PyCFD(CFD_params)

plot = False
if plot:
    plt.figure(figsize=(10, 10))

ii = 1

st_batch = time.time()
for nevt, evt in enumerate(myrun.events()):

    #     if nevt<19:
    #         continue
    t_st = time.monotonic()

    # wfs   = hsd.waveforms(evt)
    fex = hsd.peaks(evt)

    continue

    t_det = time.monotonic()
    ts = evt.timestamp
    seg = 0

    smd_peaks = np.zeros(max_peaks, dtype=float)
    cn_smd_peaks = 0

    # Sparsified waveform plot
    if fex and seg in fex and showFex:
        # Looping access
        for ndigi, (digitizer, fexdata) in enumerate(fex.items()):
            for nfex, (channel, fexchan) in enumerate(fexdata.items()):
                startpos, peaks = fexchan
                # print(f'nevt={nevt} ndigi={ndigi} nfex={nfex} npeaks={len(startpos)}')

                if not startpos:
                    continue

                # Concats waveform and timestamps from all channel into 1D array
                peaks_sizes = [peak.shape[0] for peak in peaks]
                arr_size = np.sum(peaks_sizes)
                stimes = np.zeros(arr_size)
                swf = np.zeros(arr_size, dtype=peaks[0].dtype)
                for ipeak, peak in enumerate(peaks):
                    if ipeak == 0:
                        st = 0
                    else:
                        st = np.sum(peaks_sizes[:ipeak])
                    en = st + peaks_sizes[ipeak]
                    stimes[st:en] = (
                        np.arange(startpos[ipeak], startpos[ipeak] + peaks_sizes[ipeak])
                        * sample_period
                    )
                    swf[st:en] = peak - 1  # Follow the old code

                ts = stimes
                vs = swf
                try:
                    ## pk is the identified arrival time
                    pks = CFD.CFD(vs, ts)

                    # print(nevt, ndigi, nfex, pks)
                    # Copy pks to smd_peaks array
                    pks_size = len(pks)
                    if cn_smd_peaks + pks_size <= max_peaks:
                        smd_peaks[cn_smd_peaks : cn_smd_peaks + pks_size] = pks
                        cn_smd_peaks += pks_size

                    if len(pks) > 0:
                        if plot:
                            plt.subplot(3, 3, ii)
                            plt.plot(
                                ts,
                                vs,
                                marker="o",
                                linestyle="None",
                                markerfacecolor="None",
                                label="isolated peak",
                            )
                            for pk in pks:
                                plt.plot(
                                    [pk, pk],
                                    [plt.ylim()[0], plt.ylim()[1]],
                                    "-.",
                                    label="identified arrival time",
                                )
                            plt.title("Event " + str(nevt))
                            plt.xlabel("Time (ns)")
                            _ = plt.ylabel("Amplitude (mV)")
                            # plt.legend(loc='best')

                        ii += 1
                        cn_with_peaks += 1

                except Exception as err:
                    # print(err)
                    continue

            # end for nfex

        # end for ndigi

    # end if fex

    # Save per event peaks
    # if cn_smd_peaks > 0: # for non worst-case
    smd.event(evt, peaks=smd_peaks)

    # Collect timing values for all events
    t_ana = time.monotonic()
    txt_ana += str(t_ana - t_det) + ","
    txt_det += str(t_det - t_st) + ","
    txt_tot += str(t_ana - t_st) + ","
    txt_pks += str(len(swf)) + ","

    if nevt % batch_size == 0:
        en_batch = time.time()
        print(
            f"RANK:{rank} processed {nevt} events rate:{(batch_size/(en_batch-st_batch))*1e-3:.2f}kHz",
            flush=True,
        )
        # print((batch_size/(en_batch-st_batch))*1e-3, flush=True)
        st_batch = time.time()

    cn_evts += 1

    if ii > 9 and plot:
        break


# Stop Srv nodes
# smd.done()

comm.Barrier()
t1 = MPI.Wtime()

# cn_with_peaks = comm.gather(cn_with_peaks, root=0)
# cn_evts = comm.gather(cn_evts, root=0)

if rank == 0:
    n_eb_nodes = int(os.environ.get("PS_EB_NODES", "1"))
    n_srv_nodes = int(os.environ.get("PS_SRV_NODES", "0"))
    # print(f'TOTAL TIME:{t1-t0:.2f}s #EB: {n_eb_nodes} #EVT {np.sum(cn_evts)} (with peaks): {np.sum(cn_with_peaks)} rate:{(np.sum(cn_evts)/(t1-t0))*1e-6:.4f}MHz')
    print(
        f"TOTAL TIME:{t1-t0:.2f}s #EB:{n_eb_nodes} #SRV:{n_srv_nodes} smd_batch_size:{smd_batch_size}"
    )

if plot:
    plt.tight_layout()
    plt.savefig("FEX_PKs.pdf", bbox_inches="tight")

writeout = False
if writeout:
    txt_ana = comm.gather(txt_ana, root=0)
    txt_det = comm.gather(txt_det, root=0)
    txt_tot = comm.gather(txt_tot, root=0)
    txt_pks = comm.gather(txt_pks, root=0)

    if rank == 0:
        o_ana = "".join(txt_ana)
        o_det = "".join(txt_det)
        o_tot = "".join(txt_tot)
        o_pks = "".join(txt_pks)

        with open("fex_pks_ana.csv", "w") as f:
            f.write(o_ana)
        with open("fex_pks_det.csv", "w") as f:
            f.write(o_det)
        with open("fex_pks_tot.csv", "w") as f:
            f.write(o_tot)
        with open("fex_pks_pks.csv", "w") as f:
            f.write(o_pks)
