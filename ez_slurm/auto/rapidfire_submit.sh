#!/bin/bash
if [ "${1}" = "" ]; then
echo "Usage: ./rapidfire_submit.sh EXP TRIAL TASK(CCTBX/profile) CONST(knl/haswell) FS(lustre/BB/GPFS) BBNAME"
else
EXP=${1}
TRIAL=${2}
TASK=${3}
CONST=${4}
FS=${5}
BBNAME=${6}

# get no. of cpus and times from smart.conf
n_cpus=(`grep cpus rapid.conf`)
n_times=(`grep times rapid.conf`)
n_runs=(`grep runs rapid.conf`)
EMAIL=`grep email rapid.conf | awk '{print $2}'`

# create constant vars for different contraints
if [ $CONST == "haswell" ]; then
  const_core=32
  const_thread=64
  const_max_thread=2
else
  const_core=68
  const_thread=272
  const_max_thread=4
fi

# build job submission script
let "n_tasks=${#n_cpus[@]}-1"
for i in `seq 1 $n_tasks`
do
  # set compatible run no.
  RUN_ST=${n_runs[$i]}
  RUN_EN=${n_runs[$i]}
  # calculate no. of nodes
  let "n_node=(${n_cpus[$i]}+$const_core-1)/$const_core"
  # calculate no. of cpus per proc
  if [ ${n_cpus[$i]} -ge $const_core ]; then
    n_cpu_pp=$const_max_thread
  else
    let "n_cpu_pp=$const_thread / ${n_cpus[$i]}"
  fi
  cat > submit_$$_${i}.sh << EOL
#!/bin/bash -l
#SBATCH --partition=regular
#SBATCH --account=lcls
#SBATCH --qos=premium
#SBATCH --job-name=psauto
#SBATCH --nodes=${n_node}
#SBATCH --constraint=${CONST}
#SBATCH --time=${n_times[$i]}
#SBATCH --image=docker:monarin/psanatest:latest
EOL
  if [ ${FS} == "BB" ]; then
    echo "#DW persistentdw name=${BBNAME}" >> submit_$$_${i}.sh
  fi
  echo 't_start=`date +%s`' >> submit_$$_${i}.sh
  if [ ${TASK} == "CCTBX" ]; then
    if [ ${CONST} == "knl,quad,flat" ]; then
      echo "srun -n ${n_cpus[$i]} -c ${n_cpu_pp} --cpu_bind=cores numactl -p 1 shifter ${PWD}/index.sh ${EXP} ${RUN_ST} ${RUN_EN} ${TRIAL} ${FS} ${BBNAME}" >> submit_$$_${i}.sh
    else
      echo "srun -n ${n_cpus[$i]} -c ${n_cpu_pp} --cpu_bind=cores shifter ${PWD}/index.sh ${EXP} ${RUN_ST} ${RUN_EN} ${TRIAL} ${FS} ${BBNAME}" >> submit_$$_${i}.sh
    fi
  else
    if [ ${CONST} == "knl,quad,flat" ]; then
      echo "srun -n ${n_cpus[$i]} -c ${n_cpu_pp} --cpu_bind=cores numactl -p 1 shifter ${PWD}/client_server.sh ${EXP} ${RUN_ST} ${RUN_EN} ${FS} ${BBNAME}" >> submit_$$_${i}.sh
    else
      echo "srun -n ${n_cpus[$i]} -c ${n_cpu_pp} --cpu_bind=cores shifter ${PWD}/client_server.sh ${EXP} ${RUN_ST} ${RUN_EN} ${FS} ${BBNAME}" >> submit_$$_${i}.sh
    fi
  fi
  echo 't_end=`date +%s`' >> submit_$$_${i}.sh
  echo "n_cpus=${n_cpus[$i]}" >> submit_$$_${i}.sh
  echo 'echo N_Cpus $n_cpus' >> submit_$$_${i}.sh
  echo 'echo PSJobCompleted TotalElapsed $((t_end-t_start)) $t_start $t_end' >> submit_$$_${i}.sh
  
  sbatch -o log_$$_${i}.txt submit_$$_${i}.sh
  echo "Job script submit_$$_${i}.sh submitted"
done

fi
