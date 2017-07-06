#!/bin/bash -l
#SBATCH --partition=regular
#SBATCH --qos=premium
#SBATCH --job-name=psana_sum
#SBATCH --time=00:10:00
#SBATCH --nodes=27
#SBATCH --constraint=haswell
#SBATCH --image=docker:monarin/psananersc:latest
#DW persistentdw name=myBBsml

# timing the script
START_XTC=$(date +"%s")

# base directory
BASE_DIR=${DW_PERSISTENT_STRIPED_myBBsml}/d/psdm/cxi/cxid9114/scratch/mona

# cores = 32 x nodes (Cori)
N_CORES=864
#let "N_CPU_PER_PRC = 64 / $N_CORES"
N_CPU_PER_PRC=2

# experiment parameters
EXP=cxid9114
RUN=${1}

srun -n ${N_CORES} -c ${N_CPU_PER_PRC} --cpu_bind=cores shifter ${BASE_DIR}/sum_bb.sh ${EXP} ${RUN}

END_XTC=$(date +"%s")
ELAPSED=$((END_XTC-START_XTC))
echo
echo N_Cores ${N_CORES} 
echo TotalElapsed ${ELAPSED} ${START_XTC} ${END_XTC}


