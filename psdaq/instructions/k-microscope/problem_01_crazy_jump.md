### Running kmicro at high rate (>1kHz) shows crazy jump (*FIXED* see below)
The error appears after running for a few seconds (from the kmicroscope daq log file):
```
PGPReader: Aborting on crazy jump in event counter
```
## Another unrelated problem (not able to allocate > 500MB dma memory)
Currently, we need to use the following settings in tdetsim.service on drp-neh-cmp012:
```
ExecStart=/sbin/insmod /usr/local/sbin/datadev.ko cfgTxCount=4 cfgRxCount=130816 cfgSize=4096 cfgMode=0x2
```
This is rougly 500MB. Note that increasing cfgRxCount to 1048572 (similar to other nodes) causes pgpread on drp-neh-cmp012 to fail with this error:
```
Failed to map dma buffers: Cannot allocate memory
```
This problem might come from fragmented memory issue on this drp-neh-cmp012. Running buddyinfo show only a few high-order page size (right columns) counts:
```
(daq_20241215) monarin@drp-neh-cmp012 ~ cat /proc/buddyinfo
Node 0, zone      DMA      1      1      0      0      2      1      1      0      1      1      3 
Node 0, zone    DMA32    119    102     22     34     58     35     23     14     18      3    327 
Node 0, zone   Normal    263     50     24    537    701    329    264    187    138     36  22637 
Node 1, zone   Normal    777    209     68    265    442    269    200    124     76     65  23236
```
## The fix
Read buffer overwrite protection mechanism on debugging daq page for backpressure and deadtime for all the buffers. For overview,
```
Pebble buffer <--> DMA buffer <--> FPGA buffer <--> Front-end buffer (Timing)
```
Essentially, at pebble or DMA buffer level, when the consumer is slow this should backpressure (eventually) onto the XPM, which should cause deadtime. When the XPM is dead, no more triggers will be send allowing the pebble/DMA to be flushed out correctly causing no buffer overwrites.  
The problem came from the fact that LinkGroupMask on XPMPVA for AMC0 Lane 2 (TDetSim of neh-cmp012) is not set to listen to Group 0 (it was set to None). 
