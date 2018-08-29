#!/bin/bash

grep "failed on node" ${1} | awk '{print $10}' > xx
nodes=(`cat xx`)

let "n_nodes=${#nodes[@]}"
node_list=""
for i in `seq 0 $n_nodes`
do
  node_id=${nodes[$i]} 
  node_list="$node_list ${node_id/\:/\,}"
done
echo $node_list
