### Why is evtCounter reset at 24 bits?
Try adding below to pgpread.cc LINE 193:
```
            // MONA: why is evtCounter reset at 24 bits?
            uint32_t evtCounter = event_header->evtCounter & 0xffffff;


            if (evtCounter != curr_event_counter + 1) {
                auto evtCntDiff = evtCounter - curr_event_counter;
                printf("PGPReader: Jump in complete l1Count %u -> %u | difference %d \n",
                            curr_event_counter, evtCounter, evtCntDiff);
            }
            curr_event_counter = evtCounter;

            std::this_thread::sleep_for(std::chrono::microseconds(10));
```
The evtCounter seems to get reset at 24 bits even without masking:
```
(daq_20241215) monarin@drp-neh-cmp012 ~ ~/lcls2/psdaq/build/drp/pgpread -d /dev/datadev_0 
setting lane 0, dest 0x0 
setting lane 1, dest 0x100 
setting lane 2, dest 0x200 
setting lane 3, dest 0x300 
setting lane 4, dest 0x400 
setting lane 5, dest 0x500 
setting lane 6, dest 0x600 
setting lane 7, dest 0x700 
device  /dev/datadev_0
dmaCount 2048  dmaSize 262144
PGPReader: Jump in complete l1Count 0 -> 12982989 
Size 32 B | Dest 0.0 | Transition id 2 | pulse id 12189194012205 (2838.76826157) | TimeStamp 56356934025401574  (13121621.959894758) | event counter 12982989 | index 1740
env 021a0001 | payload 00c4c30c 00000063 00000062 00000061 00000060 0000005f
Size 32 B | Dest 0.0 | Transition id 2 | pulse id 12189203602165 (2838.86416117) | TimeStamp 56356980593582896  (13121632.283435824) | event counter 12982990 | index 1741
env 021c0001 | payload 00c4c30d 00000063 00000062 00000061 00000060 0000005f
Size 32 B | Dest 0.0 | Transition id 2 | pulse id 12189206389623 (2838.89203575) | TimeStamp 56356993477831760  (13121635.282782800) | event counter 12982991 | index 1742
env 021e0001 | payload 00c4c30e 00000063 00000062 00000061 00000060 0000005f
PGPReader: Jump in complete l1Count 16777215 -> 0 
Size 32 B | Dest 0.0 | Transition id 2 | pulse id 12189254386983 (2838.137200935) | TimeStamp 56357213192007068  (13121686.953626012) | event counter 12950606 | index 1927
env 021c0001 | payload 01c4448a 00000063 00000062 00000061 00000060 0000005f
PGPReader: Jump in complete l1Count 16777215 -> 0 
PGPReader: Jump in complete l1Count 16777215 -> 0 
PGPReader: Jump in complete l1Count 16777215 -> 0 
PGPReader: Jump in complete l1Count 16777215 -> 0 
PGPReader: Jump in complete l1Count 16777215 -> 0
```
