Notes on running rixl1013320 r93 and r63

Running smalldata scripts:
    ./setup_and_run_smdtool.sh

Collect job time:
    grep "JOB TIME:" smalldata_tools/arp_scripts/slurm-jobid.out


Note:
1. There are some changes in smd2_producer.py to disable force set PS_SRV_NODES and use xtcdir from PS_XTC_DIR env var.  
2. Detector atmopal in stream 006 has been removed (TXAX_laser.py also got updated to not get this data from h5 file).
