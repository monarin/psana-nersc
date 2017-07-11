#!/bin/bash

EXP=${1}
RUN_NO=${2}
CONST=${3}
FS=${4}
BBNAME=${5}

# get no. of cpus and times from smart.conf
conf_cpus=`grep cpus smart.conf`
n_cpus=`(echo $conf_cpus)`
conf_times=`grep times smart.conf`
n_times=`(echo $conf_times)`
EMAIL=`grep email smart.conf | awk '{print $2}'`

# create constant vars for different contraints
if [ $CONST == "knl" ]; then
  const_core=68
  const_thread=272
  const_max_thread=4
else
  const_core=32
  const_thread=64
  const_max_thread=2
fi

# build job submission script
let "n_tasks=${#n_cpus[@]}-1"
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
  cat > submit_$$_${i}.sh << EOL
#!/bin/bash -l
#SBATCH --partition=regular
#SBATCH --qos=premium
#SBATCH --job-name=psauto
#SBATCH --nodes=${n_node}
#SBATCH --constraint=${CONST}
#SBATCH --time=${n_times[$i]}
#SBATCH --image=docker:monarin/psananersc:latest
EOL
  if [ ${FS} == "BB" ]; then
    echo "#DW persistentdw name=${BBNAME}" >> submit_$$_${i}.sh
  fi
  echo 't_start=`date +%s`' >> submit_$$_${i}.sh
  echo "srun -n ${n_cpus[$i]} -c ${n_cpu_pp} --cpu_bind=cores shifter ${PWD}/activate.sh ${EXP} ${RUN_NO} ${FS} ${BBNAME}" >> submit_$$_${i}.sh
  echo 't_end=`date +%s`' >> submit_$$_${i}.sh
  echo "n_cpus=${n_cpus[$i]}" >> submit_$$_${i}.sh
  echo 'echo N_Cpus $n_cpus' >> submit_$$_${i}.sh
  echo 'echo PSJobCompleted TotalElapsed $((t_end-t_start)) $t_start $t_end' >> submit_$$_${i}.sh
  
  sbatch -o log_$$_${i}.txt submit_$$_${i}.sh
  echo "Job script submit_$$_${i}.sh submitted"
  while true; do
    DATE=`date +%Y-%m-%d:%H:%M:%S`
    echo "$EXP $RUN_NO Cores: ${n_cpus[$i]} Time:${n_times[$i]}"
    ls log_$$_${i}.txt
    if [ $? -eq 0 ]; then
      is_done=`grep PSJobCompleted log_$$_${i}.txt | wc -l`
      if [ $is_done -eq 1 ]; then
        echo "$DATE Job is done"
        echo "$EXP $RUN_NO Cores: ${n_cpus[$i]} Time:${n_times[$i]} is done on $DATE" | mail -s "Cori Job Done" $EMAIL
        break
      else
        echo "$DATE Job is running..."
        sleep 5
      fi
    else
      echo "$DATE Job is still pending..."
      sleep 5
    fi
  done
done
