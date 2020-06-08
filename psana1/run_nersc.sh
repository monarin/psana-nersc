#!/bin/bash


# activate psana environment
source /img/conda.local/env.sh
source activate psana_base


# set location for experiment db and calib dir
export SIT_DATA=$CONDA_PREFIX/data
export SIT_PSDM_DATA=/global/cscratch1/sd/psdatmgr/data/psdm


python mpiDatasource.py
