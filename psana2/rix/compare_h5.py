# Compare original h5 data created by Kristjan and from running:
# ./submit_smd.sh -e rixl1013320 -r 93 -d /cds/home/m/monarin/psana-nersc/psana2/rix/output -q ffbl1q -c 5 --epicsAll

import h5py
import numpy as np

f_ori = h5py.File('/cds/data/drpsrcf/rix/rixl1013320/scratch/hdf5/smalldata/rixl1013320_Run0093.h5')
f_new = h5py.File('/cds/home/m/monarin/psana-nersc/psana2/rix/output/rixl1013320_Run0093.h5')

for grp_key in f_ori.keys():
    print(f'f_ori[{grp_key}]={f_ori[grp_key]}')
    if grp_key != 'timestamp':
        for ds_key in f_ori[grp_key].keys():
            #print(f'  {ds_key}={f_ori[grp_key][ds_key]}')
            pass
    else:
        sort_indices = np.argsort(f_new['timestamp'])
        ts_new = f_new['timestamp'][sort_indices]
        print(np.array_equal(np.sort(f_ori['timestamp']), np.sort(f_new['timestamp'])))
