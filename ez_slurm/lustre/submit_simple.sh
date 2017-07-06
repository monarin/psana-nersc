#!/bin/bash -l
#SBATCH --partition=regular
#SBATCH --qos=premium
#SBATCH --job-name=psana_simple
#SBATCH --time=00:05:00
#SBATCH --nodes=81
#SBATCH --constraint=haswell
#SBATCH --image=docker:monarin/psananersc:latest
#SBATCH --volume="/global/cscratch1/sd/monarin/d/psdm/cxi:/reg/d/psdm/CXI;/global/cscratch1/sd/monarin/d/psdm/cxi:/reg/d/psdm/cxi;/global/cscratch1/sd/monarin/g:/reg/g"

# timing the script
START_XTC=$(date +"%s")

# base directory
BASE_DIR=/global/cscratch1/sd/monarin/d/psdm/cxi/cxid9114/scratch/mona

# cores = 32 x nodes (Cori)
N_CORES=2592
N_CPU_PER_PRC=2

# experiment parameters
EXP=cxid9114
RUN=${1}

# run simple averaging script
srun -n ${N_CORES} -c ${N_CPU_PER_PRC} --cpu_bind=cores shifter ${BASE_DIR}/sum.sh ${EXP} ${RUN}

END_XTC=$(date +"%s")
ELAPSED=$((END_XTC-START_XTC))
echo
echo N_Cores ${N_CORES} 
echo TotalElapsed ${ELAPSED} ${START_XTC} ${END_XTC}


