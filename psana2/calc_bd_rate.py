import sys, os
import numpy as np
filename = sys.argv[1]
import matplotlib.pyplot as plt

data = []
with open(filename, 'r') as f:
    for line in f:
        #if line.find('bd reads chunk') >= 0:
        if line.find('rate:') >= 0:
            rate = line.split()[4]
            try:
                val = float(rate[5:9])
                data.append(val)
            except Exception:
                print('error')
            #data.append(float(line.split()[16]))

plt.hist(data)
plt.title(f'bigdata nodes rate (kHz) mean={np.mean(data):.2f} min={np.min(data):.2f} max={np.max(data):.2f}')
plt.xlabel('kHz')
plt.show()
