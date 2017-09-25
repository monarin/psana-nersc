import matplotlib.pyplot as plt

def is_number(s):
  try:
    float(s)
    return True
  except ValueError:
    return False

with open('xx','r') as f:
 data = f.read().split('\n')

data_f = [float(i) for i in data if is_number(i)]
plt.hist(data_f, 20)
plt.xlabel('ds.jump (seconds)')
plt.title('Profiling ds.jump 3117 ranks on 3118 events (cxid9114 r105)')
plt.show()

