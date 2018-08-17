with open('xx','r') as f:
  content = f.readlines()

content = [x.strip() for x in content] 
import numpy as np
t = np.zeros(len(content))
for i, line in enumerate(content):
  t[i] = float(line.split(', ')[-1].split(')')[0])

print('No. of events (all): %d indexing time (s) min: %5.2f max: %5.2f avg: %5.2f'%(t.shape[0], np.min(t), np.max(t), np.average(t)))
t_long = t[t>60]
print('No. of events (>60s):%d indexing time (s) min: %5.2f max: %5.2f avg: %5.2f'%(t_long.shape[0], np.min(t_long), np.max(t_long), np.average(t_long)))
