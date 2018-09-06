Demo18: Processing LD91 Step-by-step  
You will need an access to the input files  
/global/cscratch1/sd/psdatmgr/data/psdm/cxi/cxid9114/demo/xtc/cxid9114x12_stripe.xtc  
/global/project/projectdirs/lcls/mona/demo18/cxid9114/smalldata

mkdir -p $SCRATCH/d/psdm/cxi/cxid9114/xtc2/  
cd $SCRATCH/d/psdm/cxi/cxid9114/xtc2/  
cp -r /global/project/projectdirs/lcls/mona/demo18/cxid9114/smalldata .  
ln -s /global/cscratch1/sd/psdatmgr/data/psdm/cxi/cxid9114/demo/xtc/cxid9114x12_stripe.xtc test-r0002.xtc  
cd $SCRATCH  
git clone https://github.com/monarin/psana-nersc.git  
cd psana-nersc/demo18/cxid9114  

You may need to change --qos, --reservation, --account flags to your own preferred settings in submit_single.sh before submitting the job.   
sbatch submit_single.sh   

This script starts by broadcasting all the input files to the local nodes then run a simple program to check if all the nodes are active. If there are failed nodes, they will be excluded in the next srun command (the indexing part) with -x flag. See submit_lite.sh and index_lite.sh if you want to skip the checking step (note that output for index_lite.sh is sent to /tmp only).   
  
After the run is completed, the output will be sent to the output folder specified as the last argument in srun index_single.sh cmd. To avoid saving output files over the network, you can use /tmp (as shown in the current script). Except slurm<jobid>.out, you will not be able to access the output from /tmp later.  

Notes on data  
- Make sure timestamps in small data files are in ascending order  
- If xtc files are converted from the old format, make sure that detector name does not have special characters.  

Build your own docker: use Dockerfile in demo18 directory.  

