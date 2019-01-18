#!/bin/bash
#SLURM_JOB_NODELIST="nid000[63,72-75,77-81]"
nodes=(`scontrol show hostnames $SLURM_JOB_NODELIST`)

n_cores=32
node_list=""
f_name="hosts"
let "n_nodes=${#nodes[@]} - 1"
for i in $(seq 0 $n_nodes)
do
    node=${nodes[$i]}
    if [ $i -eq 0 ]; then
        printf '%b' "$node\n" > ${f_name}
    else
        for j in $(seq 1 $n_cores)
        do
            printf '%b' "$node\n" >> ${f_name}
        done
    fi
done


