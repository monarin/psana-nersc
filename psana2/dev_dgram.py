from psana import dgram
import os, glob, time, sys
import numpy as np

CHUNKSIZE = 0x4000000
BIGDGRAM_SIZE = 366
read_chunk = 0
if len(sys.argv) > 1:
    read_chunk = int(sys.argv[1])

n_files = 16
max_events = 1000
fds = [os.open(xtc_file, os.O_RDONLY) for xtc_file in glob.glob('/reg/d/psdm/xpp/xpptut15/scratch/mona/xtc2/*.xtc2')[:n_files]]
#fds = [os.open(xtc_file, os.O_RDONLY) for xtc_file in glob.glob('/reg/neh/home/monarin/lcls2/.tmp/smalldata/*.xtc2')[:n_files]]
configs = [dgram.Dgram(file_descriptor=fd) for fd in fds]

if read_chunk:
    print('read_chunk')
    views = [None]*n_files
    for i in range(n_files):
        views[i] = os.read(fds[i], CHUNKSIZE)

    st = time.time()
    cn_events = 0
    offsets = np.zeros(n_files, dtype='i')
    for i in range(max_events):
        dgrams = [dgram.Dgram(view=view, config=config, offset=offset) for view, config, offset in zip(views, configs, offsets)]
        cn_events += 1
        offsets += BIGDGRAM_SIZE

    en = time.time()

else:
    st = time.time()
    cn_events = 0
    for i in range(max_events):
        dgrams = [dgram.Dgram(config=config) for config in configs]
        cn_events += 1


    en = time.time()

for fd in fds:
    os.close(fd)
print('#Evt: %d Total Elapsed(s): %6.3f Rate(kHz): %6.3f'%(cn_events, (en-st), cn_events/((en-st)*1000)))

