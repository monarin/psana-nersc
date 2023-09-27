# First node must be exclusive to smd0
# * For openmpi, slots=1 must be assigned to the first node.
# Slurm variables:
# SLURM_JOB_NODELIST e.g. drp-srcf-cmp[004-010],drp-srcf-eb[010-011]
###


# Get list of hosts by expand shorthand node list into a 
# line-by-line node list
host_list=$(scontrol show hostnames $SLURM_JOB_NODELIST)
hosts=($host_list)


# Write out to host file by putting rank 0 on the first node
host_file="slurm_host_${SLURM_JOB_ID}"
for i in "${!hosts[@]}"; do
    if [[ "$i" == "0" ]]; then
        echo ${hosts[$i]} slots=1 > $host_file
    else
        echo ${hosts[$i]} >> $host_file
    fi
done

echo $host_file
