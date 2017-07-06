echo $SCRATCH # Your scratch folder 

# Log on to cori node
alias alloc='salloc -N 1 -p debug -C haswell --image=docker:monarin/psananersc:latest -t 00:30:00'

# Log on to cori node with BurstBuffer
alias alloc_bb='salloc -N 1 -p debug -C haswell --image=docker:monarin/psananersc:latest -t 00:30:00 --bbf="bbf.conf"'

# Activate shifter
alias activate_shifter='shifter /bin/bash'
