#!/bin/bash
# Get list of failed nodes from slurm log file.
slurm_o="slurm-$SLURM_JOB_ID.out"
if [ -f $slurm_o ]; then
  grep "failed on node" $slurm_o | awk '{print $10}' > xx
  nodes=(`cat xx`)

  let "n_nodes=${#nodes[@]}"
  node_list=""
  for i in `seq 0 $n_nodes`
  do
    node_id=${nodes[$i]} 
    if [ "$node_id" != "" ]; then
      if [ "$node_list" != "" ]; then
        node_list="$node_list,${node_id%?}"
      else
        node_list="${node_id%?}"
      fi
    fi
  done

  if [ "$node_list" != "" ]; then
    echo $node_list
  fi
fi
