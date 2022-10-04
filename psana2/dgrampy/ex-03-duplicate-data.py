from psana.dgramedit import DgramEdit, PyXtcFileIterator
import os, sys, time
from psana.psexp import TransitionId

# Input file, no. of events (needed to determine #L1),
# and duplication factor (n_dups).
#
#ifname = '/cds/home/m/monarin/xtc1to2/examples/data/amo06516-r0090-s000-c000.xtc2'
#n_events = 127
#n_req_L1 = 120
#n_dups = 8534 
#
#ifname = '/cds/data/drpsrcf/users/monarin/tmolv9418/tmolv9418-r0175-s000-c000.xtc2'
#n_events = 35684        # all events in the xtc2 file
#n_req_L1 = 10
#n_dups = 1
#first_L1_offset = 16783748 
#
stream_id = int(sys.argv[1])
ifname = f'/cds/data/drpsrcf/rix/rixl1013320/xtc/rixl1013320-r0093-s00{stream_id}-c000.xtc2'
n_events = 24811        # all events in the xtc2 file
n_req_L1 = 24811        # subset of L1 in the original file (set to n_events for all L1)
n_dups = 1              # No. of times, we'll duplicate the events in the input file
n_L1_dups =320           # For data with SlowUpdate, we'll duplicate L1 in between the two SlowUpdates
first_L1_offsets = [146408,25844,62668,6052,6052,10648,65411,95590,95590,95590]
first_L1_offset = first_L1_offsets[stream_id]

cn_ts= 0

def next_ts():
    global cn_ts
    current_ts = cn_ts
    cn_ts +=1
    return current_ts
    
# Output buffer for DgramEdit and write-out file
obuf = bytearray(4000000)
ofname = f'/cds/data/drpsrcf/users/monarin/rixl1013320/small{n_L1_dups}x/rixl1013320-r0093-s00{stream_id}-c000.xtc2'
out_f = open(ofname, 'wb')
print(f'write to {ofname}', flush=True)

# Open and point to fd with a buffer of max dgram size
fd = os.open(ifname, os.O_RDONLY)
pyiter = PyXtcFileIterator(fd, 0x10000000)


# Start writing out dgrams in N duplicates
cn_events = 0
cn_L1_events = 0
bfname = './tmpl1.xtc2'
buf_f = open(bfname, 'wb')

for i_dup in range(n_dups):
    while True:
        try:
            pydg = pyiter.next()
        except Exception:
            print(f'Done with {i_dup} duplications')
            break

        if pydg.service() == TransitionId.Configure:
            config = DgramEdit(pydg)
            config.updatetimestamp(next_ts())
            config.save(obuf)
            out_f.write(obuf[:config.size])
            cn_events += 1
        else:
            flag_write = True
            if (pydg.service() in (TransitionId.BeginRun, TransitionId.BeginStep, TransitionId.Enable) and i_dup > 0) \
                or (pydg.service() in (TransitionId.Disable, TransitionId.EndStep, TransitionId.EndRun) and i_dup < n_dups-1):
                flag_write = False
            
            if flag_write:
                # We'll duplicates all L1 DgramEdit that have been saved in the batch
                # and clear this batch when we see SlowUpdate.
                if pydg.service() == TransitionId.SlowUpdate:
                    if cn_L1_events > 0:
                        buf_f.close()
                        t0 = time.time()
                        cn_L1_dup_events = 0
                        for i_L1_dup in range(n_L1_dups):
                            fd_L1 = os.open(bfname, os.O_RDONLY)
                            pyiter_L1 = PyXtcFileIterator(fd_L1, 0x10000000)
                            while True:
                                try:
                                    pydg_L1 = pyiter_L1.next()
                                except Exception:
                                    os.close(fd_L1)
                                    break

                                dg_L1 = DgramEdit(pydg_L1, config=config)
                                dg_L1.updatetimestamp(next_ts())
                                if stream_id == 6:
                                    dg_L1.removedata('atmopal', 'raw')
                                dg_L1.save(obuf)
                                out_f.write(obuf[:dg_L1.size])
                                cn_events += 1
                                cn_L1_dup_events += 1
                        buf_f = open(bfname, 'wb')
                        t1 = time.time()
                        print(f'processed: ({cn_L1_dup_events}/{cn_L1_events}) {cn_L1_dup_events/cn_L1_events} elapsed time:{t1-t0:.2f}s.', flush=True)
                        cn_L1_events = 0
                
                dg = DgramEdit(pydg, config=config)
                dg.updatetimestamp(next_ts())
                if pydg.service() == TransitionId.L1Accept and stream_id == 6:  # For stream 6 rixl1013320, L1 data is removed
                    dg.removedata('atmopal', 'raw')
                dg.save(obuf)
                out_f.write(obuf[:dg.size])
                cn_events += 1
                
                # Save L1Accept in case we do batching
                if pydg.service() == TransitionId.L1Accept:
                    buf_f.write(obuf[:dg.size])
                    cn_L1_events += 1

    # end while ...

    # Move file ptr to the first L1
    os.lseek(fd, first_L1_offset, os.SEEK_SET)
    
        
os.close(fd)
out_f.close()


