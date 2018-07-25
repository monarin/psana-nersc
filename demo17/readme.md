Demo17 contains scripts for running Exafel demo 2017. A permission to access the test data folder is required to run the following commands.

From cori node,

mkdir -p $SCRATCH/d/psdm/cxi/cxid9114  
cd $SCRATCH/d/psdm  
ln -s $SCRATCH/d/psdm/cxi CXI  
cp -r /global/project/projectdirs/lcls/d/psdm/cxi/cxid9114/calib cxi/cxid9114/  
cd $SCRATCH  
git clone https://github.com/monarin/psana-nersc.git  
cd psana-nersc/demo17  
sbatch -o log.txt submit_single.sh  

This submits run 95 (28 images) using 8 cores. You can change no. of cores and experiment run no. in submit_single.sh. For example,  

#SBATCH ?nodes=2  
...
srun -n 103 -c 4 --cpu_bind=cores shifter ./index_single.sh cxid9114 96 0 debug  

will submit run 96 using 2 nodes (103 cores). Please refer to our scaling spreadsheet for no. of cores used for each run.  

Once the job is done you can check integration results by  
python integration2json.py output/discovery/dials/r0095/000/  
Integration summary json created with this content:  
{'Total processed': 28, 'Not enough spots': 0, 'Failed index': 0, 'Integrated': 28}  
  
No. of total processed should match with no. integrated.



