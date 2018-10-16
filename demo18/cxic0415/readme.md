Demo18: Processing Se-SAD (cxic0415)  
Bigdata file: /global/cscratch1/sd/psdatmgr/data/psdm/cxi/cxic0415/demo/xtc/cxic0415.xtc  
Smddata file: /global/project/projectdirs/lcls/mona/demo18/cxic0415/smalldata/test-r0050.smd.xtc  
  
mkdir -p $SCRATCH/d/psdm/cxi/cxic0415/xtc2/  
cd $SCRATCH/d/psdm/cxi/cxic0415/xtc2/  
cp -r /global/project/projectdirs/lcls/mona/demo18/cxic0415/smalldata .  
ln -s /global/cscratch1/sd/psdatmgr/data/psdm/cxi/cxic0415/demo/xtc/cxic0415.xtc test-r0050.xtc  
cd $SCRATCH  
git clone https://github.com/monarin/psana-nersc.git  
cd psana-nersc/demo18/cxic0415  
  

Note that all the runs from cxic0415 are glued together in one xtc file. This is named to run 50 (test-r0050.xtc) so that all the calibration constants can be picked up correctly.  
  

You may need to change --qos, --reservation, --account flags to your own preferred settings in submit_single.sh before submitting the job.  
sbatch submit_single.sh  
  
All the output files are being sent to the same folder (either /tmp or $PWD/output).  
