#!/bin/bash
START_XTC=$(date +"%s")
EXP=${1}
RUN=${2}
TRIAL=${3}
CMDMODE=${4}

if [ ${1} == "" ]; then
echo "Usage: ./index_single.sh EXP RUN_NO TRIAL_NO CMDMODE(none/pythonprof/strace/debug)"
else
echo $EXP $RUN $TRIAL $CMDMODE

#cctbx
source /build/setpaths.sh

# base directory is the current directory
OUT_DIR=${PWD}/output
IN_DIR=${PWD}/input
DATA_DIR=/global/cscratch1/sd/psdatmgr/data/psdm/cxi/cxid9114/demo/test_xtc
export SIT_DATA=${IN_DIR}/expdb
export SIT_PSDM_DATA=${SCRATCH}/d/psdm

# experiment parameters
RUN_F="$(printf "r%04d" ${RUN})"
TRIAL_F="$(printf "%03d" ${TRIAL})"

# setup playground
mkdir -p ${OUT_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/out
mkdir -p ${OUT_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/stdout
mkdir -p ${OUT_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/tmp

if [ "${CMDMODE}" = "pythonprof" ]; then
    python -m cProfile -s tottime xtc_process.py input.experiment=${EXP} input.run_num=${RUN} output.logging_dir=${OUT_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/stdout output.output_dir=${OUT_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/out format.cbf.invalid_pixel_mask=${IN_DIR}/mask_ld91.pickle input.reference_geometry=${IN_DIR}/geom_ld91.json ${IN_DIR}/process_batch.phil dump_indexed=False output.tmp_output_dir=${OUT_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/tmp input.xtc_dir=${DATA_DIR}
  
elif [ "${CMDMODE}" = "strace" ]; then
    strace -ttt -f -o $$.log cctbx.xfel.xtc_process input.experiment=${EXP} input.run_num=${RUN} output.logging_dir=${OUT_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/stdout output.output_dir=${OUT_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/out format.cbf.invalid_pixel_mask=${IN_DIR}/mask_ld91.pickle input.reference_geometry=${IN_DIR}/geom_ld91.json ${IN_DIR}/process_batch.phil dump_indexed=False output.tmp_output_dir=${OUT_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/tmp input.xtc_dir=${DATA_DIR}

elif [ "${CMDMODE}" = "debug" ]; then
    python xtc_process.py input.experiment=${EXP} input.run_num=${RUN} output.logging_dir=${OUT_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/stdout output.output_dir=${OUT_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/out format.cbf.invalid_pixel_mask=${IN_DIR}/mask_ld91.pickle input.reference_geometry=${IN_DIR}/geom_ld91.json ${IN_DIR}/process_batch.phil dump_indexed=False output.tmp_output_dir=${OUT_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/tmp input.xtc_dir=${DATA_DIR}
  
else
    cctbx.xfel.xtc_process input.experiment=${EXP} input.run_num=${RUN} output.logging_dir=${OUT_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/stdout output.output_dir=${OUT_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/out format.cbf.invalid_pixel_mask=${IN_DIR}/mask_ld91.pickle input.reference_geometry=${IN_DIR}/geom_ld91.json ${IN_DIR}/process_batch.phil dump_indexed=False output.tmp_output_dir=${OUT_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/tmp input.xtc_dir=${DATA_DIR}
  
fi


END_XTC=$(date +"%s")
ELAPSED=$((END_XTC-START_XTC))
echo TotalElapsed ${ELAPSED} ${START_XTC} ${END_XTC}
fi
