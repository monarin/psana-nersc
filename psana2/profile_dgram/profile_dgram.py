from psana.dgram import Dgram
import os
import cProfile
import time
from profdgram import run_test as run_test_pyx


def get_mybytes(xtc_dir, nfiles, read_size):
    mybytes = []
    for i in range(nfiles):
        fd = os.open(os.path.join(xtc_dir, f'data-r0001-s{str(i).zfill(2)}.xtc2'), os.O_RDONLY)
        mybytes.append(os.read(fd, read_size))
        os.close(fd)
    return mybytes


def run_test(mybytes, nfiles, max_events, flag_verbose):
    offsets = [0] * nfiles
    configs = [None] * nfiles 
    for i_evt in range(max_events):
        dgrams = [None] * nfiles
        for i in range(nfiles):
            if i_evt == 0:
                configs[i] = Dgram(view=mybytes[i], offset=offsets[i])
                if i == 0 and flag_verbose:
                    print(f'i_evt:{i_evt} config[{i}]={configs[i].timestamp()} service={configs[i].service()}')
                offsets[i] += configs[i]._size
            else:
                dgrams[i] = Dgram(config=configs[i], view=mybytes[i], offset=offsets[i])
                if i == 0 and flag_verbose:
                    print(f'i_evt:{i_evt} dgrams[{i}]={dgrams[i].timestamp()} service={dgrams[i].service()}')
                offsets[i] += dgrams[i]._size

if __name__ == "__main__":
    max_events = 1000
    nfiles = 32
    xtc_dir = '/cds/data/drpsrcf/users/monarin/xtcdata/10M32n'
    read_size = 256000000
    flag_prof = False
    flag_verbose = False
    
    mybytes = get_mybytes(xtc_dir, nfiles, read_size)
    
    if flag_prof:
        pr = cProfile.Profile()
        pr.enable()

    st = time.monotonic()
    #run_test(mybytes, nfiles, max_events, flag_verbose)
    run_test_pyx(mybytes, nfiles, max_events, flag_verbose)
    en = time.monotonic()

    if flag_prof:
        # Disable cProfile
        pr.disable()

        # Dump results
        # - for binary dump
        pr.dump_stats('cpu.prof')
        # - for text dump
        with open('cpu.txt', 'w') as output_file:
            sys.stdout = output_file
            pr.print_stats(sort='time')
            sys.stdout = sys.__stdout__


    print(f'Total Elapsed: {en-st:.2f}s. #files:{nfiles} #events:{max_events} rate:{(max_events/(en-st))*1e-3:.2f}kHz')
