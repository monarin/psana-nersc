#!/bin/bash -l
#SBATCH --partition=regular
#SBATCH --qos=premium
#SBATCH --job-name=psana_sum
#SBATCH --time=00:10:00
#SBATCH --nodes=38
#SBATCH --constraint=knl
#SBATCH --image=docker:monarin/psananersc:latest
#DW persistentdw name=myBBname

# timing the script
START_XTC=$(date +"%s")

# base directory
BASE_DIR=${DW_PERSISTENT_STRIPED_myBBname}/d/psdm/cxi/cxid9114/scratch/mona

# cores = 32 x nodes (Cori)
N_CORES=2584
#let "N_CPU_PER_PRC = 64 / $N_CORES"
N_CPU_PER_PRC=4

# experiment parameters
EXP=${1}
RUN=${2}

srun -n ${N_CORES} -c ${N_CPU_PER_PRC} --cpu_bind=cores shifter ${PWD}/sum_bb.sh ${EXP} ${RUN}

END_XTC=$(date +"%s")
ELAPSED=$((END_XTC-START_XTC))
echo
echo N_Cores ${N_CORES} 
echo TotalElapsed ${ELAPSED} ${START_XTC} ${END_XTC}


