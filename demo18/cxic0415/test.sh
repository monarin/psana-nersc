EXP="cxic0415"
RUN=50
TRIAL=0
RUN_F="$(printf "r%04d" ${RUN})"
TRIAL_F="$(printf "%03d" ${TRIAL})"

LIMIT=1

IN_DIR=$PWD/input
OUT_DIR=$PWD/output
DATA_DIR=/reg/d/psdm/xpp/xpptut15/scratch/mona/cxic0415
export PS_CALIB_DIR=$IN_DIR

mkdir -p ${OUT_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/out
mkdir -p ${OUT_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/stdout
mkdir -p ${OUT_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/tmp

mpirun -n 3 cctbx.xfel.xtc_process \
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
