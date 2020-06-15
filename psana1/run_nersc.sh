#!/bin/bash


# activate psana environment
#source /img/conda.local/env.sh
#source activate psana_base


# set location for experiment db and calib dir
export SIT_DATA=$CONDA_PREFIX/data
export SIT_PSDM_DATA=/global/cscratch1/sd/psdatmgr/data/psdm


# prevent crash when running on one core
export HDF5_USE_FILE_LOCKING=FALSE


python mpiDatasource.py
