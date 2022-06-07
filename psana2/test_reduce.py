"""
This example demonstrates uneven calls of MPI.Reduce
that result in hanging.

1. test_standard()
This creates a situation where one rank does not receive
data and therefore does not call Reduce.
Pass: mpirun -n 4 python test_reduce.py
Hang: mpirun -n 5 python test_reduce.py

2. test_psana2_hang()
This creates a situation when bd cores call Reduce at
every three events. This will HANG when running with
mpirun -n 4 python test_reduce.py
Hang explained:
bd0 got i=0, ts=40          --> call Reduce ¬ MATCHED
bd1 got i=0, ts=70          --> call Reduce |
total = 3 {first hsd data of bd1 is [[3,3],[3,3]]}
bd0 got i=3, ts=50,60,130   --> call Reduce
bd1 got i=2, ts=80,170      --> hang (blocked by bd0)

3. test_psana2_pass()

"""

import numpy as np
from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
import os, sys
from psana import DataSource


def test_standard():
    #Prepare data to be sent
    N_rows = 3
    N_elems = 5
    data = np.ones([N_rows,N_elems])
    for i in range(N_rows):
        data[i][:] = i + 1

    #Create send and recv model
    if rank == 0:
        my_data = np.zeros(N_elems)
        for d in data:
            rankreq = comm.recv(source=MPI.ANY_SOURCE)
            comm.send(d, dest=rankreq)

        for i in range(size-1):
            rankreq = comm.recv(source=MPI.ANY_SOURCE)
            comm.send(np.zeros(N_elems), dest=rankreq)
    else:
        my_data = np.ones(N_elems)*-1
        while True:
            comm.send(rank, dest=0)
            recv_data = comm.recv(source=0)
            if recv_data[0] == 0:
                break
            my_data = recv_data

    # Check data from each rank
    print(f'rank:{rank} my_data: {my_data}', flush=True)

    # Prepare and call reduce
    if rank==0:
        totals = np.zeros_like(my_data)
    else:
        totals = None

    if my_data[0] >= 0:
        comm.Reduce(
            [my_data, MPI.DOUBLE],
            [totals, MPI.DOUBLE],
            op = MPI.SUM,
            root = 0
        )

    if rank == 0:
        print(f"rank:{rank} totals: {totals}", flush=True)

def get_ds():
    #Set Smd0's chunksize and EventBuilder's batch_size
    batch_size = 5

    #Path to psana2 test data folder
    home = os.environ['HOME']
    xtc_dir = home + '/lcls2/psana/psana/tests/test_data/fakesteps'

    #Create a datasource and loop through events
    ds = DataSource(exp='xpptut15', run=1, dir=xtc_dir, batch_size=batch_size)
    return ds

def test_psana2_hang():
    ds = get_ds()
    run = next(ds.runs())
    hsd = run.Detector('hsd')

    #For summing over hsd data that each rank receives
    hsd_sum = np.zeros([2,2])

    #Get bd-only comm for Reduce among bd cores
    bd_comm = ds.comms.bd_only_comm()
    for i, evt in enumerate(run.events()):
        hsd_calib = hsd.raw.calib(evt)
        hsd_sum += hsd_calib

        bd_rank = bd_comm.Get_rank()
        bd_size = bd_comm.Get_size()
        print(f'bdrank:{bd_rank} i:{i} evt:{evt.timestamp} hsd[0]:{hsd_calib[0][0]} sum:{hsd_sum[0][0]}', flush=True)

        #Prepare for Reduce *** This will hang when one core is waiting for
        #for other cores to call Reduce ***
        if i % 3 == 0:
            if bd_rank==0:
                totals = np.zeros_like(hsd_sum)
            else:
                totals = None

            print(f'  bdrank:{bd_rank} calling Reduce')
            bd_comm.Reduce(
                [hsd_sum, MPI.DOUBLE],
                [totals, MPI.DOUBLE],
                op = MPI.SUM,
                root = 0
            )

            if bd_rank == 0:
                print(f"  bdrank:{bd_rank} totals: {totals[0][0]}", flush=True)

def test_psana2_pass():
    # The original data has two steps so this example works w/o setting 
    # these options below. However, they are there just to demonstrate 
    # that we can call Reduce at every marked N events. This done by psana2
    # by inserting a fake step at every PS_SMD_N_EVENTS.
    os.environ['PS_SMD_N_EVENTS'] = '4'
    os.environ['PS_FAKESTEP_FLAG'] = '1'
    
    # Create a datasource to the test data folder
    ds = get_ds()
    run = next(ds.runs())
    hsd = run.Detector('hsd')

    #For summing over hsd data that each rank receives
    hsd_sum = np.zeros([2,2])
    
    #Get bd-only comm for Reduce among bd cores
    bd_comm = ds.comms.bd_only_comm()
    
    for i_step, step in enumerate(run.steps()):
        bd_rank = bd_comm.Get_rank()
        bd_size = bd_comm.Get_size()
        hsd_calib = np.zeros([2,2])
        cn_events = 0
        for i_evt, evt in enumerate(step.events()):
            hsd_calib = hsd.raw.calib(evt)
            hsd_sum += hsd_calib
            cn_events += 1

        print(f'bdrank:{bd_rank} step:{i_step} #events:{cn_events} hsd[0]:{hsd_calib[0][0]} sum:{hsd_sum[0][0]}', flush=True)
        
        # This ensures an even no. of Reduce call among all bd cores
        # since all steps are broadcasted to them so even though
        # there are no events in the one of the steps - this is still
        # going to get called.
        if bd_rank==0:
            totals = np.zeros_like(hsd_sum)
        else:
            totals = None

        print(f'  bdrank:{bd_rank} step:{i_step} calling Reduce', flush=True)
        bd_comm.Reduce(
            [hsd_sum, MPI.DOUBLE],
            [totals, MPI.DOUBLE],
            op = MPI.SUM,
            root = 0
        )

        if bd_rank == 0:
            print(f"  bdrank:{bd_rank} step:{i_step} totals: {totals[0][0]}", flush=True)





if __name__ == "__main__":
    test_option = 1
    if len(sys.argv) > 1:
        test_option = int(sys.argv[1])

    if test_option == 1:
        test_standard()
    elif test_option == 2:
        test_psana2_hang()
    elif test_option == 3:
        test_psana2_pass()
    else:
        print(f"Test option {test_option} not supported")
