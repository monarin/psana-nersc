import sys
import numpy as np
import matplotlib.pyplot as plt


fname = sys.argv[1]
max_rows = 100
n_cols = 16
results = np.zeros([max_rows, n_cols], dtype=float)
with open(fname, 'r') as f:
    cn_rows = 0
    for line in f:
        cols = list(map(float, line.split()))
        if len(cols) == 16:
            results[cn_rows,:] = cols
            cn_rows += 1

# Data labels
# Smd0 (read MB/s, send MB/s, send kHz, Max Wait (s))
# EB (send MB/s, send kHz, Max Wait Smd0 (s), Max Wait BD (s))
# BD (read MB/s, process kHz, read (s), gen smd (s/batch), gen evt (s/batch), Max Wait (s/batch), Analysis (s/batch))
#print(results)
shows = results[:cn_rows, :]
ts = shows[:,0] - shows[0,0]

plt.subplot(3,4,1)
plt.plot(ts, shows[:,1])
plt.title('SMD0 Read (MB/s)')

plt.subplot(3,4,3)
plt.plot(ts, shows[:,2])
plt.title('SMD0 Send (MB/s)')

plt.subplot(3,4,2)
plt.plot(ts, shows[:,3])
plt.title('SMD0 Send (kHz)')

plt.subplot(3,4,4)
plt.plot(ts, shows[:,4])
plt.title('SMD0 Max Wait (s)')

plt.subplot(3,4,5)
plt.plot(ts, shows[:,5])
plt.title('EB Send (MB/s)')

plt.subplot(3,4,6)
plt.plot(ts, shows[:,6])
plt.title('EB Send (kHz)')

plt.subplot(3,4,7)
plt.plot(ts, shows[:,7])
plt.title('EB Max Wait Smd0 (s)')

plt.subplot(3,4,8)
plt.plot(ts, shows[:,8])
plt.title('EB Max Wait BD (s)')

plt.subplot(3,4,9)
plt.plot(ts, shows[:,9])
plt.title('BD Read (MB/s)')

plt.subplot(3,4,10)
plt.plot(ts, shows[:,10])
plt.title('BD Process (kHz)')

plt.subplot(3,4,11)
plt.plot(ts, shows[:,14])
plt.title('Max Wait (s)')

plt.subplot(3,4,12)
plt.plot(ts, shows[:,15])
plt.title('Analysis (s/batch)')
plt.show()


