import os
import sys

import numpy as np

filename = sys.argv[1]
req_procid = -1
if len(sys.argv) > 2:
    req_procid = int(sys.argv[2])
import matplotlib.pyplot as plt

val = 0
deltas, tags = ([], [])
with open(filename, "r") as f:
    for lineno, line in enumerate(f):
        cols = line.split()
        try:
            procid = int(cols[0])
            if req_procid == -1 or procid == req_procid:
                tmp_val = float(cols[1])
                if val > 0:
                    deltas.append((tmp_val - val) * 1e3)
                    tags.append(cols[2][:10])
                    if deltas[-1] > 20:
                        print(deltas[-1], tags[-1], f"#LINE:{lineno+1}")
                val = tmp_val
        except Exception as e:
            print(e)

deltas = np.array(deltas)
threshold = 10
shows = deltas[deltas > threshold]
# shows = tmp_shows[tmp_shows<100]
plt.plot(shows)
plt.title(f"avg={np.mean(shows):.2f} min={np.min(shows):.2f} max={np.max(shows):.2f}")
plt.show()
