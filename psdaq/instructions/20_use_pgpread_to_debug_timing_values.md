## Schematic of timing node
```
                                                              drp-neh-cmp001
[ xpm 11 amc 1 port 0 ] --> (4 lanes fiber pair) --> [ kcu bus a datadev_0 --- lane 0 ] *         
                                                                           --- lane 1
                                                                           --- lane 2
                                                                           --- lane 3
                                                           bus b datadev_1 --- lane 4 (second b might not exists)
                                                                           --- lane 5
                                                                           --- lane 6
                                                                           --- lane 7
* lanes splitted by sw, each lane has 4 virtual channels (vc)
```
For detectors, the input 4 lanes fiber pair are mapped to either datadev_0 or _1 directly (with virtual channels controlled by detector settings).
## Use pgpread to check values from the xpm
Run groupca for xpm11 group 0,
```
groupca DAQ:NEH 11 0
```
Run pgpread on the timing node,
```
monarin@drp-neh-cmp001 ~ ~/lcls2/psdaq/build/drp/pgpread -d /dev/datadev_1
```
In groupca > Transitions tab, click Configure a few times. You should see the transition for each lane.
```
monarin@drp-neh-cmp001 ~ ~/lcls2/psdaq/build/drp/pgpread -d /dev/datadev_1
setting lane 0, dest 0x0 
setting lane 1, dest 0x100 
setting lane 2, dest 0x200 
setting lane 3, dest 0x300 
setting lane 4, dest 0x400 
setting lane 5, dest 0x500 
setting lane 6, dest 0x600 
setting lane 7, dest 0x700 
device  /dev/datadev_1
dmaCount 1048576  dmaSize 4096
Size 288 B | Dest 1.0 | Transition id 2 | pulse id 7873554013149 | event counter 4 | index 105706
env 02080001 | payload 00000000 00000000 00000000 00000000 00000000 00000000
Size 288 B | Dest 2.0 | Transition id 2 | pulse id 7873554013149 | event counter 4 | index 105696
env 02080001 | payload 00000000 00000000 00000000 00000000 00000000 00000000
Size 288 B | Dest 3.0 | Transition id 2 | pulse id 7873554013149 | event counter 4 | index 105679
env 02080001 | payload 00000000 00000000 00000000 00000000 00000000 00000000
Size 288 B | Dest 0.0 | Transition id 2 | pulse id 7873554013149 | event counter 4 | index 105675
env 02080001 | payload 00000000 00000000 00000000 00000000 00000000 00000000
Size 288 B | Dest 1.0 | Transition id 2 | pulse id 7873559635463 | event counter 5 | index 105684
env 020a0001 | payload 00000000 00000000 00000000 00000000 00000000 00000000
Size 288 B | Dest 2.0 | Transition id 2 | pulse id 7873559635463 | event counter 5 | index 105682
env 020a0001 | payload 00000000 00000000 00000000 00000000 00000000 00000000
Size 288 B | Dest 3.0 | Transition id 2 | pulse id 7873559635463 | event counter 5 | index 105817
env 020a0001 | payload 00000000 00000000 00000000 00000000 00000000 00000000
Size 288 B | Dest 0.0 | Transition id 2 | pulse id 7873559635463 | event counter 5 | index 105812
env 020a0001 | payload 00000000 00000000 00000000 00000000 00000000 00000000
```
