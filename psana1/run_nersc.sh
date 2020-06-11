#!/bin/bash


# activate psana environment
source /img/conda.local/env.sh
source activate psana_base


# set location for experiment db and calib dir
export SIT_DATA=$CONDA_PREFIX/data
export SIT_PSDM_DATA=/global/cscratch1/sd/psdatmgr/data/psdm
export HDF5_USE_FILE_LOCKING=FALSE

# Choose script to run here:
python mpiDatasource.py      # xpptut15
#python mpiDatasourceCspad.py # cxic0515
