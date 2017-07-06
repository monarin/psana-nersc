import h5py
import numpy as np
import math, time

f = h5py.File("test.h5", "w")
dt_str_vlen = h5py.special_dtype(vlen=str)
ds_ts = f.create_dataset("timestamp",(100,), dtype=h5py.special_dtype(vlen=str))
now = time.time()
sec = int(math.floor(now))
msec = int(round((now-sec)*1000))
ds_ts[0]= time.strftime("%Y-%m-%dT%H:%MZ%S", time.gmtime(sec)) + (".%03d" % msec)
f.close()
