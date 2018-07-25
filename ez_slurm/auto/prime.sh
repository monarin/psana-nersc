#!/bin/bash

#cctbx
source /build/setpaths.sh

prime.mpi_run prime.phil n_postref_cycle=0 data=int.lst

