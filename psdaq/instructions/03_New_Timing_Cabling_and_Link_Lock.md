## Adding more XPM Timing cables to the BOS
1. Locate which XPM would be used - [see XPM Tree](https://confluence.slac.stanford.edu/display/PSDMInternal/Debugging+DAQ#DebuggingDAQ-XPM) for linking level. Note that each step adds extra delay that needs to be programmed.
2. Locate available AMC 
   |   AMC 1    |    AMC 0   |
   Each AMC has 8 channels but the last channel is not available.
3. Wire the optic cable from the seleted channel on one of the AMCs to the right side (detector/timing sides with lower numbers) of the BOS.
4. Use the BOS webgui to add a new Cross Connect that links the chosen timing BOS port to the desired srcf node (the right side of the BOS). 
5. Check if light is received using the devGui
   ```
   python scripts/devGui --pgp4 0 --laneConfig 1=Piranha4 --pcieBoardType Kcu1500 --enLclsII 1 --enableConfig 1 --startupMode 1
   ```
   
   For each XPM, you can use xpmpva tool to view the channel
   ```
   xpmpva DAQ:NEH:XPM:5 DAQ:NEH:XPM:6
   ```
   For viewing XPM 5 and 6.
   ![example of xpmvpa tool](/psdaq/images/ex-xpmvpa_xpm5_amc0.png)
