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
We use Deadtime (or Deadfrac) to identify bottlenecks at each stage in DAQ Pipeline. From daq control gui, Deadtime tab on xpmpva window shows Deadtime on KCU/HSD cards (seems like burst values rather than accumulated over time). This is similar to what we can find on KCU devGui or hsdpva window.  

We can also use daqStats and daqPipes (percentages) to view bottlenecks. From the table, a row represents a detector while a column represents a stage in the pipeline. 

To run daqStats or daqPipes live (getting current values),
```
daqStats -p 0 --inst tmo
daqPipes -p 0 --inst tmo 
```
You can also specify start time to viewed prerecorded values,
```
daqStats -p 0 --inst tmo --start '2020-11-11 13:50:00'
daqPipes -p 0 --inst tmo --start '2020-11-11 13:50:00'
```

daqStats window
![daqStats](/psdaq/images/daqstats.png)
daqPipes window
![daqPipes](/psdaq/images/daqpipes.png)
Navigation: Use > or < and ? for Help




                                                             
