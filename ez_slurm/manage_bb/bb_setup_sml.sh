#!/bin/bash

mkdir -p $DW_PERSISTENT_STRIPED_myBBsml/d/psdm/cxi/cxid9114
mkdir -p $DW_PERSISTENT_STRIPED_myBBsml/g/psdm
mkdir -p $DW_PERSISTENT_STRIPED_myBBsml/d/psdm/cxi/cxid9114/scratch/mona/discovery
mkdir -p $DW_PERSISTENT_STRIPED_myBBsml/d/psdm/cxi/cxid9114/scratch/mona/calib
cp /global/cscratch1/sd/monarin/d/psdm/cxi/cxid9114/scratch/mona/discovery/target.phil $DW_PERSISTENT_STRIPED_myBBsml/d/psdm/cxi/cxid9114/scratch/mona/discovery/
cp /global/cscratch1/sd/monarin/d/psdm/cxi/cxid9114/scratch/mona/calib/mask.pickle $DW_PERSISTENT_STRIPED_myBBsml/d/psdm/cxi/cxid9114/scratch/mona/calib/
cp -r /global/cscratch1/sd/monarin/g/psdm/data $DW_PERSISTENT_STRIPED_myBBsml/g/psdm/
cp -r /global/cscratch1/sd/monarin/d/psdm/cxi/cxid9114/calib $DW_PERSISTENT_STRIPED_myBBsml/d/psdm/cxi/cxid9114/
ln -s $DW_PERSISTENT_STRIPED_myBBsml/d/psdm/cxi $DW_PERSISTENT_STRIPED_myBBsml/d/psdm/CXI

