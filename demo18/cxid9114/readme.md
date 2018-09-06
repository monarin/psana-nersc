Demo18: Processing LD91 Step-by-step  
You will need an access to the input files (test-r0001.xtc and smalldata/test-r001.smd.xtc):  
/global/cscratch1/sd/monarin/d/psdm/cxi/cxid9114/xtc2  

cd $SCRATCH  
git clone https://github.com/monarin/psana-nersc.git  
cd demo18/cxid9114   
sbatch submit_single.sh   

After the run is completed, the output will be sent to ./output folder. To avoid saving output files
over the network, use    
sbatch submit_lite.sh    
  
Except slurm<jobid>.out, you will not be able to access the output with this option.  

Notes on data  
- Make sure timestamps in small data files are in ascending order  
- If xtc files are converted from the old format, make sure that detector name does not have special characters.  

Build your own docker: use Dockerfile in demo18 directory.  

