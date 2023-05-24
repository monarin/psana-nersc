## DAQ Pipeline 
From the KCU cards (or any other interface e.g. HSD cards), data flow from one memory buffer to another. 
This note shows different steps and memory buffers involved until data are delivered to shmem or file system.
```
                    | --> Worker 1 [Worker Memory] --> |
KCU/HSD Cards   --> | --> Worker 2 [Worker Memory] --> | --> off node -->  DISK/SHMEM  
[Card Memory]       |                                  |      |   ^  
                    | --> Worker N [Worker Memory] --> |      v   |  
                                                               TEB
```
## Deadtime
Deadtime: the fraction of time the the memory buffer is full.  
Deadfrac: the fraction of L1Accepts that were lost (due to full buffer).  
We use Deadtime (or Deadfrac) to identify bottlenecks at each stage in DAQ Pipeline. 
                                                             
