#!/bin/bash
START_XTC=$(date +"%s")
EXP=${1}
RUN=${2}
TRIAL=${3}
CMDMODE=${4}
LIMIT=${5}
RUN_F="$(printf "r%04d" ${RUN})"
TRIAL_F="$(printf "%03d" ${TRIAL})"


if [ $# -eq 0 ]; then
    echo "Usage: ./index_lite.sh EXP RUN_NO TRIAL_NO CMDMODE(none/pythonprof/strace/debug)"
    exit 0
fi

echo $EXP $RUN $TRIAL $CMDMODE $LIMIT

# base directory is the current directory
IN_DIR=${PWD}/input
OUT_DIR=/tmp
DATA_DIR=/global/cscratch1/sd/monarin/d/psdm/cxi/${EXP}/xtc2

export PS_CALIB_DIR=$IN_DIR
export PS_SMD_N_EVENTS=1000
export PS_SMD_NODES=32

cctbx_args="input.experiment=${EXP} input.run_num=${RUN} output.output_dir=${OUT_DIR} output.logging_dir=${OUT_DIR} output.tmp_output_dir=${OUT_DIR} format.cbf.invalid_pixel_mask=${IN_DIR}/mask_ld91.pickle input.reference_geometry=/tmp/geom_ld91.json /tmp/process_batch.phil dump_indexed=False input.xtc_dir=${DATA_DIR}"

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
