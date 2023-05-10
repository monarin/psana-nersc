## Adding new wave8 to TXI and make it available through already commissioning cmp004 node 
### Wave8 installation 
Wave8 takes xpm input and together with its data produce data outputs (PGP 0 and PGP1).  
[ PGP 0 (daq) | PGP 1 (control/ioc) | xpm (in) | unused ].  
![wave8_with_cables](/psdaq/images/wave8_with_cables.png). 
* For TXI wave8, timing is taken from xpm 5 in room 208 via fiber patch (mirror between txi and 208 top patch). 
* Data ports (PGP 0 and 1) are wired back with the same fiber patch to 208 and IOC machine (handled by control). PGP 0 is connected with Long Range cable (to SRCF nodes) and PGP 1 is connected with Short Range cable (only to hutch ioc machine).   
* For PGP 0 (daq data), we connect fiber patch data port in room 208 to the BOS port 1.7.4 and label it as TXI_FIM. 
![ins05_BOS_TXI_Wave8](/psdaq/images/ins05_BOS_TXI_Wave8.png)
This is then cross-linked using the BOS webgui to 5.2.4 DRP-SRCF-CMP004-QSFP1_1 (or lane 5 from 8 lanes counting from 0).
```
     QSFP0_  | QSFP1_
     0 1 2 3   0 1 2 3
LANE 0 1 2 3   4 5 6 7
```
* For PGP 1 (control data), this is done by control staff)

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
### Wave8 devGui
To start the devGui
```
python scripts/wave8DAQ.py --l 5 --enDataPath 0 --startupMode 1
```
Note that currenly my own clone isn't working so have to run this from `/cds/home/c/cpo/git/wave8_2.4.2/software`. The lane (-l) is 5 and the other parameters help sharing the detadev_N resource in case other processes are using the driver too.

Check PgpMon[1] (QSFP1) LinkReady register
![ins05_wave8gui_LinkReady](/psdaq/images/ins05_wave8gui_LinkReady.png)
Check TimingFrameRx RxLinkUp register
![ins05_wave8gui_TimingFrameRx_RxLinkUp](/psdaq/images/ins05_wave8gui_TimingFrameRx_RxLinkUp.png)
### IOC Manager
After PGP 1 connection with IOC machine is established by control staffs, we can view wave8 registers by runninng iocmanager gui from txi hutch.
```
kinit
ssh txi-control -l txiopr
/reg/g/pcds/epics/ioc/txi/pgpWave8/R1.0.0/build/iocBoot/ioc-txi-pgpw8-01/edm-ioc-txi-pgpw8-01.cmd
```
From the iocmanager main and Wave8 diag screens, we can obtain:
* epics_prefix value (top left read TXI:RP:W8:01) that is needed for cnf parameter
* check Up Time to see if this corresponds to what we see on wave8 devGui (in case we're not sure about the correct lane)
![txi_ioc_wave8_main](/psdaq/images/txi_ioc_wave8_main.png)
![txi_ioc_wave8_diag](/psdaq/images/txi_ioc_wave8_diag.png)
### Running Wave8 on daq control
The full working cnf file is available here 


