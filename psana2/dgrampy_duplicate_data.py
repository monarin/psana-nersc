import dgrampy as dp
import os
from psana.psexp import TransitionId

filename = '/cds/home/m/monarin/tmp/tmp/tmolv9418-r0175-s000-c000.xtc2'
n_events = 35389
n_dups = 1000 
cn_ts= 0

with open('tmolv9418-r0175-s000-c000.xtc2', 'wb') as f:
    for i_dup in range(n_dups):
        fd = os.open(filename, os.O_RDONLY)
        pyiter = dp.PyXtcFileIterator(fd, 0x1000000)
        i = 0
        while i < n_events:
            pydg = pyiter.next()
            
            # Update ts
            dp.updatetimestamp(pydg, 2, cn_ts)
            
            # Copy dgram header and data
            dp.copy_dgram(pydg)
            dp.iterate(pydg)
            buf = dp.get_buf()
            
            if i < 4:
                if i_dup == 0:
                    # write out Configure, BeginRun, BeginStep, Enable for first loop
                    f.write(buf)
                    cn_ts += 1
            elif i < 35386:
                # all L1
                f.write(buf)
                cn_ts += 1
            else:
                if i_dup == n_dups - 1:
                    # write out Disable, EndStep, EndRun for last loop
                    f.write(buf)
                    cn_ts +=1
            dp.clearbuf()
            i += 1

        os.close(fd)



