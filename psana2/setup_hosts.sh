###
# This script uses two SLURM environment variables to generate
# a host file that places rank 0 on a separate node. No. of 
# available ranks will be fewer (since all ranks on the selected-
# smd0 node are not usable). 
# Slurm variables:
# SLURM_TASKS_PER_NODE e.g. 50(x2),49 for 149 cores on 3 nodes
# SLURM_JOB_NODELIST e.g. drp-srcf-cmp[004-010],drp-srcf-eb[010-011]
###


# Get no. tasks per node array
tasks_per_nodes=()
IFS=',' read -ra TASKS_PER_NODE <<< "$SLURM_TASKS_PER_NODE"
for task_per_node in "${TASKS_PER_NODE[@]}"; do
    # Task per node can be 50(x2) or 25. For the former
    # we need to extract no. of tasks per node and no. of nodes
    task_x=$( echo "$task_per_node" | sed 's/(//' | sed 's/)//' )
    x_char='x'
    if [[ "$task_x" == *"$x_char"* ]]; then
        IFS='x' read -ra tsks_per_node <<< "$task_x"
        n_tasks=${tsks_per_node[0]}
        n_nodes=${tsks_per_node[1]}
        for i in $(seq 1 $n_nodes); do
            tasks_per_node+=( $n_tasks )
        done
    else
        tasks_per_node+=( $task_x )
    fi
done


# Get list of hosts by expand shorthand node list into a 
# line-by-line node list
host_list=$(scontrol show hostnames $SLURM_JOB_NODELIST)
hosts=($host_list)


# Write out to host file by putting rank 0 on the first node
host_file="slurm_host_${SLURM_JOB_ID}"
cn_tasks=0
for i in "${!tasks_per_node[@]}"; do
    if [[ "$i" == "0" ]]; then
        echo ${hosts[$i]} > $host_file
        ((cn_tasks++))
    else
        for j in $(seq 1 ${tasks_per_node[$i]}); do
            echo ${hosts[$i]} >> $host_file
            ((cn_tasks++))
        done
    fi
done

export SLURM_HOSTFILE=$host_file
export SLURM_NTASKS=$cn_tasks
