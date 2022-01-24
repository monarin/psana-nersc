from psana import DataSource
from psana.hexanode.PyCFD import PyCFD
import matplotlib.pyplot as plt
import numpy as np

ds = DataSource(exp='tmox42619',run=126,max_events=100)
run = next(ds.runs())
hsd = run.Detector('hsd')


##CFD parameters
CFD_params = {'sample_interval': 1.68269e-10,
  'fraction': 0.35,
  'delay': 0.6e-09,
  'polarity': 'Negative',
  'threshold': 10,
  'walk': 0,
  'timerange_low': 0,
  'timerange_high': 100e-05,
  'offset': 2049}
CFD = PyCFD(CFD_params)

# For reconstructing time array.
rate = (6.4*(13/14))    #GHz
interval_ns = (1/rate)  #Nanoseconds 
arr_size = 1000
interval_arr = np.arange(0, interval_ns*arr_size, interval_ns)

plot = True 

for nevt, evt in enumerate(run.events()):
    #wf = hsd.raw.waveforms(evt)
    fex = hsd.raw.peaks(evt)
    
    if not fex: assert fex is None
       
    if fex:
        for ndigi,(digitizer,fexdata) in enumerate(fex.items()):
            for nfex,(channel,fexchan) in enumerate(fexdata.items()):
                startpos,peaks = fexchan
                for npeak,(start,peak) in enumerate(zip(startpos,peaks)):
                    peaklen = len(peak)

                    # Create an array of time starting from "start" with a specified interval
                    ts = interval_arr + start 
                    vs = peak
                    pk = CFD.CFD(vs,ts[:peaklen])
                    print('nevt:',nevt,'ndigi:',ndigi,'nfex:',nfex,'npeak:',npeak,'start:',start,'peaklen:',peaklen, 'pk:', pk)
                    if plot:
                        print(f'vs={vs}')
                        print(f'ts={ts[:peaklen]}')
                        print(f'pk={pk}')
                        plt.figure(figsize=(9,5))
                        plt.plot(ts[:peaklen],vs,marker='o',markerfacecolor='None',label='isolated peak')
                        #plt.plot([pk[0],pk[0]],[plt.ylim()[0],plt.ylim()[1]],'-.',label='identified arrival time')
                        plt.legend(loc='best')
                        plt.xlabel('Time (ns)')
                        plt.ylabel('Amplitude (mV)')
                        plt.show()

 
