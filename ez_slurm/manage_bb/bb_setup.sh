#!/bin/bash

mkdir -p $DW_PERSISTENT_STRIPED_myBBname/d/psdm/cxi/cxid9114
mkdir -p $DW_PERSISTENT_STRIPED_myBBname/g/psdm
mkdir -p $DW_PERSISTENT_STRIPED_myBBname/d/psdm/cxi/cxid9114/scratch/mona/discovery
mkdir -p $DW_PERSISTENT_STRIPED_myBBname/d/psdm/cxi/cxid9114/scratch/mona/calib
cp /global/cscratch1/sd/monarin/d/psdm/cxi/cxid9114/scratch/mona/discovery/target.phil $DW_PERSISTENT_STRIPED_myBBname/d/psdm/cxi/cxid9114/scratch/mona/discovery/
cp /global/cscratch1/sd/monarin/d/psdm/cxi/cxid9114/scratch/mona/calib/mask.pickle $DW_PERSISTENT_STRIPED_myBBname/d/psdm/cxi/cxid9114/scratch/mona/calib/
cp -r /global/cscratch1/sd/monarin/g/psdm/data $DW_PERSISTENT_STRIPED_myBBname/g/psdm/
cp -r /global/cscratch1/sd/monarin/d/psdm/cxi/cxid9114/calib $DW_PERSISTENT_STRIPED_myBBname/d/psdm/cxi/cxid9114/


