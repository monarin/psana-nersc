from psana import dgram
import os, glob, time

n_files = 1
max_events = 100
fds = [os.open(xtc_file, os.O_RDONLY) for xtc_file in glob.glob('/reg/d/psdm/xpp/xpptut15/scratch/mona/xtc2/*.xtc2')][:n_files]
configs = [dgram.Dgram(file_descriptor=fd) for fd in fds]
st = time.time()
for i in range(max_events):
    dgrams = [dgram.Dgram(config=config) for config in configs]

en = time.time()
print('Total Elapsed(s): %6.3f Rate(kHz): %6.3f'%((en-st), max_events/((en-st)*1000)))

