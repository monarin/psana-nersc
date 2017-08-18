#!/bin/bash

DWBB=$DW_PERSISTENT_STRIPED_monarinbb
EXP=${1}

mkdir -p ${DWBB}/d/psdm/cxi/${EXP}
mkdir -p ${DWBB}/g/psdm
mkdir -p ${DWBB}/d/psdm/cxi/${EXP}/scratch/discovery
mkdir -p ${DWBB}/d/psdm/cxi/${EXP}/scratch/calib
#cp /global/cscratch1/sd/monarin/d/psdm/cxi/${EXP}/scratch/discovery/target.phil ${DWBB}/d/psdm/cxi/${EXP}/scratch/discovery/
#cp /global/cscratch1/sd/monarin/d/psdm/cxi/${EXP}/scratch/calib/mask.pickle $${DWBB}/d/psdm/cxi/${EXP}/scratch/calib/
cp -r /global/cscratch1/sd/monarin/g/psdm/data ${DWBB}/g/psdm/
cp -r /global/cscratch1/sd/monarin/d/psdm/cxi/${EXP}/calib ${DWBB}/d/psdm/cxi/${EXP}/

