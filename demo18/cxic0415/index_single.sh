#!/bin/bash
START_XTC=$(date +"%s")
EXP=${1}
RUN=${2}
TRIAL=${3}
CMDMODE=${4}
LIMIT=${5}
OUT_DIR=${6}
RUN_F="$(printf "r%04d" ${RUN})"
TRIAL_F="$(printf "%03d" ${TRIAL})"


if [ $# -eq 0 ]; then
    echo "Usage: ./index_single.sh EXP RUN_NO TRIAL_NO CMDMODE(none/pythonprof/strace/debug) MAX_EVTS OUT_DIR"
    exit 0
fi

echo $EXP $RUN $TRIAL $CMDMODE $LIMIT $OUT_DIR

# mask and metrology files are from the current dir
IN_DIR=${PWD}/input
DATA_DIR=/global/cscratch1/sd/monarin/d/psdm/cxi/${EXP}/xtc2

export PS_CALIB_DIR=$IN_DIR
export PS_SMD_N_EVENTS=1000
export PS_SMD_NODES=32

# setup playground
if [ "${CMDMODE}" != "/tmp" ]; then
    mkdir -p ${OUT_DIR}
fi

cctbx_args="input.experiment=${EXP} input.run_num=${RUN} output.logging_dir=${OUT_DIR} output.output_dir=${OUT_DIR} format.cbf.invalid_pixel_mask=${IN_DIR}/mask.pickle /tmp/process_batch.phil dump_indexed=False output.tmp_output_dir=${OUT_DIR} input.xtc_dir=${DATA_DIR}"

if [ "$LIMIT" -ne 0 ]; then
    cctbx_args="$cctbx_args max_events=${LIMIT}"
fi

if [ "${CMDMODE}" = "pythonprof" ]; then
    python -m cProfile -s tottime python /tmp/xtc_process.py ${cctbx_args}
  
elif [ "${CMDMODE}" = "strace" ]; then
    strace -ttt -f -o $$.log python /tmp/xtc_process.py ${cctbx_args}

elif [ "${CMDMODE}" = "debug" ]; then
    python /tmp/xtc_process.py ${cctbx_args}
  
else
    cctbx.xfel.xtc_process ${cctbx_args}
  
fi


END_XTC=$(date +"%s")
ELAPSED=$((END_XTC-START_XTC))
echo TotalElapsed ${ELAPSED} ${START_XTC} ${END_XTC}
