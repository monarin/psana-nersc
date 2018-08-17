#!/bin/bash
START_XTC=$(date +"%s")
EXP=${1}
RUN=${2}
TRIAL=${3}
CMDMODE=${4}
RUN_F="$(printf "r%04d" ${RUN})"
TRIAL_F="$(printf "%03d" ${TRIAL})"


if [ $# -eq 0 ]; then
    echo "Usage: ./index_single.sh EXP RUN_NO TRIAL_NO CMDMODE(none/pythonprof/strace/debug)"
    exit 0
fi

echo $EXP $RUN $TRIAL $CMDMODE

# base directory is the current directory
IN_DIR=/tmp
LIMIT=2
OUT_DIR=/tmp/output
DATA_DIR=/global/cscratch1/sd/monarin/d/psdm/cxi/${EXP}/xtc2

# setup envs
export CONDA_EXE=/opt/conda/bin/conda                        
export CONDA_PREFIX=/opt/conda                               
export CONDA_PROMPT_MODIFIER=(base)                          
export CONDA_PYTHON_EXE=/opt/conda/bin/python                
export CONDA_SHLVL=1
export INFOPATH=/opt/rh/devtoolset-7/root/usr/share/info

export LD_LIBRARY_PATH=/opt/udiImage/modules/mpich/lib64:/opt/rh/devtoolset-7/root/usr/lib64:/opt/rh/devtoolset-7/root/usr/lib:/opt/rh/devtoolset-7/root/usr/lib64/dyninst:/opt/rh/devtoolset-7/root/usr/lib/dyninst:/opt/rh/devtoolset-7/root/usr/lib64:/opt/rh/devtoolset-7/root/usr/lib
export MANPATH=/opt/rh/devtoolset-7/root/usr/share/man:/usr/common/software/man:/usr/common/mss/man:/usr/common/nsg/man:/opt/cray/pe/mpt/7.7.0/gni/man/mpich:/opt/cray/pe/atp/2.1.1/man:/opt/cray/alps/6.5.28-6.0.5.0_18.6__g13a91b6.ari/man:/opt/cray/job/2.2.2-6.0.5.0_8.47__g3c644b5.ari/man:/opt/cray/pe/pmi/5.0.13/man:/opt/cray/pe/libsci/18.03.1/man:/opt/cray/pe/man/csmlversion:/opt/cray/pe/craype/2.5.14/man:/opt/intel/compilers_and_libraries_2018.1.163/linux/man/common:/usr/syscom/nsg/man:/opt/cray/pe/modules/3.2.10.6/share/man:/global/homes/c/canon/man:/usr/local/man:/usr/share/man:/opt/cray/share/man:/opt/cray/pe/man:/opt/cray/share/man
export PATH=/cctbx/build/bin:/lcls2/install/bin:/lcls2/build/bin:/opt/rh/devtoolset-7/root/usr/bin:/opt/conda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/udiImage/bin
export PCP_DIR=/opt/rh/devtoolset-7/root
export PERL5LIB=/opt/rh/devtoolset-7/root//usr/lib64/perl5/vendor_perl:/opt/rh/devtoolset-7/root/usr/lib/perl5:/opt/rh/devtoolset-7/root//usr/share/perl5/vendor_perl
export PMI_MMAP_SYNC_WAIT_TIME=600
export PYTHONPATH=/lcls2/install/lib/python2.7/site-packages
export HOME=/tmp
#source /cctbx/build/setpaths.sh

export PS_CALIB_DIR=$IN_DIR
export PS_SMD_N_EVENTS=100
export PS_SMD_NODES=1

# setup playground
#mkdir -p ${OUT_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/out
#mkdir -p ${OUT_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/stdout
#mkdir -p ${OUT_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/tmp

cctbx_args="input.experiment=${EXP} input.run_num=${RUN} output.logging_dir=${OUT_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/stdout output.output_dir=${OUT_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/out format.cbf.invalid_pixel_mask=${IN_DIR}/mask.pickle ${IN_DIR}/process_batch.phil dump_indexed=False output.tmp_output_dir=${OUT_DIR}/discovery/dials/${RUN_F}/${TRIAL_F}/tmp input.xtc_dir=${DATA_DIR} max_events=${LIMIT}"

if [ "${CMDMODE}" = "pythonprof" ]; then
    python -m cProfile -s tottime cctbx.xfel.xtc_process ${cctbx_args}
  
elif [ "${CMDMODE}" = "strace" ]; then
    strace -ttt -f -o $$.log cctbx.xfel.xtc_process ${cctbx_args}

elif [ "${CMDMODE}" = "debug" ]; then
    python /tmp/xtc_process.py ${cctbx_args}
  
else
    cctbx.xfel.xtc_process ${cctbx_args}
  
fi


END_XTC=$(date +"%s")
ELAPSED=$((END_XTC-START_XTC))
echo TotalElapsed ${ELAPSED} ${START_XTC} ${END_XTC}
