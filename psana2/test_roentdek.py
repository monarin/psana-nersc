from psana import DataSource
from psana.hexanode.PyCFD import PyCFD
from psana.hexanode.DLDProcessor  import DLDProcessor
import numpy as np
from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
import sys, os
import time

from psana.hexanode.DLDStatistics import DLDStatistics
from psana.hexanode.DLDGraphics   import draw_plots

from psana.hexanode.HitFinder import HitFinder

import matplotlib.pyplot as plt

def get_time():
    comm.Barrier()
    return MPI.Wtime()

def find_peaks(pkwin_list, startpos_list, CFD):
    """Finds peaks by concatenating all peak windows and
    populating time series with correct start positions.
    
    Concatenate peak windows into one long array (vs)
    with startpos padding along as another array (ts)
    Example:
    pkwin_list [[1 1 3 1], [1 3 1 1]]
    startpos [0, 7]
    Results:
    vs = [1 1 3 1 1 3 1 1]
    ts = [0 1 2 3 7 8 9 10]

    CFD.CFD is called on vs and ts and the function returns
    a list of peaks.
    """
    peaks_sizes = [peak.shape[0] for peak in pkwin_list]
    arr_size = np.sum(peaks_sizes)
    pks = []

    if arr_size > 0:
        stimes = np.zeros(arr_size)
        swf = np.zeros(arr_size, dtype=pkwin_list[0].dtype)
        for ipeak, peak in enumerate(pkwin_list):
            if ipeak == 0:
                st = 0
            else:
                st = np.sum(peaks_sizes[:ipeak])
            en = st + peaks_sizes[ipeak]
            _stimes = np.arange(startpos_list[ipeak], 
                                startpos_list[ipeak]+(peaks_sizes[ipeak]*CFD.sample_interval), 
                                CFD.sample_interval
                               )
            stimes[st:en] = _stimes[:peaks_sizes[ipeak]]
            swf[st:en]  = peak 
        ts = stimes
        vs = swf
        pks = CFD.CFD(vs, ts) 

    return pks

