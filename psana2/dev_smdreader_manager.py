
import os, glob
from psana.psexp.smdreader_manager import SmdReaderManager

class Container(object):
    pass

class Run(object):
    def __init__(self):
        filenames = glob.glob('/reg/neh/home/monarin/lcls2/psana/psana/tests/.tmp_smd0/.tmp/smalldata/*.xtc2')
        fds = [os.open(f, os.O_RDONLY) for f in filenames]
        self.smd_dm = Container()
        setattr(self.smd_dm, 'fds', fds)
        self.max_events = 1000

if __name__ == "__main__":
    run = Run()
    os.environ['PS_SMD_N_EVENTS'] = "1"
    smdr_man = SmdReaderManager(run)
    for chunk in smdr_man.chunks():
        smd_chunk, step_chunk = chunk
        print(f'{memoryview(smd_chunk).nbytes} {memoryview(step_chunk).nbytes}')

