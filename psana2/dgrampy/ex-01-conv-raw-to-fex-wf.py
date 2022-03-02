""" Converts raw to fex-style waveforms

    Note: 
        modified from lcls2/psana/psana/hexanode/examples/
        ex-22-data-acqiris-peaks-save-h5-xiangli.py
    Input raw waveforms:
        time 1 2 3 4 5 6 7 8 9....
        wf = 2 3 4 5 4 3 2 1 1 1 2 3 4 6 3 2 1 1 1
    threshold:
        3
    Output fex peaks:
        [3,4,5,4,3] starttime 2
        [3,4,6,3] starttime 12
"""
import logging
logger = logging.getLogger(__name__)

import sys
from time import time

from psana import DataSource
from psana.hexanode.WFPeaks import WFPeaks

from psana.pyalgos.generic.NDArrUtils import print_ndarr
from psana.pyalgos.generic.Utils import str_kwargs, do_print

import numpy as np

from psana.hexanode.PyCFD import PyCFD
import matplotlib.pyplot as plt

USAGE = 'Usage: python %s' % sys.argv[0]

def get_window_from_peaks(wf, wt, peak_ind, window_size, plot=False, 
        CFD=None, sample_period=None):
    """Returns a list of 1D waveforms and start positions.
    
    From each peak index in `peak_ind`, copy waveform per channel
    wf[i_peak, -window_size+1 to window_size] 
    to a new array. 

    If CFD peakfinder is given, calculate peak from the caputured window.
    """
    n_peaks = len(peak_ind)
    peaks_arr = np.zeros([n_peaks, window_size], dtype=wf.dtype)
    startpos_arr = np.zeros(n_peaks, dtype=wt.dtype)

    plt.plot(wt, wf, label=f'waveform window_size={window_size}')
    for i_peak, pkind in enumerate(peak_ind):
        print(f'    i_peak={i_peak} start peak: {wt[pkind]} pkind={pkind}')
        peaks_arr[i_peak,:] = wf[pkind: pkind+window_size]
        startpos_arr[i_peak] = wt[pkind]
        plt.plot(wt[pkind: pkind+window_size], wf[pkind: pkind+window_size], label=f'window #{i_peak}')

    if plot:
        plt.scatter(wt[peak_ind], wf[peak_ind], marker='o', c='r', label='peaks from found indices')
        result_peaks = test_findpeaks_with_CFD(peaks_arr, startpos_arr, CFD, sample_period)
        plt.legend()
        plt.show()
    return peaks_arr, startpos_arr

def test_findpeaks_with_CFD(peaks_arr, startpos_arr, CFD, sample_period):
    """Test finding peaks from windows. The results should match with
    the original peak finding results `pktsec`.
    """
    result_peaks = np.zeros(peaks_arr.shape[0], dtype=peaks_arr.dtype)
    for i_peak in range(peaks_arr.shape[0]):
        ts = np.array([startpos_arr[i_peak] + (i * sample_period) \
                for i in range(peaks_arr.shape[1])])
        #pks = CFD.CFD(peaks_arr[i_peak,:], ts) 
        print(f'i_peak={i_peak}')
        print(f'peaks_arr[i_peak,:]={peaks_arr[i_peak,:].shape} {peaks_arr[i_peak,:]}')
        print(f'ts={ts.shape} {ts}')
        #print(f'pks={pks}')
    return result_peaks

