#!/bin/bash
START_XTC=$(date +"%s")

BB_DIR=$DW_PERSISTENT_STRIPED_monarinbb

#for experiment database
export SIT_DATA=${BB_DIR}/g/psdm/data

#for psana
export SIT_PSDM_DATA=${BB_DIR}/d/psdm

#cctbx
#source /build/setpaths.sh

# experiment parameters
EXP=${1}
RUN_ST=${2}
RUN_EN=${3}

# base directory
BASE_DIR=${BB_DIR}/d/psdm/cxi/${EXP}/scratch/

python /global/cscratch1/sd/monarin/d/psdm/cxi/cxid9114/scratch/mona/psana-nersc/ez_slurm/burstbuffer/simpler_psana.py ${EXP} ${RUN_ST} ${RUN_EN}

END_XTC=$(date +"%s")
ELAPSED=$((END_XTC-START_XTC))
echo TotalElapsed_OneCore ${ELAPSED} ${START_XTC} ${END_XTC}

