#!/bin/bash -l
#SBATCH --partition=regular
#SBATCH --account=lcls
#SBATCH --qos=premium
#SBATCH --job-name=psauto
#SBATCH --nodes=${4}
#SBATCH --constraint=knl
#SBATCH --time=${5}
#SBATCH --image=docker:monarin/psanatest:latest
t_start=`date +%s`

if [ "${1}" == "" ]; then
  echo "Usage: ./sbundle.sh EXP TRIAL GROUPNO N_NODES TIME"
else
EXP=${1}
TRIAL=${2}
GROUPNO=${3}
runs=(`grep runs_${GROUPNO} bundle.conf`)
n_cpus=(`grep n_cpus_${GROUPNO} bundle.conf`)

const_core=68
const_thread=272
const_max_thread=4

let "n_tasks=${#runs[@]}-1"
for i in `seq 1 $n_tasks`
do
  # calculate no. of nodes
  let "n_node=(${n_cpus[$i]}+$const_core-1)/$const_core"
  # calculate no. of cpus per proc
  if [ ${n_cpus[$i]} -ge $const_core ]; then
    n_cpu_pp=$const_max_thread
  else
    let "n_cpu_pp=$const_thread / ${n_cpus[$i]}"
  fi
  srun -N $n_node -n ${n_cpus[$i]} -c $n_cpu_pp --cpu_bind=cores shifter /global/cscratch1/sd/monarin/d/psdm/cxi/cxid9114/scratch/mona/psana-nersc/ez_slurm/auto/index.sh $EXP ${runs[$i]} ${runs[$i]} $TRIAL GPFS &
done
wait
fi

t_end=`date +%s`
echo PSJobCompleted TotalElapsed $((t_end-t_start)) $t_start $t_end
