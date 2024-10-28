## Adding more XPM Timing cables to the BOS
1. Locate which XPM would be used - [see XPM Tree](https://confluence.slac.stanford.edu/display/PSDMInternal/Debugging+DAQ#DebuggingDAQ-XPM) for linking level. Note that each step adds extra delay that needs to be programmed.
2. Locate available AMC (upside down)
   |      AMC 1      |       AMC 0     |
   | x 6 5 4 3 2 1 0 | x 6 5 4 3 2 1 0 |  FSP ID counting from 0 from the left
   Each AMC has 8 channels but the last channel is not available.
4. Wire the optic cable from the seleted channel on one of the AMCs to the LEFT side (detector/timing sides with lower numbers) of the BOS.
5. Wire the MPO breakout (usually used) cable from the BOS RIGHT side (4 port pairs) to the available patch panel (mirrored to SRCF). We need to document this in the [SRCF cable confluence page](https://confluence.slac.stanford.edu/display/PSDMInternal/SRCF+Fiber+Cabling) because this is unknown from the BOS. 
6. Wire (go to SRCF) the patch panel with MPO breakout cable to the node(s). 
7. Use the BOS webgui to add a new Cross Connect that links the chosen timing BOS port to the desired srcf node (the right side of the BOS). 
8. Check light level
    * Check if light is received using the devGui (Note that for timing-only node, there's no devGui so we can only use the BOS to check the light level).
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

## TimingTxReset on Wave8 Gui
Another place that might help fixing link lock problem is from resetting TimingTxReset on Wave8 gui.
![wave8_gui_TimingTxReset](/psdaq/images/wave8_gui_TimingTxReset.png)
