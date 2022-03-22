""" Converts raw to fex-style waveforms

    Note: 
        modified from lcls2/psana/psana/hexanode/examples/
        ex-22-data-acqiris-peaks-save-h5-xiangli.py
    
    Input raw waveforms:
        time 1 2 3 4 5 6 7 8 9....
        wf = 2 3 4 5 4 3 2 1 1 1 2 3 4 6 3 2 1 1 1
    threshold:
        3
    Output simulated fex data:
        [3,4,5,4,3] starttime 2
        [3,4,6,3] starttime 12
        Output to xtc2 (one stream per one channel)
    
    Tests:
        Output from Roentdek algorithm (xyrt) using raw waveforms is
        compared with what comes out from the simulated fex data.

"""
import logging
logger = logging.getLogger(__name__)

import sys
from time import time

from psana import DataSource

from psana.pyalgos.generic.NDArrUtils import print_ndarr
from psana.pyalgos.generic.Utils import str_kwargs, do_print

import numpy as np

from psana.hexanode.PyCFD import PyCFD
import matplotlib.pyplot as plt

from psana.hexanode.DLDProcessor  import DLDProcessor

import dgrampy as dp
from psana.psexp import TransitionId

USAGE = 'Usage: python %s' % sys.argv[0]

def get_window_from_peaks(wf, wt, peak_ind, window_size, plot=False, 
        CFD=None, sample_period=None, threshold=None):
    """Returns a list of 1D waveforms and start positions.

    Note that no. of windows may not necessary match with no. of peaks. This is
    because adjacent peaks can appear in the same window.

    From given locations of peaks (`peak_ind`), extend the window (both left 
    and right) until it hit the threshold (+/- `window_size`). This is considered 
    as one window and as we move to the next peak_ind, we check if it has been merged
    into the previous window. 
    """
    n_peaks = len(peak_ind)
    pkwin_list = []
    startpos_list = []

    plt.plot(wt, wf, label=f'waveform window_size={window_size}')
    st, en = (0, 0)
    for i_peak, pkind in enumerate(peak_ind):
        # Check if this peak index is included in the previous windows
        if pkind in range(st, en): continue

        st = pkind
        en = pkind 
        threshold = 0.003

        # Walk left
        while wf[st] <= threshold and st > 0:
            st -= 1
        if st > window_size:
            st -= window_size

        # Walk right
        while wf[en] <= threshold and en < wf.shape[0]-1:
            en += 1
        if en < wf.shape[0] - window_size:
            en += window_size 
        pkwin_list.append(wf[st: en])
        startpos_list.append(wt[st])
        #plt.plot(wt[st:en], wf[st:en], label=f'window #{i_peak}')

    result_peaks = test_findpeaks_with_CFD(pkwin_list, startpos_list, CFD, sample_period)
    
    if plot:
        plt.scatter(wt[peak_ind], wf[peak_ind], marker='o', c='r', label='peaks from found indices')
        first_pks = [pkwin[0] for pkwin in pkwin_list]
        plt.scatter(startpos_list, first_pks, marker='x', c='g', label='begin window')
        plt.legend()
        plt.show()
    return pkwin_list, startpos_list, result_peaks

