## Symptom: split on None traceback. 
Root cause: Detector disconnected. 


## Daq Monitoring:  
[TMO and Rix Monitoring](https://confluence.slac.stanford.edu/display/LCLSIIData/psdaq#psdaq-DAQMonitoring)
Symptom: 
1. shows two opal completey dead. 
2. xpmpva > deadtime tab > two opals show 1 (cmp026 and cmp011)
3. check tmo.cnf for aliases 

## HSD Cards
HSD Machine has 8 PCI slots for HSD cards. Each card has two channels. In the cnf file, the notation fot this in -k option is seen as xxxxxxxx3D-A and xxxxxxxx3D-B for one 3D card with A and B channels.

## Parameter gate_ns could be causing failures
1MHz Camera, each image is 1 microsec (exposure time, gate_ns in daq control)
HSD Camera is fancy, images can overlap. 

## Deadtime raised 
After running for a while, we crashed with some detectors showing deadtime 1. From the log file, it looks like the eventbuilder was trying to build SlowUpdate from contributors but it couldn't.
```
tmo-teb[7266]: <W> Fixup SlowUpdate, 0072c1474e07bf, size 0, source 0^M
tmo-teb[7266]: <W> Fixup SlowUpdate, 0072c1474e07bf, size 0, source 5^M
Timed-out       SlowUpdate 0072c1474e07bf, size     0, for  remaining 0000000000000021, RoGs 0003, contract 00000000000007ff, age 12073 ms, tmo 12000 ms^M
```

remaining shows drp_ids (bit mask) that are not coming in. In this case, bit 0 and bit 5 (in hex this is 0000000000000021). Note `contract` shows no. of expected contributors (00000000000007ff) = 11.
