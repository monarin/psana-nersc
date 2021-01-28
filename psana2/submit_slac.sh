#!/bin/bash
#SBATCH --partition=anagpu
#SBATCH --job-name=psana2-test
#SBATCH --ntasks=4
#SBATCH --ntasks-per-node=4
#SBATCH --output=%j.log
 
# -u flushes print statements which can otherwise be hidden if mpi hangs
t_start=`date +%s`
srun python ./test_mpi.py 

#srun -n 339320 -c 4 --cpu_bind=cores -x=nid08201,nid11988 shifter ./index_lite.sh cxid9114 2 99 debug 0
t_end=`date +%s`

echo PSJobCompleted TotalElapsed $((t_end-t_start)) 
