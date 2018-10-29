import numpy as np
import matplotlib.pyplot as plt
import glob, os

debug_files=glob.glob('/global/cscratch1/sd/monarin/psana-nersc/demo18/cxic0415/out/*.txt')

for df in debug_files:
    x = [0]*100
    rank = int(os.path.basename(df).split('_')[0])
    with open(df, 'r') as f:
        cn_elem = 0
        print("read rank %d"%rank)
        for data in f:
            try:
                x[cn_elem] = float(data)
                cn_elem += 1
            except:
	        pass
    y = [rank]*len(x)
    plt.scatter(x[:cn_elem], y[:cn_elem], s=2, c='b', alpha=0.5)

plt.show()
      
