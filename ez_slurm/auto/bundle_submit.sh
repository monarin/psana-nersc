#!/bin/bash
if [ "${1}" = "" ]; then
  echo "Usage: ./bundle_submit.sh EXP TRIAL N_GROUPS ALLOCTIME"
else
EXP=${1}
TRIAL=${2}
ALLOCTIME=${4}
let "N_GROUPS=${3}-1"
n_nodes=(60 61 61 61 63 62 61)
for i in `seq 0 $N_GROUPS`
do
  let "GROUPID=$i+1"
  sbatch -o log_${GROUPID}.txt sbundle.sh $EXP $TRIAL $GROUPID ${n_nodes[$i]} $ALLOCTIME
done
fi
