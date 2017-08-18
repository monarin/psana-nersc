#!/bin/bash -l
#SBATCH --partition=regular
#SBATCH --qos=premium
#SBATCH --job-name=psana_simple
#SBATCH --time=00:30:00
#SBATCH --nodes=1
#SBATCH --constraint=haswell
#SBATCH --image=docker:monarin/psananersc:latest
#SBATCH --volume="/global/cscratch1/sd/monarin/d/psdm/cxi:/reg/d/psdm/CXI;/global/cscratch1/sd/monarin/d/psdm/cxi:/reg/d/psdm/cxi;/global/cscratch1/sd/monarin/g:/reg/g"

# timing the script
START_XTC=$(date +"%s")

# cores = 32 x nodes (Cori)
N_CORES=32
N_CPU_PER_PRC=2

# experiment parameters
EXP=${1}
RUN=${2}

# run simple averaging script
srun -n ${N_CORES} -c ${N_CPU_PER_PRC} --cpu_bind=cores shifter ${PWD}/sum.sh ${EXP} ${RUN}

END_XTC=$(date +"%s")
ELAPSED=$((END_XTC-START_XTC))
echo
echo N_Cores ${N_CORES} 
echo TotalElapsed ${ELAPSED} ${START_XTC} ${END_XTC}


