#!/bin/bash

EXP=${1}

mkdir -p $DW_PERSISTENT_STRIPED_myBBsml/d/psdm/cxi/${EXP}/xtc
mkdir -p $DW_PERSISTENT_STRIPED_myBBsml/g/psdm
mkdir -p $DW_PERSISTENT_STRIPED_myBBsml/d/psdm/cxi/${EXP}/scratch/discovery
mkdir -p $DW_PERSISTENT_STRIPED_myBBsml/d/psdm/cxi/${EXP}/scratch/calib
cp /global/cscratch1/sd/monarin/d/psdm/cxi/${EXP}/scratch/discovery/target.phil $DW_PERSISTENT_STRIPED_myBBsml/d/psdm/cxi/${EXP}/scratch/discovery/
cp /global/cscratch1/sd/monarin/d/psdm/cxi/${EXP}/scratch/calib/mask.pickle $DW_PERSISTENT_STRIPED_myBBsml/d/psdm/cxi/${EXP}/scratch/calib/
cp -r /global/cscratch1/sd/monarin/g/psdm/data $DW_PERSISTENT_STRIPED_myBBsml/g/psdm/
cp -r /global/cscratch1/sd/monarin/d/psdm/cxi/${EXP}/calib $DW_PERSISTENT_STRIPED_myBBsml/d/psdm/cxi/${EXP}/
ln -s $DW_PERSISTENT_STRIPED_myBBsml/d/psdm/cxi $DW_PERSISTENT_STRIPED_myBBsml/d/psdm/CXI
cp -r /global/cscratch1/sd/monarin/d/psdm/cxi/${EXP}/xtc/index $DW_PERSISTENT_STRIPED_myBBsml/d/psdm/cxi/${EXP}/xtc/
cp -r /global/cscratch1/sd/monarin/d/psdm/cxi/${EXP}/xtc/smalldata $DW_PERSISTENT_STRIPED_myBBsml/d/psdm/cxi/${EXP}/xtc/
