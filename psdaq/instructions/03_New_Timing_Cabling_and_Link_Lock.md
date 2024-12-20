## Adding more XPM Timing cables to the BOS
1. Locate which XPM would be used - [see XPM Tree](https://confluence.slac.stanford.edu/display/PSDMInternal/Debugging+DAQ#DebuggingDAQ-XPM) for linking level. Note that each step adds extra delay that needs to be programmed. Room 208 XPMs:
   ```
   network switch on bottom: slot 1
   xpm0: slot 2
   xpm5: slot 4
   xpm6: slot 5
   hxr xpm: slot 7 (fed from lcls1 timing in the back 2 racks down)
   ```
2. Locate available AMC (upside down)
   ```
   |      AMC 1      |       AMC 0     |
   | x 6 5 4 3 2 1 0 | x 6 5 4 3 2 1 0 |  FSP ID counting from 0 from the right
   ```
   Each AMC has 8 channels but the last channel is not available.
3. Wire the optic cable from the seleted channel on one of the AMCs to the LEFT side (detector/timing sides with lower numbers) of the BOS.
4. Wire the MPO breakout (usually used) cable from the BOS RIGHT side (4 port pairs) to the available patch panel (mirrored to SRCF). We need to document this in the [SRCF cable confluence page](https://confluence.slac.stanford.edu/display/PSDMInternal/SRCF+Fiber+Cabling) because this is unknown from the BOS. 
5. Wire (go to SRCF) the patch panel with MPO breakout cable to the node(s). 
6. Use the BOS webgui to add a new Cross Connect that links the chosen timing BOS port to the desired srcf node (the right side of the BOS). 
7. Check light level
    * Use the BOS (all nodes)
      * If In or Out shows -90, check if cable is swapped (this could be anywhere in the connections). You have to go through XPM, the BOS, or the srcf node and swap the fiber cable. If the swap is done correctly, you should see the correct light level ~10 < -1.
    * Use devGui (only data/timing node) 
   ```
   python scripts/devGui --pgp4 0 --laneConfig 1=Piranha4 --pcieBoardType Kcu1500 --enLclsII 1 --enableConfig 1 --startupMode 1
   ```
   ![devgui check timing signal](/psdaq/images/03_devgui_timing_signal.png)
    * Check if data (k-pattern) is received correctly. The k-pattern is used to identify the starting bit. When located correctly, no. of unique k should match what is expected. RxLinkUp should be 0x1 if this pattern is detected correctly.
   ![devgui debugtree check RxLinkUp](/psdaq/images/03_devgui_debugtree_RxLinkUp.png)
   if RxLinkUp is 0x0 (down),
      * Troubleshoot 1 Click Exec on ConfigureXpmMini then Exec on ConfigLclsTimingV2
      * Troubleshoot 2 on xpmvpa below, click TxLinkReset on the matcing columns. These columns are ordered by channel no. (SFP) as appeared on the AMC starting from 0. There are eight SFP channels but the last one is disabled so only seven are functionning.
    * For each XPM, you can use xpmpva tool to view the channel (the name of the device will only shows up once configured by the DAQ).
   ```
   xpmpva DAQ:NEH:XPM:5 DAQ:NEH:XPM:6
   ```
   For viewing XPM 5 and 6.
   ![example of xpmvpa tool](/psdaq/images/ex-xpmvpa_xpm5_amc0.png)
8. Install firmware (see seperate instruction) and copy tdetsim.service from a similar timing node if necessary. 

## TimingTxReset on Wave8 Gui
Another place that might help fixing link lock problem is from resetting TimingTxReset on Wave8 gui.
![wave8_gui_TimingTxReset](/psdaq/images/wave8_gui_TimingTxReset.png)
