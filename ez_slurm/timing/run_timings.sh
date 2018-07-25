#!/bin/bash

export INSTALL_ROOT=/global/project/projectdirs/lcls/apps/logbk-batch-client
export PYTHONPATH=${INSTALL_ROOT}
export FW_CONFIG_FILE=${INSTALL_ROOT}/etc/nersc/cori/FW_config.yaml
export BATCH_MGR_URL="https://pswww-dev.slac.stanford.edu/batch_manager_nersc"

module load python/2.7-anaconda-4.4
source activate /global/project/projectdirs/lcls/conda/envs/workflow-1.0

python $INSTALL_ROOT/bin/nersc/cori/timings.py

