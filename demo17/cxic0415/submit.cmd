#!/bin/bash
#BSUB -J cctbx      # job name
#BSUB -W 00:10                # wall-clock time (hrs:mins)
#BSUB -n 8                   # number of tasks in job
#BSUB -q psdebugq              # queue
#BSUB -e cctbx_error.%J.log     # error file name in which %J is replaced by the job ID
#BSUB -o cctbx_output.%J.log     # output file name in which %J is replaced by the job ID

# experiment parameters
EXP="cxic0415"
RUN=101
TRIAL=0
RUN_F="$(printf "r%04d" ${RUN})"
TRIAL_F="$(printf "%03d" ${TRIAL})"

export IN_DIR=$PWD/input
export LIMIT=10
export OUT_DIR=$PWD/output
export DATA_DIR=/reg/d/psdm/cxi/${EXP}/xtc
export PS_CALIB_DIR=$IN_DIR

source /reg/neh/home/monarin/miniconda2/etc/profile.d/conda.sh
conda activate cctbx-dev
export SIT_DATA=/reg/g/psdm/data
source /reg/neh/home/monarin/cctbx/build/setpaths.sh

# setup playground
mkdir -p ${OUT_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/out
mkdir -p ${OUT_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/stdout
mkdir -p ${OUT_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/tmp

mpirun cctbx.xfel.xtc_process \
   input.experiment=${EXP} \
   input.run_num=${RUN} \
   output.logging_dir=${OUT_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/stdout \
   output.output_dir=${OUT_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/out \
   format.cbf.invalid_pixel_mask=$IN_DIR/mask.pickle \
   $IN_DIR/process_batch.phil \
   dump_indexed=False \
   output.tmp_output_dir=${OUT_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/tmp \
   input.xtc_dir=$DATA_DIR \
   max_events=$LIMIT
