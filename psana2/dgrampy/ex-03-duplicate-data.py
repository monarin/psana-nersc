from psana.dgrampy import DgramPy, PyXtcFileIterator
import os
from psana.psexp import TransitionId

# Input file, no. of events (needed to determine #L1),
# and duplication factor (n_dups).
ifname = '/cds/home/m/monarin/xtc1to2/examples/data/amo06516-r0090-s000-c000.xtc2'
n_events = 127
n_dups = 2500 
cn_ts= 0

def next_ts():
    global cn_ts
    current_ts = cn_ts
    cn_ts +=1
    return current_ts
    
# Output file
ofname = '/cds/data/drpsrcf/users/monarin/amo06516/amo06516-r0090-s000-c000.xtc2'
out_f = open(ofname, 'wb')
print(f'write to {ofname}')

fd = os.open(ifname, os.O_RDONLY)
for i_dup in range(n_dups):
    print(f'i_dup:{i_dup}')
    pyiter = PyXtcFileIterator(fd, 0x10000000)
    i = 0
    while i < n_events:
        pydg = pyiter.next()
        
        if i == 0:
            if i_dup == 0:
                config = DgramPy(pydg)
                config.updatetimestamp(next_ts())
                config.save(out_f)
        else:
            flag_write = False
            if i < 4:
                # Write out Configure, BeginRun, BeginStep, Enable for first loop
                if i_dup == 0:
                    flag_write = True
            elif i < n_events - 3:
                # All L1
                flag_write = True
            else:
                # Disable, EndStep, EndRun
                if i_dup == n_dups - 1:
                    flag_write = True
            
            if flag_write:
                dg = DgramPy(pydg, config=config)
                dg.updatetimestamp(next_ts())
                dg.save(out_f)

        i += 1
    # end while i < ...
    os.lseek(fd, 0, os.SEEK_SET)
        
os.close(fd)
out_f.close()


