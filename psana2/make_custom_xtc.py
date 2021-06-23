from psana.dgram import Dgram
import os
import time
import shutil
import sys

buffering = 0

def open_file(fname):
    fd = os.open(fname, os.O_RDONLY)
    f_size = os.path.getsize(fname)
    return fd, f_size

def get_config(fd_in):
    config = Dgram(file_descriptor=fd_in)
    offset = memoryview(config).nbytes
    return offset, config

def write_dgram(config, f_out, offset, skip=False):
    d = Dgram(config=config)
    offset += memoryview(d).nbytes
    if not skip:
        f_out.write(d)
        print(f'write dgram {memoryview(d).nbytes} bytes')
    return offset

    
if __name__ == "__main__":

    xtc_fname_in = "data-r0001-s01.xtc2"
    xtc_fd, xtc_f_size = open_file(xtc_fname_in)
    xtc_f_out = open(f"data-r0001-s01-c01.xtc2" ,"wb", buffering=buffering)

    xtc_offset, xtc_config = get_config(xtc_fd)
    #xtc_f_out.write(xtc_config) #first chunk only

    cn_events = 2
    #selected_events = list(range(2, 15+1)) # first chunk
    selected_events = list(range(16, 23+1)) # second chunk
    while xtc_offset < xtc_f_size:
        # write dgram only if event_id is in the selected events
        print(f"cn_events={cn_events}")
        if cn_events in selected_events:
            skip = False
        else:
            skip = True
        xtc_offset = write_dgram(xtc_config, xtc_f_out, xtc_offset, skip=skip)

        cn_events += 1

    xtc_f_out.close()
    os.close(xtc_fd)

