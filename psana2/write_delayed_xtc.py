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

def write_config(fd_in, f_out):
    config = Dgram(file_descriptor=fd_in)
    offset = memoryview(config).nbytes
    f_out.write(config)
    print(f'write config {offset} bytes')
    return offset, config

def write_dgram(config, f_out, offset):
    d = Dgram(config=config)
    offset += memoryview(d).nbytes
    f_out.write(d)
    print(f'write dgram {memoryview(d).nbytes} bytes')
    return offset

    
if __name__ == "__main__":

    if len(sys.argv) == 1:
        max_events = 50
        start_cp_at = 50
    else:
        max_events = int(sys.argv[1])
        start_cp_at = int(sys.argv[2]) # start copying to .xtc2 file at event#

    smd_fname_in = "/cds/data/drpsrcf/users/monarin/xtcdata/10M60n/xtcdata/smalldata/data-r0001-s00.smd.xtc2"
    xtc_fname_in = "/cds/data/drpsrcf/users/monarin/xtcdata/10M60n/xtcdata/data-r0001-s00.xtc2"

    smd_fd, smd_f_size = open_file(smd_fname_in)
    xtc_fd, xtc_f_size = open_file(xtc_fname_in)

    smd_f_out = open("./tmp/smalldata/data-r0001-s00.smd.xtc2.inprogress", "wb", buffering=buffering)
    xtc_f_out = open("./tmp/data-r0001-s00.xtc2.inprogress" ,"wb", buffering=buffering)


    # write config for both smd and xtc files
    smd_offset, smd_config = write_config(smd_fd, smd_f_out)
    xtc_offset, xtc_config = write_config(xtc_fd, xtc_f_out)

    cn_events = 0
    while smd_offset < smd_f_size and xtc_offset < xtc_f_size and cn_events < max_events:
        # write dgram
        smd_offset = write_dgram(smd_config, smd_f_out, smd_offset)
        xtc_offset = write_dgram(xtc_config, xtc_f_out, xtc_offset)

        cn_events += 1
        print(f'Finished write evt#{cn_events} - sleep 1 second...')
        
        if cn_events == start_cp_at:
            shutil.copyfile("./tmp/smalldata/data-r0001-s00.smd.xtc2.inprogress", "./tmp/smalldata/data-r0001-s00.smd.xtc2")
            shutil.copyfile("./tmp/data-r0001-s00.xtc2.inprogress", "./tmp/data-r0001-s00.xtc2")
            print(f'copy .inprogress files to .xtc2 files')
            
        time.sleep(1)

    smd_f_out.close()
    xtc_f_out.close()
    os.close(smd_fd)
    os.close(xtc_fd)
