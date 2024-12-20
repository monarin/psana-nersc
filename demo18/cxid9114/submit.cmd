#!/bin/bash
#BSUB -J cctbx      # job name
#BSUB -n 12                   # number of tasks in job
#BSUB -q psdebugq              # queue
#BSUB -e cctbx_error.%J.log     # error file name in which %J is replaced by the job ID
#BSUB -o cctbx_output.%J.log     # output file name in which %J is replaced by the job ID

t_start=`date +%s`

# experiment parameters
EXP="cxid9114"
RUN=96
TRIAL=0
RUN_F="$(printf "r%04d" ${RUN})"
TRIAL_F="$(printf "%03d" ${TRIAL})"

export IN_DIR=$PWD/input
export LIMIT=10
export OUT_DIR=$PWD/output
export DATA_DIR=/reg/d/psdm/xpp/xpptut15/scratch/mona/cxid9114
export PS_CALIB_DIR=$IN_DIR

source ~/tmp/lcls2_py2/setup_env.sh -py2
conda activate ps2cctbx
source /reg/neh/home/monarin/.conda/envs/ps2cctbx/cctbx/build/setpaths.sh

# setup playground
mkdir -p ${OUT_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/out
mkdir -p ${OUT_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/stdout
mkdir -p ${OUT_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/tmp

mpirun cctbx.xfel.xtc_process \
   input.experiment=${EXP} \
   input.run_num=${RUN} \
   output.logging_dir=${OUT_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/stdout \
   output.output_dir=${OUT_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/out \
   format.cbf.invalid_pixel_mask=$IN_DIR/mask_ld91.pickle \
   $IN_DIR/process_batch.phil \
   dump_indexed=False \
   output.tmp_output_dir=${OUT_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/tmp \
   input.reference_geometry=${IN_DIR}/geom_ld91.json \
   input.xtc_dir=$DATA_DIR \
   max_events=$LIMIT

t_end=`date +%s`

echo TotalElapsed $((t_end-t_start)) $t_start $t_end
