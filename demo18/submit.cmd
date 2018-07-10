#!/bin/bash
#BSUB -J cctbx      # job name
#BSUB -W 00:10                # wall-clock time (hrs:mins)
#BSUB -n 8                   # number of tasks in job
#BSUB -q psdebugq              # queue
#BSUB -e cctbx_error.%J.log     # error file name in which %J is replaced by the job ID
#BSUB -o cctbx_output.%J.log     # output file name in which %J is replaced by the job ID


export IN_DIR=$PWD/input
export LIMIT=10
export OUT_DIR=$PWD/output
export DATA_DIR=/reg/d/psdm/xpp/xpptut15/scratch/mona/cxid9114
export PS_CALIB_DIR=$IN_DIR

source ~/lcls2/setup_env_python2.sh
conda activate ps2cctbx
source /reg/neh/home/monarin/.conda/envs/ps2cctbx/cctbx/build/setpaths.sh

mkdir -p $OUT_DIR/discovery/dials/r0108/000/out
mkdir -p $OUT_DIR/discovery/dials/r0108/000/stdout
mkdir -p $OUT_DIR/discovery/dials/r0108/000/tmp

mpirun cctbx.xfel.xtc_process \
   input.experiment=cxid9114 \
   input.run_num=108 \
   output.logging_dir=$OUT_DIR/discovery/dials/r0108/000/stdout \
   output.output_dir=$OUT_DIR/discovery/dials/r0108/000/out \
   format.cbf.invalid_pixel_mask=$IN_DIR/mask_ld91.pickle \
   $IN_DIR/process_batch.phil \
   dump_indexed=False \
   output.tmp_output_dir=$OUT_DIR/discovery/dials/r0108/000/tmp \
   input.reference_geometry=$IN_DIR/geom_ld91.json \
   input.xtc_dir=$DATA_DIR \
   max_events=$LIMIT
