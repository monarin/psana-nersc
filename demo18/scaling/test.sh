source /opt/conda/etc/profile.d/conda.sh
conda activate base
source /opt/rh/devtoolset-7/enable
export PATH=/lcls2/install/bin:/lcls2/build/bin:${PATH}
export PYTHONPATH=/lcls2/install/lib/python2.7/site-packages

export PS_SMD_N_EVENTS=1000
export PS_SMD_NODES=3
export PMI_MMAP_SYNC_WAIT_TIME=600

sbcast -p ./test.py /tmp/test.py
python /tmp/test.py

#python test.py
#strace -ttt -f -o $$.log python test.py
