#!/bin/bash
#SBATCH --partition=milano
#SBATCH --account=lcls:data
#SBATCH --job-name=test-psana2
#SBATCH --output=output-%j.txt
#SBATCH --nodes=2
#SBATCH --exclusive
#SBATCH --time=30:00
##SBATCH --acount=lcls:prjdat21


t_start=`date +%s`


# Configure psana2 parallelization
export PS_N_TASKS_PER_NODE=120
echo PS_N_TASKS_PER_NODE=$PS_N_TASKS_PER_NODE
source setup_hosts_openmpi.sh


#mpirun -np $PS_N_RANKS --hostfile $PS_HOST_FILE python test_mpi.py
export PS_EB_NODES=4
export PS_SRV_NODES=0
export PS_VERBOSITY=0
export PS_ZEROEDBUG_WAIT_SEC=0
#MAX_EVENTS=0
#EXP="tmoc00221"
#RUNNO=34
#XTCDIR="/sdf/data/lcls/drpsrcf/ffb"
#mpirun -np $PS_N_RANKS --hostfile $PS_HOST_FILE python test_live.py $EXP $RUNNO $MAX_EVENTS ${XTCDIR}
mpirun -n 121 --hostfile $PS_HOST_FILE python test_psana2_perf.py


t_end=`date +%s`
echo PSJobCompleted TotalElapsed $((t_end-t_start)) 
