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
from psana.psexp.updatestore import UpdateStore

def filter(evt):
    return True

if __name__ == "__main__":
    nfiles = 16
    max_events = 10
    batch_size = 1
    os.environ['PS_SMD_N_EVENTS']=str(batch_size)

    smd_files = np.asarray(['/reg/neh/home/monarin/data/smalldata/data-r0001-s%s.smd.xtc2'%str(i).zfill(2) for i in range(nfiles)])
    xtc_files = np.asarray(['/reg/neh/home/monarin/data/data-r0001-s%s.xtc2'%str(i).zfill(2) for i in range(nfiles)])

    smd_dm = DgramManager(smd_files)
    configs = smd_dm.configs
    dm = DgramManager(xtc_files, configs=configs)
    
    epics_store = UpdateStore(configs, 'epics')

    ev_man = EventManager(configs, dm, filter_fn=filter)
   
    #get smd chunks
    smdr_man = SmdReaderManager(smd_dm.fds, max_events)
    eb_man = EventBuilderManager(configs, batch_size, filter)
    n_events = 0
    delta_t = []
    for i, (smd_chunk, update_chunk) in enumerate(smdr_man.chunks()):
        update_pf = PacketFooter(view=update_chunk)
        update_views = update_pf.split_packets()
        epics_store.update(update_views)
        for idx, update in enumerate(epics_store._update_list):
            print(idx, update.n_items)

        for j, batch_dict in enumerate(eb_man.batches(smd_chunk)):
            batch, _ = batch_dict[0]
            st = time.time()
            for k, evt in enumerate(ev_man.events(batch)):
                en = time.time()
                vals = epics_store.values([evt], 'HX2:DVD:GCC:01:PMON')
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
