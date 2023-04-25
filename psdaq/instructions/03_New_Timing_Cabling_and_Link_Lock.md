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
   ![devgui check timing signal](/psdaq/images/03_devgui_timing_signal.png)
6. Check if data (k-pattern) is received correctly. The k-pattern is used to identify the starting bit. When located correctly, no. of unique k should match what is expected. RxLinkUp should be 0x1 if this pattern is detected correctly.
   ![devgui debugtree check RxLinkUp](/psdaq/images/03_devgui_debugtree_RxLinkUp.png)
   if RxLinkUp is 0x0 (down),
   * Troubleshoot 1 Click Exec on ConfigureXpmMini then Exec on ConfigLclsTimingV2
   * Troubleshoot 2 on xpmvpa below, click TxLinkReset on the matcing columns. These columns are ordered by channel no. (SFP) as appeared on the AMC starting from 0. There are eight SFP channels but the last one is disabled so only seven are functionning.
   For each XPM, you can use xpmpva tool to view the channel
   ```
   xpmpva DAQ:NEH:XPM:5 DAQ:NEH:XPM:6
   ```
   For viewing XPM 5 and 6.
   ![example of xpmvpa tool](/psdaq/images/ex-xpmvpa_xpm5_amc0.png)
## TimingTxReset on Wave8 Gui
Another place that might help fixing link lock problem is from resetting TimingTxReset on Wave8 gui.
![wave8_gui_TimingTxReset](/psdaq/images/wave8_gui_TimingTxReset.png)
