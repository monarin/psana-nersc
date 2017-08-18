#!/bin/bash -l
#SBATCH --partition=regular
#SBATCH --qos=premium
#SBATCH --job-name=psana_sum
#SBATCH --time=00:10:00
#SBATCH --nodes=1
#SBATCH --constraint=haswell
#SBATCH --image=docker:monarin/psanatest:latest
#DW persistentdw name=monarinbb

# timing the script
START_XTC=$(date +"%s")

# cores = 32 x nodes (Cori)
N_CORES=32
#let "N_CPU_PER_PRC = 64 / $N_CORES"
N_CPU_PER_PRC=2

# experiment parameters
EXP=${1}
RUN_ST=${2}
RUN_EN=${3}

srun -n ${N_CORES} -c ${N_CPU_PER_PRC} --cpu_bind=cores shifter ${PWD}/sum_bb.sh ${EXP} ${RUN_ST} ${RUN_EN}

END_XTC=$(date +"%s")
ELAPSED=$((END_XTC-START_XTC))
echo
echo N_Cores ${N_CORES} 
echo TotalElapsed ${ELAPSED} ${START_XTC} ${END_XTC}