def proc_data(**kwargs):
    XTCDIR       = kwargs.get('xtcdir', '/cds/home/m/monarin/psana-nersc/psana2/dgrampy/amox27716')
    DETNAME      = kwargs.get('detname','tmo_quadanode')
    EVSKIP       = kwargs.get('evskip', 0)
    EVENTS       = kwargs.get('events', 10) + EVSKIP
    EXP          = kwargs.get('exp', 'amox27716')
    RUN          = kwargs.get('run', 85)
    VERBOSE      = kwargs.get('verbose', True)
    PLOT         = kwargs.get('plot', False)
    OFPREFIX     = kwargs.get('ofprefix','./')
    PARAMSCFD    = kwargs.get('paramsCFD')
    NUMCHS       = kwargs.get('numchs', 5)
    NUMHITS      = kwargs.get('numhits', 16)
    TESTMODE     = kwargs.get('testmode', 1)
    ROENTDEK     = kwargs.get('roentdek', 'dldproc')
    MONITOR      = kwargs.get('monitor', False)
    DETECTORS    = kwargs.get('detectors', 1)

    # Open datasource
    ds = DataSource(exp=EXP, 
                    run=RUN, 
                    dir=XTCDIR, 
                    max_events=EVENTS,
                    monitor=MONITOR,
                   )
    run = next(ds.runs())
    det = run.Detector("tmo_quadanode")
    
    # Hidden-rank problem
    if det:
        # Update calibration constants
        dldpars = {'consts':det.calibconst}
        kwargs.update(dldpars)
        
        # Initialize PyCFD per channel
        cfds = {}
        for i_chan in range(NUMCHS):
            cfds[i_chan] = PyCFD(PARAMSCFD[i_chan])
        
        # Intitialize Roentdek wrapper and Xiang's hitfinder
        proc  = DLDProcessor(**kwargs)
        HF = HitFinder(kwargs)
        if PLOT: stats = DLDStatistics(proc,**kwargs)

        # Collect batch rate with t0 and t1
        t0 = time.monotonic()

        # Find peaks for each channel and saves them in a fixed
        # size array for running Roentdek algorithms
        cn_no_peaks_events = 0
        cn_peaks = np.zeros(EVENTS, dtype=np.int64)
        dt_pks = np.zeros(EVENTS, dtype=np.float64)
        dt_rtks = np.zeros(EVENTS, dtype=np.float64)
        
        # Aux arrays for passing N-channels data to Roentdek
        nhits_fex = np.zeros(NUMCHS * DETECTORS, dtype=np.int64)
        pktsec_fex = np.zeros([NUMCHS * DETECTORS, NUMHITS], dtype=np.float64)

    # Setup srv nodes if writing is requested
    if TESTMODE == 4:
        smd_batch_size = 1000
        smd = ds.smalldata(filename='/cds/data/drpsrcf/users/monarin/amox27716/out/mysmallh5.h5', 
                           batch_size=smd_batch_size, 
                          )
    
    for i_ev, evt in enumerate(run.events()):
        if VERBOSE: print(f'EVENT: {i_ev}')
        
        # Get list of waveforms and startpos by segment id
        waveforms = det.fex.waveforms(evt, n_dets=DETECTORS)
        times = det.fex.times(evt, n_dets=DETECTORS)

        # Run peakfinder
        # For > 1 detector, we get new detector at every NUMCHS streams.
        # Note that we reuse PyCFD for all detectors (for testing).
        t0_pk = time.monotonic()
        if TESTMODE in (2, 3, 4):
            n_result_peaks = np.zeros(NUMCHS * DETECTORS, dtype=np.int64)
            for i_det in range(DETECTORS):
                for i_chan in range(NUMCHS):
                    seg_id = int(i_det * NUMCHS + i_chan)
                    # TODO: Eliminate sample_interval
                    result_peaks = find_peaks(waveforms[seg_id], 
                                              times[seg_id], 
                                              cfds[i_chan], 
                                             )
                    
                    n_result_peaks[seg_id] = len(result_peaks)
                    if VERBOSE: print(f'  det: {i_det} chan:{i_chan} #peaks:{len(result_peaks)}')
                    
                    # Save hits and peaks from fex data
                    nhits_chan_fex = min(len(result_peaks), NUMHITS)
                    nhits_fex[seg_id] = nhits_chan_fex
                    pktsec_fex[seg_id,:nhits_chan_fex] = result_peaks[:nhits_chan_fex]
                    pktsec_fex[seg_id,nhits_chan_fex:] = 0
                
            if np.all(n_result_peaks==0): cn_no_peaks_events += 1
            cn_peaks[i_ev] = np.prod(n_result_peaks + 1)
        t1_pk = time.monotonic()
        dt_pks[i_ev] = t1_pk - t0_pk

        # Run Roentdek
        t0_rtk = time.monotonic()
        rt_hits = np.zeros([DETECTORS, NUMHITS, 4], dtype=np.float64)
        if TESTMODE in (3, 4) and np.sum(n_result_peaks) > 0:
            for i_det in range(DETECTORS):
                st = int(i_det * NUMCHS)
                en = st + NUMCHS

                if ROENTDEK == 'dldproc':
                    # Roentdek wrapper
                    # TODO: With Mikhail - eliminate i_ev
                    proc.event_proc(i_ev, nhits_fex[st:en], pktsec_fex[st:en, :])
                    for i,(x,y,r,t) in enumerate(proc.xyrt_list(i_ev, nhits_fex[st:en], pktsec_fex[st:en,:])):
                        # Allow saving upto NUMHITS
                        if i == NUMHITS: break
                        rt_hits[i_det, i, :] = [x,y,r,t]
                        if VERBOSE: print('    hit:%2d x:%7.3f y:%7.3f t:%10.5g r:%7.3f' % (i,x,y,t,r))
                else: 
                    # Xiang's peakfinding
                    HF.FindHits(pktsec_fex[4,:nhits_fex[4]],
                            pktsec_fex[0,:nhits_fex[0]],
                            pktsec_fex[1,:nhits_fex[1]],
                            pktsec_fex[2,:nhits_fex[2]],
                            pktsec_fex[3,:nhits_fex[3]])
                    xs1,ys1,ts1 = HF.GetXYT()
                    if VERBOSE: print(f'xs1={xs1} ys1={ys1} ts1={ts1}')

                if PLOT: stats.fill_data(nhits_fex[st:en], pktsec_fex[st:en, :])

        t1_rtk = time.monotonic()
        dt_rtks[i_ev] = t1_rtk - t0_rtk

        # Calculate batch rate
        if i_ev % 1000 == 0 and i_ev > 0:
            t1 = time.monotonic()
            print(f'RANK: {rank} RATE: {(1000/(t1-t0))*1e-3:.2f} kHz')
            t0 = time.monotonic()

        if TESTMODE == 4:
            smd.event(evt, peaks=pktsec_fex, hits=rt_hits)

    # end for i_ev in...
    if TESTMODE == 4:
        smd.done()

    if PLOT:
        draw_plots(stats, prefix=OFPREFIX+EXP+f'-r{str(RUN).zfill(4)}', do_save=True, hwin_x0y0=(0,10))

    # Plot correlation between calc. time and #peaks and histogram of calc.time
    #plt.subplot(2,2,1)
    #plt.hist(dt_pks*1e3)
    #plt.title('Histogram of peak finding time (ms)')
    #plt.subplot(2,2,2)
    #plt.scatter(cn_peaks, dt_pks*1e3)
    #plt.title('CC of #peaks and peakfinding time (ms)')
    #plt.subplot(2,2,3)
    #plt.hist(dt_rtks*1e3)
    #plt.title('Histogram of Roentdek calc. time (ms)')
    #plt.subplot(2,2,4)
    #plt.scatter(cn_peaks, dt_rtks*1e3)
    #plt.title('CC of #np.prod(peaks+1) and Roentdek calc. time (ms)')
    #plt.show()

    #ind = cn_peaks == 0
    #plt.subplot(2,1,1)
    #plt.plot(dt_rtks[ind])
    #plt.title('Roentdek Calc. Time (s.) for Zero-peak events')
    #plt.subplot(2,1,2)
    #plt.plot(cn_peaks[ind])
    #plt.show()
    
    if VERBOSE: print(f'EVENTS={EVENTS} NO PEAK EVENTS={cn_no_peaks_events}')


