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
### Enable all lanes with kcuSim
To enable one or more lanes provided by the kcu firmware, run
```
kcuSim -C 0,0,0xff  # -C partition (group), length (of the fake data, 0 for none), 0xff = 11111111 for all 8 lanes
```
Check with kcuSim -s
```
monarin@drp-neh-cmp001 ~ kcuSim -s
-- Core Axi Version --
  firmware version  :  5000000
  scratch           :  0
  uptime count      :  5295239
  build string      :  DrpTDet: Vivado v2023.1, rdsrv301 (Ubuntu 20.04.6 LTS), Built Thu 05 Sep 2024 03:58:09 PM PDT by weaver
00000004 00000001 00000000 00000000 0ee6b280 00000001 20020000 28200408
07735c41 0000000d 00000000 00000000 00000000 00000000 00000000 00000000
00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000
00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000
00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000
00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000
00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000
00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000
TxRefClk: 185.734272 MHz
RxRecClk: 185.733904 MHz
  lanes             :  4
  monEnable         :  0

-- migLane Registers --
         blockSize          4        4        4        4
         blocksPause       3f       3f       3f       3f
         blocksFree       1ff      1ff      1ff      1ff
         blocksQued         0        0        0        0
         writeQueCnt       a4       10       65       55
         wrIndex           a4       10       65       55
         wcIndex           a4       10       65       55
         rdIndex           a4       10       65       55
         axilOther   125.000000 MHz [locked]
         timingRef   185.713000 MHz [locked]
         migA        200.001000 MHz [locked]
         migB        200.001000 MHz [locked]
              length        0        0        0        0
               clear        0        0        0        0
              enable        1        1        1        1
        messagedelay        1       62        b       5b        b        b       5b        b
             localid fb009c15
            remoteid ff0b5407
              enable        1        1        1        1        0        0        0        0
               group        0        0        0        0        0        0        0        0

```
* NOTE that datadev_0 is the right 4 columns and datadev_1 is the left 4 columns.
