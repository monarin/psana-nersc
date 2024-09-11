import os, sys
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

filename = sys.argv[1]

labels = {'WAITTIME SMD0-EB': [(-1, 's', 1, [])],
        'WAITTIME EB-SMD0': [(-2, 's', 2, [])],
        'WAITTIME EB-BD': [(-1, 's', 3, [])],
        'WAITTIME BD-': [(-1, 's', 4, [])],
        'events in': [(-1, 'kHz', 5, [])],
        'READRATE SMD0': [(4, 'MB/s', 6, [])],
        'RATE SMD0-EB': [(-2, 'kHz', 7, [])],
        'RATE EB-BD': [(-2, 'kHz', 8, [])],
        'RATE BD': [(-2, 'kHz', 9, [])],
        'bd reads chunk': [(4,'MB', 10, []), (-2, 'MB/s', 11, [])]
        }

with open(filename, "r") as f:
    for line in f:
        for label, details in labels.items():
            if line.find(label) > -1:
                for detail in details:
                    col_idx, unit, plot_pos, vals = detail
                    cols = line.split()
                    if label == "events in":
                        val = float(cols[col_idx][5:8])
                    else:
                        try:
                            val = float(cols[col_idx])
                        except Exception as e:
                            print(line)
                            print(e)
                            raise
                    vals.append(val)
                break


for label, details in labels.items():
    for detail in details:
        col_idx, unit, plot_pos, vals = detail
        plt.subplot(3, 4, plot_pos)
        plt.plot(vals)
        plt.title(f'{label} avg:{np.average(vals):.2f} min:{np.min(vals):.2f} max:{np.max(vals):.2f}')
        plt.ylabel(unit)
plt.show()

