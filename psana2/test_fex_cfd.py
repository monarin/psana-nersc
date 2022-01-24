import matplotlib.pyplot as plt
import numpy as np
from psana import *
from psana.hexanode.PyCFD import PyCFD


# Configure plot
plot = True

# Create datasource
ds = DataSource(exp='tmolv9418', run=175)
myrun = next(ds.runs())
sample_period = 1000e-9/6400*14./13.
showFex = True

det = myrun.Detector('hsd')
hsd = det.raw

seg_chans = hsd._seg_chans()
print('seg_chans {:}'.format(seg_chans))

# lookup constants by segment number
raw_sz = 0
fex_sz = 0
for config in det._configs:
    if not 'hsd' in config.__dict__:
        print('Skipping config {:}'.format(config.__dict__))
        continue
    scfg = getattr(config, 'hsd')

    # Find the maximum raw_sz and fex_sz
    for seg, segcfg in scfg.items():
        if segcfg.config.user.raw.prescale > 0:
            _raw_sz = segcfg.config.user.raw.gate_ns*6.4*13/14
            if _raw_sz > raw_sz:
                raw_sz = _raw_sz
        if segcfg.config.user.fex.prescale>0:
            _fex_sz = segcfg.config.user.fex.gate_ns*6.4*13/14
            if _fex_sz > fex_sz:
                fex_sz = _fex_sz
            print(f'ymin[{seg}] = {segcfg.config.user.fex.ymin}')
            print(f'ymax[{seg}] = {segcfg.config.user.fex.ymax}')

# Compute max_size from max raw_sz and fex_sz
max_size = int((raw_sz + fex_sz)*1.05) # 20 rows * 40 samples/row * raw,sparse
print('raw_sz {:}R  fex_sz {:}R  max_size {:}S'.format(raw_sz,fex_sz,max_size))

# Run peaking finding
CFD_params = {'sample_interval': 1.68269e-10,
  'fraction': 0.35,
  'delay': 0.35e-09,
  'polarity': 'Negative',
  'threshold': 5,
  'walk': 0,
  'timerange_low': 0,
  'timerange_high': 100e-05,
  'offset': 2049}

CFD = PyCFD(CFD_params)
if plot:
    plt.figure(figsize=(10,10))
ii = 1


# Collecting analysis times
max_arr_size = 9
ana_times = np.zeros(max_arr_size, dtype=np.float32)
txt_out = ''

for nevt, evt in enumerate(myrun.events()):
    t_now   = time.time()
    wfs     = hsd.waveforms(evt)
    peaks   = hsd.peaks(evt)
    ts      = evt.timestamp
    seg     = 0
    chan    = 0
    seg_chans[0][0]

    # Sparsified waveform plot
    st_ana = time.monotonic()

    stimes = None
    swf = None
    if peaks and seg in peaks and showFex:
        for i in range(len(peaks[seg][0][0])):
            _s0     = peaks[seg][0][0][i]
            _swf    = peaks[seg][0][1][i]-1
            _ns     = len(_swf)
            _stimes = np.arange(_s0, _s0+_ns)*sample_period

            if stimes is None:
                stimes  = _stimes
                swf     = _swf # single peak
            else:
                stimes  = np.append(stimes, _stimes)
                swf     = np.append(swf, _swf) # all peaks in the waveform
        
        ts = stimes
        vs = swf
        try:
            # pk is the identified arrival time
            pks = CFD.CFD(vs, ts)[0]

            if len(pks)>0:
                if plot:
                    plt.subplot(3,3,ii)
                    plt.plot(ts,vs,marker='o',linestyle='None',markerfacecolor='None',label='isolated peak')                
                    for pk in pks:
                        plt.plot([pk,pk],[plt.ylim()[0],plt.ylim()[1]],'-.',label='identified arrival time')
            
                ii += 1  
            # plt.legend(loc='best')
        except Exception as err:
            #print(err)
            continue
        
        if plot:
            plt.title('Event '+str(nevt))
            plt.xlabel('Time (ns)')
            _=plt.ylabel('Amplitude (mV)')

    # end if peaks
    en_ana = time.monotonic()
    ana_times[ii-1] = en_ana - st_ana
    txt_out += f'{en_ana-st_ana},'

    if ii>=max_arr_size:
        break
    

if plot:
    plt.tight_layout()
    plt.savefig('FEX_PKs.pdf',bbox_inches='tight')


#ana_ms = ana_times[:ii-1] * 1e3
#plt.hist(ana_ms)
#plt.title(f'#evts:{len(ana_ms)} avg:{np.mean(ana_ms):.5f}ms max:{np.max(ana_ms):.5f}ms min:{np.min(ana_ms):.5f}ms')
#plt.show()

with open('out_fex_cfd.csv', 'w') as f:
    f.write(txt_out)
