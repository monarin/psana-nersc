## Adding new wave8 to TXI and make it avaiable through already commissioning cmp004 node 
### Wave8 installation 
Wave8 takes xpm input and together with its data produce one data output.  
[ data (out) | unused | xpm (in) | unused ].  
For TXI, xpm is taken from 208 via fiber patch (mirror between txi and 208 top patch). Data is wired back with the same fiber patch to 208. 
We then connect fiber patch data port to the BOS port 1.7.4 and label it as TXI_FIM. This is then cross-linked using the BOS webgui so TXI
wave 8 is connected to cmp004_QSFP1_1.

We can check the optic signal on the BOS. 
![ins05_BOS_TXI_Wave8](/psdaq/images/ins05_BOS_TXI_Wave8.png)
## Checking the optic signal and linklock using Wave8 devGui
Wave8 devGuis installation:
```
$ git clone --recursive git@github.com:slaclab/wave8
```
When checkout a different version, also udpate submodules:
```
$ git submodule update --recursive
```
We can use either Kcu1500 or Wave8 devGui to check for optic signal and linklock.
### Kcu1500 devGui
To start the devGui
```
ssh drp-srcf-cmp004
cd wave8/software
python scripts/PcieDebugGui.py --boardType Kcu1500
```
For Optic, check the value of RxPower[1] of Qsfp[1] on Kcu1500
![ins05_devgui_kcu1500_QSFP1_1](/psdaq/images/ins05_devgui_kcu1500_QSFP1_1.png)
For linklock, check Lane 5 (QSFP1_1 corresponds to lane 5 of the 8 lanes on KCU). 
The LinkReady register should show True for both RxStatus and TxStauts. 
![ins05_devGui_kcu1500_Lane5_LinkReady](/psdaq/images/ins05_devGui_kcu1500_Lane5_LinkReady.png)






