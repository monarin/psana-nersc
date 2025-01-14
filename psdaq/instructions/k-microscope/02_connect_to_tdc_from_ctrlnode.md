After tdb receives an assigned IP from the dns server installed on the ctl node, we can use the python script below to connect and receive some data from it. 
## Troubleshoot
We had to nudge the cables and the connections inside the tdc box a little (not sure what was loose really) for this to work...

## Python script 
Run this on the ctrl node, note that the IP has to be changed to what is assigned to the tdc. The script also uses PulseIdReceiver.py (available here ~monarin/sw/kmicro/event_receiver_TDC/python).
```
import PulseIdReceiver
import time

# connect to the TDC (*NOTE* change the IP to the one assigned to the tdc)
r = PulseIdReceiver.PulseIdReceiver('192.168.0.150')

# enable the start signal
r.enable()

def printCounters():
    r.disable()
    r.resetCounters()

    r.enable()
    time.sleep(1.0)
    r.disable()
    print("L0 Counter      : " + str(r.countL0()))
    print("Accepted L1     : " + str(r.countL1Accepted()))
    print("Rejected L1     : " + str(r.countL1Rejected()))
    print("Transition      : " + str(r.countTransition()))
    print("Valid           : " + str(r.countValid()))
    print("Trigger         : " + str(r.countTrigger()))
    print("Partition Addr  : " + str(r.partitionAddr()))
    print("Partition Word0 : " + str(r.partitionWord0()))
    print("Pause to trig   : " + str(r.pauseToTrig()))
    print("notPauseToTrig  : " + str(r.notPauseToTrig()))

    print("Ratio Valid / Accepted: " + str(r.countValid() / r.countL1Accepted()))
    r.enable()

# Print all counters
printCounters()

# get the limit of the FIFO (in kB, where the pause signal is activated)
r.get_fifo_limit()

# Get the max. fifo watermark since the last reset
r.get_fifo_max()

```