def proc_data(**kwargs):

    logger.info(str_kwargs(kwargs, title='Input parameters:'))

    DSNAME       = kwargs.get('dsname', '/reg/g/psdm/detector/data2_test/xtc/data-amox27716-r0100-acqiris-e001000.xtc2')
    DETNAME      = kwargs.get('detname','tmo_quadanode')
    EVSKIP       = kwargs.get('evskip', 0)
    EVENTS       = kwargs.get('events', 10) + EVSKIP
    EXP          = kwargs.get('exp', 'amox27716')
    RUN          = kwargs.get('run', 100)
    VERBOSE      = kwargs.get('verbose', True)
    PLOT         = kwargs.get('plot', True)
    OFPREFIX     = kwargs.get('ofprefix','./')
    PARAMSCFD    = kwargs.get('paramsCFD')

    peaks = WFPeaks(**kwargs)

    ds    = DataSource(files=DSNAME)
    orun  = next(ds.runs())
    det   = orun.Detector(DETNAME)

    tb_sec = time()
    nev = 0
    for nev,evt in enumerate(orun.events()):

        if nev<EVSKIP: continue
        if nev>EVENTS: break

        if do_print(nev): logger.info('Event %4d'%nev)
        t0_sec = time()

        wts = det.raw.times(evt)
        wfs = det.raw.waveforms(evt)

        nhits, pkinds, pkvals, pktsec = peaks(wfs,wts) # ACCESS TO PEAK INFO

        # Function peaks returns `pktsec` for each channel. We need to locate
        # index of these peaks in wts. The indices will be used to identify
        # windows of waveform wfs and startpos in wts.
        n_chans = len(nhits)
        window_size = 64
        print(f'nev={nev}')

        for i_chan in range(n_chans):
            print(f'  i_chan={i_chan}/{n_chans} dtype: pktsec={pktsec.dtype} wts={wts.dtype}')
            print(f'  nhits={nhits[i_chan]}')
            print(f'  pktsec={pktsec[i_chan]}')
            
            # Calculate sample interval
            sample_intervals = wts[i_chan,1:] - wts[i_chan,:-1]
            #print(f'  sample_intervals={sample_intervals}')
            
            # Find peak indices
            peak_ind = np.searchsorted(wts[i_chan,:], pktsec[i_chan][:nhits[i_chan]])
            print(f'  pktsec*={wts[i_chan, peak_ind]}')

            if PLOT:
                plt.plot(wts[i_chan, :], wfs[i_chan,:], label='waveform')
                # Get peak values from found indices
                pktval = wfs[i_chan, peak_ind]
                plt.scatter(pktsec[i_chan, :nhits[i_chan]], pktval, marker='o', c='r', label=f'CFD peaks #{nhits[i_chan]}')
                plt.scatter(wts[i_chan, peak_ind], pktval, marker='x', c='g', label=f'ts from found indices #{len(wts[i_chan, peak_ind])}')
                plt.legend()
                plt.show()
            
            # Use CFD to verify that peak windows returns correct peaks
            CFD_params = PARAMSCFD[i_chan]
            CFD = PyCFD(CFD_params)
            
            # Find peak windows
            peaks_arr, startpos_arr = get_window_from_peaks(
                    wfs[i_chan,:], wts[i_chan,:], peak_ind, window_size, plot=PLOT,
                    CFD=CFD, sample_period=CFD_params['sample_interval'])

            break
            
            n_peaks = nhits[i_chan]
            for i_peak in range(n_peaks):
                print(f'    i_peak={i_peak}')
                print(f'    peaks={peaks_arr[i_peak,:]}')
                print(f'    startpos={startpos_arr[i_peak]}')
            
        if VERBOSE:
            print("  ev:%4d waveforms processing time = %.6f sec" % (nev, time()-t0_sec))
            print_ndarr(wfs,    '    waveforms      : ', last=4)
            print_ndarr(wts,    '    times          : ', last=4)
            print_ndarr(nhits,  '    number_of_hits : ')
            print_ndarr(pktsec, '    peak_times_sec : ', last=4)


    print("  ev:%4d processing time = %.6f sec" % (nev, time()-tb_sec))


if __name__ == "__main__":

    logging.basicConfig(format='%(levelname)s: %(message)s', datefmt='%Y-%m-%dT%H:%M:%S', level=logging.INFO)

    tname = sys.argv[1] if len(sys.argv) > 1 else '1'
    print('%s\nTEST %s' % (50*'_', tname))

    kwargs = {'dsname'   : '/reg/g/psdm/detector/data2_test/xtc/data-amox27716-r0100-acqiris-e001000.xtc2',
              'detname'  : 'tmo_quadanode',
              'numchs'   : 5,
              'numhits'  : 16,
              'evskip'   : 0,
              'events'   : 0,
              'ofprefix' : './',
              'run'      : 100,
              'exp'      : 'amox27716',
              'version'  : 4,
              'DLD'      : True,
              'paramsCFD': {0: {'channel': 'mcp',
                              'delay': 3.068e-09,
                              'fraction': 0.35,
                              'offset': 0.054470544805354439,
                              'polarity': 'Negative',
                              'sample_interval': 2.5e-10,
                              'threshold': 0.056374120466532174,
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
