import sys

import matplotlib.pyplot as plt
import numpy as np

fname = sys.argv[1]
data = []
with open(fname, "r") as f:
    for line in f:
        try:
            data.append(float(line))
        except Exception:
            pass
print(len(data), np.min(data), np.mean(data), np.max(data))
