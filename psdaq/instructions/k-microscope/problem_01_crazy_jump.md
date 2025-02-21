### Running kmicro at high rate (>1kHz) shows crazy jump
The error appears after running for a few seconds (from the kmicroscope daq log file):
```
PGPReader: Aborting on crazy jump in event counter
```
This seems to come from buffer counts and size settings in tdetsim.service. Currently, we need to use the following settings in tdetsim.service on drp-neh-cmp012:
```
ExecStart=/sbin/insmod /usr/local/sbin/datadev.ko cfgTxCount=4 cfgRxCount=130816 cfgSize=4096 cfgMode=0x2
```
This is rougly 500MB. Note that increasing cfgRxCount to 1048572 (similar to other nodes) causes pgpread on drp-neh-cmp012 to fail with this error:
```
Failed to map dma buffers: Cannot allocate memory
```
