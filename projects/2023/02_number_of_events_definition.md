## Definition of no. of events parameters
```
max_events  smd0 ----------------> eb0 ------------> bd0
                                       ------------> bd1
                 ----------------> eb1 ------------> bd2
                                       ------------> bd3
                  PS_SMD_N_EVENTS       batch_size
```
Parameter definitions:
- max_events: Maximum number of L1Accept events that smd0 reads
- PS_SMD_N_EVENTS: (Environment variable): No. of L1Accept events that smd0 send to one eb at a time.
- batch_size: No. of events that eb send to one bd at a time (Note that this can only be a number smaller than PS_SMD_N_EVENTS)

For integrating detector run, these numbers are calculated from the integrating detector.
