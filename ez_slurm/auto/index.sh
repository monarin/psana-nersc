#!/bin/bash
START_XTC=$(date +"%s")
EXP=${1}
RUN_ST=${2}
RUN_EN=${3}
TRIAL=${4}
FS=${5}
BBNAME=${6}
CMDMODE=${7}

if [ ${1} == "" ]; then
echo "Usage: ./index.sh EXP RUN_ST RUN_EN TRIAL_NO FS(Lustre/BB/GPFS) BurstBufferName CMDMODE(none/pythonprof/strace/debug)"
else

if [ ${FS} == "BB" ]; then
  PSREF=`echo DW_PERSISTENT_STRIPED_$BBNAME`
  PSDIR="${!PSREF}"
  WK_DIR=${PSDIR}
elif [ ${FS} == "GPFS" ]; then
  PSDIR=/global/project/projectdirs/lcls
  WK_DIR=$SCRATCH
else
  PSDIR=$SCRATCH
  WK_DIR=$SCRATCH
fi

#for experiment database
export SIT_DATA=${PSDIR}/g/psdm/data
#for psana
export SIT_PSDM_DATA=${PSDIR}/d/psdm
#cctbx
source /build/setpaths.sh

# base directory
BASE_DIR=${WK_DIR}/d/psdm/cxi/${EXP}/scratch

# looping through all the given runs
for RUN in `seq $RUN_ST $RUN_EN`; do
  START_RUN=$(date +"%s")

  # experiment parameters
  RUN_F="$(printf "r%04d" ${RUN})"
  TRIAL_F="$(printf "%03d" ${TRIAL})"

  # setup playground
  mkdir -p ${BASE_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/out
  mkdir -p ${BASE_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/stdout
  mkdir -p ${BASE_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/tmp

  if [ "${CMDMODE}" = "pythonprof" ]; then
    python -m cProfile -s tottime xtc_process.py input.experiment=${EXP} input.run_num=${RUN} output.logging_dir=${BASE_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/stdout output.output_dir=${BASE_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/out format.cbf.invalid_pixel_mask=${BASE_DIR}/calib/mask_ld91.pickle input.reference_geometry=${BASE_DIR}/discovery/geom_ld91.json ${BASE_DIR}/discovery/process_batch.phil dump_indexed=False output.tmp_output_dir=${BASE_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/tmp
  
  elif [ "${CMDMODE}" = "strace" ]; then
    strace -ttt -f -o $$.log cctbx.xfel.xtc_process input.experiment=${EXP} input.run_num=${RUN} output.logging_dir=${BASE_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/stdout output.output_dir=${BASE_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/out format.cbf.invalid_pixel_mask=${BASE_DIR}/calib/mask_ld91.pickle input.reference_geometry=${BASE_DIR}/discovery/geom_ld91.json ${BASE_DIR}/discovery/process_batch.phil dump_indexed=False output.tmp_output_dir=${BASE_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/tmp

  elif [ "${CMDMODE}" = "debug" ]; then
    python xtc_process.py input.experiment=${EXP} input.run_num=${RUN} output.logging_dir=${BASE_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/stdout output.output_dir=${BASE_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/out format.cbf.invalid_pixel_mask=${BASE_DIR}/calib/mask_ld91.pickle input.reference_geometry=${BASE_DIR}/discovery/geom_ld91.json ${BASE_DIR}/discovery/process_batch.phil dump_indexed=False output.tmp_output_dir=${BASE_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/tmp input.xtc_dir=/global/cscratch1/sd/psdatmgr/data/psdm/cxi/cxid9114/demo/xtc
  
  else
    cctbx.xfel.xtc_process input.experiment=${EXP} input.run_num=${RUN} output.logging_dir=${BASE_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/stdout output.output_dir=${BASE_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/out format.cbf.invalid_pixel_mask=${BASE_DIR}/calib/mask_ld91.pickle input.reference_geometry=${BASE_DIR}/discovery/geom_ld91.json ${BASE_DIR}/discovery/process_batch.phil dump_indexed=False output.tmp_output_dir=${BASE_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/tmp input.xtc_dir=/global/cscratch1/sd/psdatmgr/data/psdm/cxi/cxid9114/demo/test_xtc
  
  fi

  END_RUN=$(date +"%s")
  ELAPSED_RUN=$((END_RUN-START_RUN))
  echo TotalElapsed_One_Run ${ELAPSED_RUN} ${START_RUN} ${END_RUN}

done

END_XTC=$(date +"%s")
ELAPSED=$((END_XTC-START_XTC))
echo TotalElapsed_All_Runs ${ELAPSED} ${START_XTC} ${END_XTC}
fi
