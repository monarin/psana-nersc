import os, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

filename = sys.argv[1]
rank = int(sys.argv[2])

vals = []
with open(filename, "r") as f:
    for line in f:
        if line.find(f'RANK:{rank} wait') == 0:
            cols = line.split()
            val = float(cols[2])
            print(val)
            vals.append(val)

plt.plot(vals)
plt.title('N_bd=1 batch_size=1000 (single EB/ 15 smd files)')
plt.xlabel('batch#')
plt.ylabel('seconds')
plt.savefig('foo.png')
