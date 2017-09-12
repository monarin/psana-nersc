#!/bin/bash
START_XTC=$(date +"%s")
EXP=${1}
RUN=${2}
TRIAL=${3}
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

#cctbx
source /build/setpaths.sh

# base directory
BASE_DIR=${PSDIR}/d/psdm/cxi/${EXP}/scratch
OUT_DIR=/tmp

# experiment parameters
RUN_F="$(printf "r%04d" ${RUN})"
TRIAL_F="$(printf "%03d" ${TRIAL})"

# setup playground
mkdir -p ${OUT_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/$$/out
mkdir -p ${OUT_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/$$/stdout
mkdir -p ${OUT_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/$$/tmp

ls ${BASE_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}
if [ $? -gt 0 ]; then
  mkdir -p ${BASE_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/out
  mkdir -p ${BASE_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/stdout
fi

#run index
cctbx.xfel.xtc_process input.experiment=${EXP} input.run_num=${RUN} output.logging_dir=${OUT_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/$$/stdout output.output_dir=${OUT_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/$$/out format.cbf.invalid_pixel_mask=${BASE_DIR}/calib/mask_ld91.pickle input.reference_geometry=${BASE_DIR}/discovery/geom_ld91.json ${BASE_DIR}/discovery/process_batch.phil dump_indexed=False output.tmp_output_dir=${OUT_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/$$/tmp

cp -rf ${OUT_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/$$/out/* ${BASE_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/out/
cp -rf ${OUT_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/$$/stdout/* ${BASE_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/stdout/

END_XTC=$(date +"%s")
ELAPSED=$((END_XTC-START_XTC))
echo TotalElapsed_OneCore ${ELAPSED} ${START_XTC} ${END_XTC}

