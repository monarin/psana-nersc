from psana.dgram import Dgram

def run_test(mybytes, nfiles, max_events, flag_verbose):
    offsets = [0] * nfiles
    configs = [None] * nfiles 
    cdef int i, i_evt
    print(f'profdgram cython')
    for i_evt in range(max_events):
        dgrams = [None] * nfiles
        for i in range(nfiles):
            if i_evt == 0:
                configs[i] = Dgram(view=mybytes[i], offset=offsets[i])
                offsets[i] += configs[i]._size
            else:
                dgrams[i] = Dgram(config=configs[i], view=mybytes[i], offset=offsets[i])
                offsets[i] += dgrams[i]._size
