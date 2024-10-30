import os

import numpy as np

# This `batch_size` should be set to a small number (e.g. 1)
# since all other events which are part of this intg. event will be sent
# in the same batch.
os.environ["PS_SMD_N_EVENTS"] = "1"

from psana import DataSource

ds = DataSource(
    exp="rixx1003721",
    run=171,
    intg_det="andor_vls",
)
run = next(ds.runs())
hsd = run.Detector("hsd")
andor = run.Detector("andor_vls")

# Test calculating sum of the hsd for each integrating event.
sum_hsd = 0
for i_evt, evt in enumerate(run.events()):
    hsd_peaks = hsd.raw.waveforms(evt)[0][0]
    if hsd_peaks is None:
        continue
    andor_val = andor.raw.value(evt)

    # Keep summing the value of the other detector (hsd in this case)
    sum_hsd += np.sum(hsd_peaks[:]) / np.prod(hsd_peaks.shape)

    # When an integrating event is found, print out and reset the sum variable
    if andor_val is not None:
        val_andor = np.sum(andor_val[:]) / np.prod(andor_val.shape)
        print(f"i_evt: {i_evt} andor: {val_andor} sum_hsd:{sum_hsd}")
        sum_hsd = 0
