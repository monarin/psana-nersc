import numpy as np
import time
#import torch

a = np.arange(59400, dtype=np.float64)
#b = np.arange(60000, dtype=int)
#a = torch.arange(2048)
#b = torch.arange(59400)

t = []
for i in range(10):
    st = time.monotonic()
    c = np.outer(a,a)
    #c = torch.outer(b, a)
    en = time.monotonic()
    #print(i, en-st)
    t.append(en-st)

print(f'min: {np.min(t)} max: {np.max(t)} avg: {np.average(t)}')