if __name__ == "__main__":
    # Show rank 0 pid for Prometheus query
    if rank == 0:
        print(f'RANK 0 PID: {os.getpid()}', flush=True)

    # Input for scaling test (from run_slac.sh)
    testmode = 1
    if len(sys.argv) > 1:
        testmode = int(sys.argv[1])
    max_events = 0
    if len(sys.argv) > 2:
        max_events = int(sys.argv[2])
    detectors = 1
    if len(sys.argv) > 3:
        detectors = int(sys.argv[3])
    roentdek_alg = "dldproc"
    if len(sys.argv) > 4:
        roentdek_alg = sys.argv[4]

    # To test correct reading performance, we need to use the folder with 
    # correct no. of stream files. This is because PSANA2 reads everything.
    if detectors == 1:
        xtc_dir = '/cds/data/drpsrcf/users/monarin/amox27716/big' # 5 streams
    else:
        xtc_dir = '/cds/data/drpsrcf/users/monarin/amox27716/xtc' # 10 streams

    kwargs = {'xtcdir'   : xtc_dir,
              'detname'  : 'tmo_quadanode',
              'numchs'   : 5,
              'numhits'  : 16,
              'evskip'   : 0,
              'events'   : max_events,
              'ofprefix' : './',
              'run'      : 85,
              'exp'      : 'amox27716',
              'version'  : 4,
              'DLD'      : True,
              'testmode' : testmode,
              'roentdek' : roentdek_alg,
              'monitor'  : False,
              'detectors': detectors,
              'paramsCFD': {0: {'channel': 'mcp',
                              'delay': 1e-8,
                              'fraction': 0.35,
                              'offset': 0.042,
                              'polarity': 'Negative',
                              'sample_interval': 2.5e-10,
                              'threshold':  0.028,
                              'timerange_high': 1e-05,
                              'timerange_low': 1e-06,
                              'walk': 0},
                              1: {'channel': 'x1',
                              'delay': 3.997500000000001e-09,
                              'fraction': 0.35,
                              'offset': 0.032654320557811034,
                              'polarity': 'Negative',
                              'sample_interval': 2.5e-10,
                              'threshold': 0.048439800379417808,
                              'timerange_high': 1e-05,
                              'timerange_low': 1e-06,
                              'walk': 0},
                             2: {'channel': 'x2',
                               'delay': 4.712500000000001e-09,
                              'fraction': 0.35,
                              'offset': 0.058295909692775157,
                              'polarity': 'Negative',
                              'sample_interval': 2.5e-10,
                              'threshold': 0.062173077232695384,
                              'timerange_high': 1e-05,
                              'timerange_low': 1e-06,
                              'walk': 0},
                             3: {'channel': 'y1',
                              'delay': 4.5435e-09,
                              'fraction': 0.35,
                              'offset': 0.01740340726630819,
                              'polarity': 'Negative',
                              'sample_interval': 2.5e-10,
                              'threshold': 0.035850750860370109,
                              'timerange_high': 1e-05,
                              'timerange_low': 1e-06,
                              'walk': 0},
                             4: {'channel': 'y2',
                              'delay': 4.140500000000001e-09,
                              'fraction': 0.35,
                              'offset': 0.0088379291811293368,
                              'polarity': 'Negative',
                              'sample_interval': 2.5e-10,
                              'threshold': 0.035254198205580331,
                              'timerange_high': 1e-05,
                              'timerange_low': 1e-06,
                              'walk': 0}}}
    # Parameters of the CFD descriminator for hit time finding algotithm
    cfdpars= {'cfd_base'       :  0.,
              'cfd_thr'        : -0.05,
              'cfd_cfr'        :  0.85,
              'cfd_deadtime'   :  10.0,
              'cfd_leadingedge':  True,
              'cfd_ioffsetbeg' :  1000,
              'cfd_ioffsetend' :  2000,
              'cfd_wfbinbeg'   :  6000,
              'cfd_wfbinend'   : 22000,
             }
    kwargs.update(cfdpars)

    # Parameters of the HitFinder (Xiang's algorithm)
    hfpars = {
              'runtime_u' : 90,
              'runtime_v' : 100,
              'tsum_avg_u' : 130,
              'tsum_avg_v' : 141,
              'tsum_hw_u' : 6,
              'tsum_hw_v' : 6,
              'f_u' : 1,
              'f_v' : 1,
              'Rmax': 45,
             }
    kwargs.update(hfpars)
    

    t0 = get_time()
    proc_data(**kwargs)
    t1 = get_time()

    if rank == 0:
        nev = kwargs['events']
        
        # Use total no. of events
        if nev == 0: nev = 29790007

        n_ebs = os.environ.get('PS_EB_NODES', '1')
        n_srvs = os.environ.get('PS_SRV_NODES', '0')

        print(f"EVENTS: {nev} MODE: {kwargs['testmode']} #EB: {n_ebs} #SRV: {n_srvs} ELAPSED TIME: {t1-t0:.2f}s TOTALRATE: {(nev/(t1-t0))*1e-3:.4f}kHz")
