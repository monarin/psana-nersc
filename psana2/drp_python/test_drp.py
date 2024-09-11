from psana import DataSource
from psana.dgramedit import AlgDef, DetectorDef
import sys
import numpy as np

ds=DataSource(drp=drp_info)
thread_num=drp_info.worker_num
print(f"[Python - Thread {thread_num}] - Imports done")

algdef = AlgDef("simplefloat32", 1, 2, 4)
detdef = DetectorDef("floatdet", "justafloat", "float1248")  # detname, dettype, detid
datadef = {
    "valfloat32": (np.float32, 0),
}

det = ds.add_detector(detdef, algdef, datadef)

for run in ds.runs():
    for evt in run.events():
        timestamp = evt.timestamp
        print(
            f"[Python - Thread {thread_num}] Timestamp: {(timestamp >> 32) & 0xffffffff}.{timestamp & 0xffffffff}"
        )
        det.simplefloat32.valfloat32 = np.float32(2023.2)
        ds.adddata(det.simplefloat32)