def test_findpeaks_with_CFD(pkwin_list, startpos_list, CFD, sample_period):
    """Test finding peaks from windows. The results should match with
    the original peak finding results `pktsec`.
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
                    startpos_list[ipeak]+(peaks_sizes[ipeak]*sample_period), sample_period)
            stimes[st:en] = _stimes[:peaks_sizes[ipeak]]
            swf[st:en]  = peak 
        
        ts = stimes
        vs = swf
        plt.plot(ts, vs, label=f'long window')
        
        pks = CFD.CFD(vs, ts) 

        if len(pks) > 0:
            peak_ind = np.searchsorted(stimes, pks)
            plt.scatter(pks, swf[peak_ind], marker='o', c='m', label=f'CFD peaks') 
    
    return pks

def dgrampy_start(expt, runnum, out_xtcfname, segment_id, ts):
    """Setup required parameters to create xtc2 from scratch.
    
    Note: ts is the original config timestamp. Only config (
    and L1Accept - see dgrampy_adddata) will have a matching 
    timestamp with the original file. Other transitions are
    just +1 from this config timestamp.
    """
    # NameId setup
    nodeId = 1 
    namesId = {
        "tmo_quadanode": 0,
        "runinfo": 1,
    }

    # Tells dgrampy to write new dgrams to this given output filename
    dp.creatextc2(out_xtcfname)

    # Create config, algorithm, and detector
    config = dp.config(ts=ts)
    alg = dp.alg("fex", 4, 5, 6)
    det = dp.det("tmo_quadanode", "quadanode", "detnum1234")
    ts += 1

    runinfo_alg = dp.alg("runinfo", 0, 0, 1)
    runinfo_det = dp.det("runinfo", "runinfo", "")

    # Define data formats
    datadef_dict = {
        "startpos": (dp.DataType.DOUBLE, 1),
        "waveforms": (dp.DataType.DOUBLE, 1),
        "lengths": (dp.DataType.INT64, 1),
    }
    datadef = dp.datadef(datadef_dict)

    runinfodef_dict = {
        "expt": (dp.DataType.CHARSTR, 1),
        "runnum": (dp.DataType.UINT32, 0),
    }
    runinfodef = dp.datadef(runinfodef_dict)

    # Create Names
    data_names = dp.names(
        config, det, alg, datadef, nodeId=nodeId, namesId=namesId["tmo_quadanode"], segment=segment_id
    )
    runinfo_names = dp.names(
        config,
        runinfo_det,
        runinfo_alg,
        runinfodef,
        nodeId=nodeId,
        namesId=namesId["runinfo"],
        segment=segment_id,
    )
    
    dp.save(config)

    beginrun = dp.dgram(transid=TransitionId.BeginRun, ts=ts)
    beginrun_data = {"expt": expt, "runnum": runnum}
    dp.adddata(beginrun, runinfo_names, runinfodef, beginrun_data)
    dp.save(beginrun)
    ts += 1
    
    beginstep = dp.dgram(transid=TransitionId.BeginStep, ts=ts)
    dp.save(beginstep)
    ts += 1
    
    enable = dp.dgram(transid=TransitionId.Enable, ts=ts)
    dp.save(enable)

    return data_names, datadef

def dgrampy_adddata(data_names, datadef, startpos_list, pkwin_list, ts):
    d0 = dp.dgram(ts=ts)

    # Converts pkwin_list to 1D array and store len of each
    # item in lengths array.
    lengths = np.array([len(pkwin) for pkwin in pkwin_list], dtype=np.int64)
    waveforms = np.zeros(np.sum(lengths), dtype=np.float64)
    for i, pkwin in enumerate(pkwin_list):
        st = np.sum(lengths[:i])
        en = st + lengths[i]
        waveforms[st:en] = pkwin
    print(f'adddata lengths={lengths}')
    print(f'        waveforms={waveforms}')
    print(f'        startpos={np.asarray(startpos_list, dtype=np.float64)}')
    
    data = {
        "startpos": np.asarray(startpos_list, dtype=np.float64),
        "waveforms": waveforms,
        "lengths": lengths,
    }
    dp.adddata(d0, data_names, datadef, data)
    dp.save(d0)

def dgrampy_done(ts):
    """Post-pend all ending transitions."""
    disable = dp.dgram(transid=TransitionId.Disable, ts=ts)
    dp.save(disable)
    ts += 1
    endstep = dp.dgram(transid=TransitionId.EndStep, ts=ts)
    dp.save(endstep)
    ts += 1
    endrun = dp.dgram(transid=TransitionId.EndRun, ts=ts)
    dp.save(endrun)
    dp.closextc2()

def proc_data(**kwargs):

    logger.info(str_kwargs(kwargs, title='Input parameters:'))

    DSNAME       = kwargs.get('dsname', '/reg/g/psdm/detector/data2_test/xtc/data-amox27716-r0100-acqiris-e001000.xtc2')
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


    ds    = DataSource(files=DSNAME)
    orun  = next(ds.runs())
    det   = orun.Detector(DETNAME)
    dldpars = {'consts':det.calibconst}

    # Update calibcfg and calibtab
    kwargs.update(dldpars)

    tb_sec = time()
    nev = 0

    # Counts no. of channels with different no. peaks from CFD(raw) and CFD(win)
    cn_match = 0
    cn_unmatch = 0 
    cn_match_dld = 0
    cn_unmatch_dld = 0

    # Summing differences between each peak from CFD(raw) and CFD(win)
    sum_err = 0
    sum_pks = 0
    
    # Summing differences between x,y,r,t (output from Roentdek)
    sum_err_dld = np.zeros([EVENTS, 4], dtype=np.float64) 

    # Initialize PyCFD per channel
    cfds = {}
    for i_chan in range(NUMCHS):
        CFD_params = PARAMSCFD[i_chan]
        cfds[i_chan] = PyCFD(CFD_params)

    # This is used for calculate Roentdek algorithm (_c is for checking
    # peaks from simulated fex data).
    proc  = DLDProcessor(**kwargs)
    proc_c= DLDProcessor(**kwargs)

    # Initialize dgrampy and generate starting transitions for xtc2
    out_i_chan = 4 
    out_xtcfname = f"data-r0085-s{str(out_i_chan).zfill(3)}-c000.xtc2"
    segment_id = 4
    ts = 0 
    data_names, datadef = dgrampy_start(EXP, RUN, out_xtcfname, segment_id, ts)
    
    ts += 4 # Configure, BeginRun, BeginStep, Enable
    for nev,evt in enumerate(orun.events()):

        if nev<EVSKIP: continue
        if nev>=EVENTS: break


        if do_print(nev): logger.info('Event %4d'%nev)
        t0_sec = time()

        wts = det.raw.times(evt)
        wfs = det.raw.waveforms(evt)

        # Function peaks returns `pktsec` for each channel. We need to locate
        # index of these peaks in wts. The indices will be used to identify
        # windows of waveform wfs and startpos in wts.
        NUMCHS = wfs.shape[0]
        window_size = 8
        nhits = np.zeros(NUMCHS, dtype=np.int64)
        pktsec = np.zeros([NUMCHS, NUMHITS], dtype=wts.dtype)

        nhits_fex = np.zeros(NUMCHS, dtype=np.int64)
        pktsec_fex = np.zeros([NUMCHS, NUMHITS], dtype=wts.dtype)

        for i_chan in range(NUMCHS):
            # Find peaks using CFD
            CFD_params = PARAMSCFD[i_chan]
            CFD = cfds[i_chan]

            pktsec_chan = CFD.CFD(wfs[i_chan,:], wts[i_chan,:])
            nhits_chan = min(len(pktsec_chan), NUMHITS)
            nhits[i_chan] = nhits_chan

            pktsec[i_chan,:nhits_chan] = pktsec_chan[:nhits_chan]

            # Calculate sample interval
            sample_intervals = wts[i_chan,1:] - wts[i_chan,:-1]
            
            # Find peak indices
            peak_ind = np.searchsorted(wts[i_chan,:], pktsec_chan)

            if False:
                plt.plot(wts[i_chan, :], wfs[i_chan,:], label='waveform')
                # Get peak values from found indices
                pktval = wfs[i_chan, peak_ind]
                plt.scatter(pktsec_chan, pktval, marker='o', c='r', label=f'CFD peaks #{nhits[i_chan]}')
                plt.scatter(wts[i_chan, peak_ind], pktval, marker='x', c='g', label=f'ts from found indices #{len(wts[i_chan, peak_ind])}')
                plt.legend()
                plt.show()
            
            
            # Find peak windows
            pkwin_list, startpos_list, result_peaks = get_window_from_peaks(
                    wfs[i_chan,:], wts[i_chan,:], peak_ind, window_size, plot=PLOT,
                    CFD=CFD, sample_period=CFD_params['sample_interval'],
                    threshold=CFD_params['threshold'])
            
            # Save hits and peaks from fex data
            nhits_chan_fex = min(len(result_peaks), NUMHITS)
            nhits_fex[i_chan] = nhits_chan_fex
            pktsec_fex[i_chan,:nhits_chan_fex] = result_peaks[:nhits_chan_fex]

            # Write out one channel at a time (change out_i_chan to switch file)
            if i_chan == out_i_chan:
                dgrampy_adddata(data_names, datadef, startpos_list, pkwin_list, ts)
                ts += 1
            
            # Calculate the differences betwen CFD(raw) and CFD(windows)
            if len(result_peaks) == nhits[i_chan]:
                sum_err += np.sum(np.absolute(np.asarray(pktsec_chan) - np.asarray(result_peaks)))
                sum_pks += nhits[i_chan]
                cn_match += 1
            else:
                cn_unmatch += 1


        # end for i_chan...
        
        # Test RoenDek algorithm
        proc.event_proc(nev, nhits, pktsec)
        proc_c.event_proc(nev, nhits_fex, pktsec_fex)
        xyrt = proc.xyrt_list(nev, nhits, pktsec)
        xyrt_c = proc_c.xyrt_list(nev, nhits_fex, pktsec_fex)
        if len(xyrt) == len(xyrt_c):
            for i, ((x,y,r,t), (x_c,y_c,r_c,t_c)) in enumerate(zip(xyrt, xyrt_c)):
                dx = abs(x-x_c)
                dy = abs(y-y_c)
                dr = abs(r-r_c)
                dt = abs(t-t_c)
                sum_err_dld[nev,:] = [dx, dy, dr, dt]
                print('  ev:%4d hit:%2d dx:%7.3f dy:%7.3f dt:%10.5g dr:%7.3f' % (nev,i,dx,dy,dt,dr))
            cn_match_dld += 1
        else:
            cn_unmatch_dld += 1
        
        if VERBOSE:
            print("  ev:%4d waveforms processing time = %.6f sec" % (nev, time()-t0_sec))
            print_ndarr(wfs,    '    waveforms      : ', last=4)
            print_ndarr(wts,    '    times          : ', last=4)
            print_ndarr(nhits,  '    number_of_hits : ')
        

    # end for nev, evt in...
    dgrampy_done(ts)

    print("Summary ev:%4d processing time = %.6f sec" % (nev, time()-tb_sec))
    print(f"average err per channel: {sum_err/sum_pks} #unmatch: {cn_unmatch} ({(cn_unmatch/(5*nev))*100:.2f} %)")
    print(f"average err(x,y,r,t) per evt:  {np.sum(sum_err_dld, axis=0)/nev} #unmatch: {cn_unmatch_dld} ({(cn_unmatch_dld/nev)*100:.2f} %)")


if __name__ == "__main__":

    logging.basicConfig(format='%(levelname)s: %(message)s', datefmt='%Y-%m-%dT%H:%M:%S', level=logging.INFO)

    tname = sys.argv[1] if len(sys.argv) > 1 else '1'
    print('%s\nTEST %s' % (50*'_', tname))

    kwargs = {'dsname'   : '/reg/g/psdm/detector/data2_test/xtc/data-amox27716-r0085-acqiris-e001000.xtc2',
              'detname'  : 'tmo_quadanode',
              'numchs'   : 5,
              'numhits'  : 16,
              'evskip'   : 0,
              'events'   : 1000,
              'ofprefix' : './',
              'run'      : 85,
              'exp'      : 'amox27716',
              'version'  : 4,
              'DLD'      : True,
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

    proc_data(**kwargs)

    print('\n%s' % USAGE)
    sys.exit('End of %s' % sys.argv[0])

# EOF
