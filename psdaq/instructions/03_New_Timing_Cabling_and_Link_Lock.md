## Adding more XPM Timing cables to the BOS
1. Locate which XPM would be used - [see XPM Tree](https://confluence.slac.stanford.edu/display/PSDMInternal/Debugging+DAQ#DebuggingDAQ-XPM) for linking level. Note that each step adds extra delay that needs to be programmed.
2. Locate available AMC 
   |   AMC 1    |    AMC 0   |
   Each AMC has 8 channels but the last channel is not available.
   For each XPM, you can use xpmpva tool to view the channel
   ```
   xpmpva DAQ:NEH:XPM:5 DAQ:NEH:XPM:6
   ```
   For viewing XPM 5 and 6.
