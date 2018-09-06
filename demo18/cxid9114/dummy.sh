# Determine failed nodes from chk_nodes slurm output
NODES=10
failed_nodes=`./show_failed_nodes.sh`
IFS=',' read -r -a array <<< $failed_nodes
let "n_failed_nodes=${#array[@]}"
exclude_flag=""
if [ "$n_failed_nodes" -gt 0 ]; then
  exclude_flag="-x $failed_nodes "
fi
ACTIVE_NODES=$((NODES-n_failed_nodes))
ACTIVE_CORES=$((ACTIVE_NODES*68))

echo "srun -N $ACTIVE_NODES -n $ACTIVE_CORES -c 4 --cpu_bind=cores ${exclude_flag}shifter ./index_single.sh cxid9114 2 0 debug $LIMIT /tmp"
