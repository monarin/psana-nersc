import os
import sys

import numpy as np

filename = sys.argv[1]
import matplotlib.pyplot as plt

data = {
    "WAITTIME SMD0-EB": [],
    "WAITTIME EB-SMD0": [],
    "WAITTIME EB-BD": [],
    "WAITTIME BD-EB": [],
    "RATE SMD0-EB": [],
    "RATE EB-BD": [],
    "RATE BD": [],
    "READRATE SMD0": [],
}

with open(filename, "r") as f:
    for line in f:
        for tag_name, values in data.items():
            if line.find(tag_name) >= 0:
                try:
                    values.append(float(line.split()[4]))
                except Exception as e:
                    print(e)

for i, (tag_name, values) in enumerate(data.items()):
    try:
        plt.subplot(2, 4, i + 1)
        plt.plot(values, label=tag_name)
        plt.title(
            f"({len(values)}) avg={np.mean(values):.2f} min={np.min(values):.2f} max={np.max(values):.2f}"
        )
        plt.xlabel(tag_name)
    except Exception as e:
        print(e)
plt.show()
