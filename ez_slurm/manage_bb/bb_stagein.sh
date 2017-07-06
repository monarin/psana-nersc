#!/bin/bash
#SBATCH -p regular
#SBATCH -N 1
#SBATCH -C haswell
#SBATCH -t 00:05:00
#DW persistentdw name=myBBname
#DW stage_in source=/global/cscratch1/sd/monarin/d/psdm/cxi/cxid9114/xtc destination=$DW_PERSISTENT_STRIPED_myBBname/d/psdm/cxi/cxid9114/xtc type=directory
