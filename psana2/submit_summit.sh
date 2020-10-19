#!/bin/bash
#BSUB -P CHM137
#BSUB -W 00:15
#BSUB -nnodes 7
#BSUB -alloc_flags gpumps
#BSUB -J RunPsana2
#BSUB -o RunPsana2.%J
#BSUB -e RunPsana2.%J
 
t_start=`date +%s`

source $MEMBERWORK/chm137/installation/psana2/summit/env.sh

#jsrun -n44 -r11 -a1 -c1 -g0 ./run.sh
#jsrun --erf_input erf.txt ./run.sh
jsrun -n 261 ./run.sh

t_end=`date +%s`
echo PSJobCompleted TotalElapsed $((t_end-t_start)) $t_start $t_end
