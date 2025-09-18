### Symptoms
Sometimes the epix10ka 1kHz doesn't start up. Running devGui or initializing from the DAQ shows this error:
```
General Error: Transaction error for block Top.AxiVersion.FpgaVersion with address 0x00000000. Error Timeout waiting for register transaction 2671 message response.
Traceback (most recent call last):
  File "/cds/sw/ds/ana/conda2/inst/envs/daq_20250402/lib/python3.9/site-packages/pyrogue/_Variable.py", line 1252, in get
    self._parent.checkBlocks(recurse=False, variable=self)
```
### Fix
Restart the DAQ (once/twice) fixes it.
