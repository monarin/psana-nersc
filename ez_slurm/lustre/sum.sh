#!/bin/bash
START_XTC=$(date +"%s")

#for experiment database
export SIT_DATA=/reg/g/psdm/data

#for psana
export SIT_PSDM_DATA=/reg/d/psdm

#cctbx
source /build/setpaths.sh

# experiment parameters
EXP=${1}
RUN=${2}

python /global/cscratch1/sd/monarin/d/psdm/cxi/cxid9114/scratch/mona/psana-nersc/ez_slurm/auto/client_server.py ${EXP} ${RUN}

END_XTC=$(date +"%s")
ELAPSED=$((END_XTC-START_XTC))
echo TotalElapsed_OneCore ${ELAPSED} ${START_XTC} ${END_XTC}

