import os, sys
import numpy as np
#import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt

filename = sys.argv[1]

vals = []
with open(filename, "r") as f:
    for line in f:
        if line.find(f'PROCRATE') >= 0:
            cols = line.split()
            val = float(cols[3])
            print(val)
            vals.append(val)

plt.hist(vals)
plt.title(f'BD Processing Rate Avg:{np.mean(vals):.2f}kHz Max:{np.max(vals):.2f}kHz Min:{np.min(vals):.2f}kHz')
plt.xlabel('Processing Rate (kHz)')
plt.ylabel('Frequencies')
plt.show()
#plt.savefig('foo.png')
