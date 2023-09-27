#!/usr/bin/env python

from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
myhost = MPI.Get_processor_name()

import os
path = '/sdf/data/lcls/drpsrcf/ffb/tmo/tmoc00221/xtc/smalldata/tmoc00221-r0028-s000-c000.smd.xtc2'

print(f'RANK{rank}x size:{size} {myhost} {os.path.isfile(path)}')

#from psana import DataSource


