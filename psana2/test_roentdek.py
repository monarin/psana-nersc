from psana import DataSource
from psana.hexanode.PyCFD import PyCFD
from psana.hexanode.DLDProcessor  import DLDProcessor
import numpy as np

def find_peaks(pkwin_list, startpos_list, CFD, sample_period):
    """Finds peaks by concatenating all peak windows and
    populating time series with correct start positions.
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

    # Open datasource
    ds = DataSource(exp=EXP, run=RUN, dir=XTCDIR)
    run = next(ds.runs())
    det = run.Detector("tmo_quadanode")
    
    # Update calibration constants
    dldpars = {'consts':det.calibconst}
    kwargs.update(dldpars)
    
    # Initialize PyCFD per channel
    cfds = {}
    for i_chan in range(NUMCHS):
        cfds[i_chan] = PyCFD(PARAMSCFD[i_chan])
    
    # Intitialize Roentdek wrapper
    proc  = DLDProcessor(**kwargs)

    # Find peaks for each channel and saves them in a fixed
    # size array for running Roentdek algorithms
    for i_ev, evt in enumerate(run.events()):
        nhits_fex = np.zeros(NUMCHS, dtype=np.int64)
        pktsec_fex = np.zeros([NUMCHS, NUMHITS], dtype=np.float64)

        # Run peakfinder
        for i_chan in range(NUMCHS):
            result_peaks = find_peaks(det.fex.waveforms(evt, i_chan), 
                                      det.fex.times(evt, i_chan), 
                                      cfds[i_chan], 
                                      PARAMSCFD[i_chan]['sample_interval']
                                     )
            
            #print(i_ev, i_chan, result_peaks)
            
            # Save hits and peaks from fex data
            nhits_chan_fex = min(len(result_peaks), NUMHITS)
            nhits_fex[i_chan] = nhits_chan_fex
            pktsec_fex[i_chan,:nhits_chan_fex] = result_peaks[:nhits_chan_fex]

        # Run Roentdek
        proc.event_proc(i_ev, nhits_fex, pktsec_fex)
        for i,(x,y,r,t) in enumerate(proc.xyrt_list(i_ev, nhits_fex, pktsec_fex)):
            print('ev:%4d hit:%2d x:%7.3f y:%7.3f t:%10.5g r:%7.3f' % (i_ev, i,x,y,t,r))

if __name__ == "__main__":
    kwargs = {'xtcdir'   : '/cds/home/m/monarin/psana-nersc/psana2/dgrampy/amox27716',
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
