#!/bin/bash
EXP=${1}
TRIAL=${2}
FS=${3}
BBNAME=${4}

if [ ${1} == "" ]; then
echo "Usage: ./prime.sh EXP TRIAL_NO FS(Lustre/BB/GPFS) BurstBufferName CMDMODE(none/pythonprof/strace/debug)"
else

if [ ${FS} == "BB" ]; then
  PSREF=`echo DW_PERSISTENT_STRIPED_$BBNAME`
  PSDIR="${!PSREF}"
  WKDIR=${PSDIR}
elif [ ${FS} == "GPFS" ]; then
  PSDIR=/global/project/projectdirs/lcls
  WKDIR=$SCRATCH
else
  PSDIR=$SCRATCH
  WKDIR=$SCRATCH
fi

#cctbx
source /build/setpaths.sh

TRIAL_F="$(printf "%03d" ${TRIAL})"
DATA=${PSDIR}/d/psdm/cxi/${EXP}/scratch/discovery/dials/r0109/${TRIAL_F}/out/*.tar

python mpi_run.py ${WKDIR}/d/psdm/cxi/${EXP}/scratch/discovery/prime.phil n_postref_cycle=0 data=${PSDIR}/d/psdm/cxi/${EXP}/scratch/discovery/dials/pickle.lst

fi
