import sys
import numpy as np

fname = sys.argv[1]
vals = []
with open(fname,'r') as f:
  for line in f: vals.append(float(line.strip()))

print 'Mean=%6.2f Median=%6.2f Min=%6.2f Max=%6.2f'%(np.mean(vals), np.median(vals), min(vals), max(vals))

