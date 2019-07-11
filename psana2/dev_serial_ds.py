"""
from psana.eventbuilder import EventBuilder

views=[]
views.append(memoryview(bytearray(b'abc')))
views.append(memoryview(bytearray(b'def')))
views.append(memoryview(bytearray(b'ghi')))

ev = EventBuilder(views, None)
#ev.testme()
"""
from psana import dgram
from psana.psexp.smdreader_manager import SmdReaderManager
from psana.psexp.eventbuilder_manager import EventBuilderManager
import os, time, glob
import numpy as np
from psana.psexp.packet_footer import PacketFooter
from psana.psexp.event_manager import EventManager
from psana.dgrammanager import DgramManager
from psana.psexp.epicsstore import EpicsStore
from psana.psexp.epicsreader import EpicsReader

def filter(evt):
    return True

if __name__ == "__main__":
    nfiles = 1
    max_events = 1000
    batch_size = 1
    os.environ['PS_SMD_N_EVENTS']=str(batch_size)

    #smd_files = np.asarray(['/ffb01/mona/xtc2/smalldata/data-r0001-s%02d.smd.xtc2'%i for i in range(nfiles)])
    #xtc_files = np.asarray(['/ffb01/mona/xtc2/data-r0001-s%02d.xtc2'%i for i in range(nfiles)])
    
    smd_files = np.asarray(['/reg/neh/home/monarin/lcls2/tmp2/smalldata/data-r0001-s00.smd.xtc2'])
    xtc_files = np.asarray(['/reg/neh/home/monarin/lcls2/tmp2/data-r0001-s00.xtc2'])

    smd_dm = DgramManager(smd_files)
    smd_configs = smd_dm.configs
    dm = DgramManager(xtc_files)
    
    #epics_file = '/reg/d/psdm/xpp/xpptut15/scratch/mona/xtc2/data-r0001-epc.xtc2'
    #epics_reader = EpicsReader(epics_file)
    #epics_store = EpicsStore()

    ev_man = EventManager(smd_configs, dm, filter_fn=filter)
   
    #get smd chunks
    smdr_man = SmdReaderManager(smd_dm.fds, max_events)
    eb_man = EventBuilderManager(smd_configs, batch_size, filter)
    n_events = 0
    delta_t = []
    for i, chunk in enumerate(smdr_man.chunks()):
        #epics_store.update(epics_reader.read(), epics_reader._config, min_ts=smdr_man.min_ts)
        for j, batch_dict in enumerate(eb_man.batches(chunk)):
            batch, _ = batch_dict[0]
            #batch = batch_dict
            st = time.time()
            for k, evt in enumerate(ev_man.events(batch)):
                en = time.time()
                #epics_evt = epics_store.checkout_by_events([evt])[0]
                delta_t.append((en - st)*1000)
                st = time.time()
                n_events += 1

    delta_thres = 1
    delta_t = np.asarray(delta_t) 
    delta_t_sml = delta_t[delta_t < delta_thres]
    delta_t_big = delta_t[delta_t >= delta_thres] / 1000 # unit in seconds
    total_t = np.sum(delta_t)/ 1000 # unit in seconds
    
    print('n_events: %d batch_size: %d '%(n_events, batch_size))
    
    if len(delta_t_sml) > 0:
        print('#fast_evts: %d mean (ms) %6.4f min %6.4f max %6.4f std %6.4f'%(len(delta_t_sml), np.mean(delta_t_sml), np.min(delta_t_sml), np.max(delta_t_sml), np.std(delta_t_sml)))

    if len(delta_t_big) > 0:
        print('Batch read (s) mean: %6.4f min: %6.4f max: %6.4f std: %6.4f'%(np.mean(delta_t_big), np.min(delta_t_big), np.max(delta_t_big), np.std(delta_t_big)))
        print('#points > %d ms: %d'%(delta_thres, len(delta_t_big)))
    
    print('Total Elapsed (s): %6.2f Rate (kHz): %6.2f Bandwidth (MB/s): %6.2f'%(total_t, max_events/ (total_t*1000), (737 * nfiles * max_events) / (total_t * 1000000)))
