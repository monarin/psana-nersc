import os, sys
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

filename = sys.argv[1]
search_term = sys.argv[2]

vals = []
with open(filename, "r") as f:
    for line in f:
        if line.find(search_term) > -1:
            cols = line.split()
            if search_term == "events in":
                val = float(cols[-1][5:8])
            elif search_term == "WAITTIME EB-SMD0":
                val = float(cols[-2])
            else:
                val = float(cols[-1])

            #if val > 50  or val < 10: continue
            print(val)
            vals.append(val)

plt.plot(vals)
plt.title(f'{search_term} avg:{np.average(vals):.2f} min:{np.min(vals):.2f} max:{np.max(vals):.2f}')
plt.xlabel('time')
plt.ylabel('seconds')
plt.show()
