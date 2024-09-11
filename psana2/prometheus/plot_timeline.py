import sys

fname = sys.argv[1]
rank = sys.argv[2]

prev_ts = 0
deltas = []
cn_waits = 0
txt_total_rate = ''
txt_n_nodes = ''
with open(fname, 'r') as f:
    for line in f:
        if line.find(f'rank:{rank} TIMELINE') > -1:
            cols = line.split()
            ts = float(cols[-1])
            if prev_ts:
                delta = (ts-prev_ts)*1000
                deltas.append(delta)
                if delta > 100:
                    cn_waits += 1
                    print(line)
            prev_ts = ts
        elif line.find('events=') > -1:
            cols = line.split()
            txt_total_rate = cols[-1]
            txt_n_nodes = cols[1] +' '+ cols[2]

import matplotlib.pyplot as plt
plt.plot(deltas)
plt.title(f'RANK{rank} Timeline ({cn_waits=}) {txt_n_nodes} {txt_total_rate} ')
plt.show()
