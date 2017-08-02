# psana-nersc
Dockerfile
Psana/Cctbx and their dependencies build for Nersc Shifter.
2017-08-01:
- psana-conda: 1.3.9
- cctbx: update indexing parameters (tmp_output_dir, etc.) 

ez_slurm: Sample job submitting scripts.
To submit a job(s) automatically, use ez_slurm/auto
You can submit jobs with different no. of cpus and allocated times using this
script. After a jobs is completed, you will receive an email from the address
as specified in the smart.conf file.
- Setup data folder (see below)
- Modify the config file, smart.conf, for no. of cpus, allocated times, and your email
- Runing the script:
  . smart_submit.sh exp run_no constraint filesystem [optional: burstbuffer_name]
  Examples:
  . smart_submit.sh cxid9114 108 haswell lustre
  . smart_submit.sh cxid9114 108 knl BB myBBname
- Optional: Update environment variables or Python worker script in activate.sh
- Optional: Update Python worker script 
 
To submit a job manually on Cori-I, see lustre or burstbuffer folders 
for specific settings on different file systems.
- submit_simple.sh: Slurm job submitting script
- sum.sh: Set environment variables for Psana and Cctbx then call worker script
- simpler_psana.py: Worker Python script

To setup a data folder
1. On Lustre (Cori Scratch)
- mkdir -p $SCRATCH/d/psdm/cxi
- ln -s $SCRATCH/d/psdm/cxi $SCRATCH/d/psdm/CXI
- Copy your experimental folder to $SCRATCH/d/psdm/cxi
- mkdir -p $SCRATCH/g
- Copy experiment database folder to $SCRATCH/g
2. On Burstbuffer
- See manage_bb for creating/managing a burstbuffer
- Follow (1) and substitute $SCRATCH with $DW_PERSISTENT_STRIPED_myBBname 
  when myBBname is your burstbuffer. 
