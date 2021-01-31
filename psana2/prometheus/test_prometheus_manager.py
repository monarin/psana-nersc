from psana.psexp.prometheus_manager import PrometheusManager
from prometheus_client import Summary
import threading
import logging, os, time
logging.basicConfig(level=logging.DEBUG,
        format='(%(threadName)-10s) %(message)s',
        )
from mpi4py import MPI
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
import random

s = PrometheusManager.get_metric('psana_smd0_wait_disk')

class Tester(object):

    def __init__(self, prom_man):
        self.prom_man = prom_man
        logging.debug('starting prometheus client on rank %d'%rank)

        self.c = self.prom_man.get_metric('psana_smd0_read')

    @s.time()
    def receive(self):
        t = random.randrange(0,10)
        logging.debug('receive() sleep %d s'%(t))
        time.sleep(t)
    
    def run(self):
        cn = 0
        while True:
            self.c.labels('evts','None').inc(1)
            time.sleep(1)
            cn += 1
            logging.debug('cn=%d'%cn)

            self.receive()
            if cn == 100:
                break

        logging.debug('exit')

def test_tester(jobid):
    prom_man = PrometheusManager(jobid)
    e = threading.Event()
    t = threading.Thread(name='PrometheusThread%s'%(rank),
            target=prom_man.push_metrics,
            args=(e, rank),
            daemon=True)
    t.start()
    
    tester = Tester(prom_man)
    tester.run()

    e.set()
    t.join()

if __name__ == "__main__":
    if rank == 0:
        jobid = os.getpid()
    else:
        jobid = None
    jobid = comm.bcast(jobid, root=0)
    test_tester(jobid)
    #test_tester(jobid)
