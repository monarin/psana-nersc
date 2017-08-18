#!/bin/bash
START_XTC=$(date +"%s")
EXP=${1}
RUN_ST=${2}
RUN_EN=${3}
FS=${4}
BBNAME=${5}

if [ ${FS} == "BB" ]; then
  PSREF=`echo DW_PERSISTENT_STRIPED_$BBNAME`
  PSDIR="${!PSREF}"
else
  PSDIR=$SCRATCH
fi

#for experiment database
export SIT_DATA=${PSDIR}/g/psdm/data

#for psana
export SIT_PSDM_DATA=${PSDIR}/d/psdm

# base directory
BASE_DIR=${PSDIR}/d/psdm/cxi/${EXP}/scratch

python ${PWD}/worker.py ${EXP} ${RUN_ST} ${RUN_EN}

END_XTC=$(date +"%s")
ELAPSED=$((END_XTC-START_XTC))
echo TotalElapsed_OneCore ${ELAPSED} ${START_XTC} ${END_XTC}

