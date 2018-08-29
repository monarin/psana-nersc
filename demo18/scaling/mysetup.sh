
t_start=`date +%s`
export PS_SMD_NODES=1
export PS_SMD_N_EVENTS=1000
export PS_CALIB_DIR=/tmp

#strace -ttt -f -o $$.log python /tmp/test_read.py
python /tmp/test_read.py

t_end=`date +%s`
echo OneCore TotalElapsed $((t_end-t_start)) $t_start $t_end
