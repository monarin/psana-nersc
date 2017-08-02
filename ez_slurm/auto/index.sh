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
#source /build/setpaths.sh
source /global/homes/m/monarin/cctbx/build/setpaths.sh

# base directory
BASE_DIR=${PSDIR}/d/psdm/cxi/${EXP}/scratch

# experiment parameters
RUN_F="$(printf "r%04d" ${RUN})"
TRIAL_F="$(printf "%03d" ${TRIAL})"

# setup playground
mkdir -p ${BASE_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/out
mkdir -p ${BASE_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/stdout

#run index
#python -m cProfile -s tottime /modules/cctbx_project/xfel/command_line/xtc_process.py input.experiment=${EXP} input.run_num=${RUN} output.logging_dir=${BASE_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/stdout output.output_dir=${BASE_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/out ${BASE_DIR}/discovery/target.phil

#strace -ttt -f -o $$.log cctbx.xfel.xtc_process input.experiment=${EXP} input.run_num=${RUN} output.logging_dir=${BASE_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/stdout output.output_dir=${BASE_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/out ${BASE_DIR}/discovery/target.phil

cctbx.xfel.xtc_process input.experiment=${EXP} input.run_num=${RUN} output.logging_dir=${BASE_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/stdout output.output_dir=${BASE_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/out format.cbf.invalid_pixel_mask=${BASE_DIR}/calib/mask.pickle dispatch.max_events=1 ${BASE_DIR}/discovery/target.phil

END_XTC=$(date +"%s")
ELAPSED=$((END_XTC-START_XTC))
echo TotalElapsed_OneCore ${ELAPSED} ${START_XTC} ${END_XTC}

