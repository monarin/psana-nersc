#!/bin/bash
START_XTC=$(date +"%s")
EXP=${1}
TRIAL=${2}
RUN_ST=${3}
RUN_EN=${4}
FS=${5}
BBNAME=${6}

if [ ${1} == "" ]; then
echo "Usage: ./untar.sh EXP TRIAL_NO RUN_ST RUN_EN FS(Lustre/BB/GPFS) BurstBufferName CMDMODE(none/pythonprof/strace/debug)"
else

if [ ${FS} == "BB" ]; then
  PSREF=`echo DW_PERSISTENT_STRIPED_$BBNAME`
  PSDIR="${!PSREF}"
  WKDIR=${PSDIR}
elif [ ${FS} == "GPFS" ]; then
  PSDIR=/global/project/projectdirs/lcls
  WKDIR=$SCRATCH
else
  PSDIR=$SCRATCH
  WKDIR=$SCRATCH
fi

TRIAL_F="$(printf "%03d" ${TRIAL})"

echo "" > ${PSDIR}/d/psdm/cxi/${EXP}/scratch/discovery/dials/pickle.lst

for RUN in `seq $RUN_ST $RUN_EN`; do
  RUN_F="$(printf "r%04d" ${RUN})"
  DATA_OUT=${PSDIR}/d/psdm/cxi/${EXP}/scratch/discovery/dials/${RUN_F}/${TRIAL_F}/pickle/
  mkdir -p $DATA_OUT
  for f in ${PSDIR}/d/psdm/cxi/${EXP}/scratch/discovery/dials/${RUN_F}/${TRIAL_F}/out/*.tar; do 
    tar xf $f -C $DATA_OUT
  done
  ls ${PSDIR}/d/psdm/cxi/${EXP}/scratch/discovery/dials/${RUN_F}/${TRIAL_F}/pickle/*.pickle >> ${PSDIR}/d/psdm/cxi/${EXP}/scratch/discovery/dials/pickle.lst
  done

END_XTC=$(date +"%s")
ELAPSED=$((END_XTC-START_XTC))
echo TotalElapsed ${ELAPSED} ${START_XTC} ${END_XTC}

fi
