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
To start the devGui, make sure that rogue matches with the firmware. As of 20250409, we need Rogue/pyrogue version v5.18.4 from ps-4.6.0.
```
ssh drp-srcf-cmp004
cd wave8/software
python scripts/PcieDebugGui.py --boardType XilinxKcu1500
```
For Optic, check the value of RxPower[1] of Qsfp[1] on Kcu1500
![ins05_devgui_kcu1500_QSFP1_1](/psdaq/images/ins05_devgui_kcu1500_QSFP1_1.png)
For linklock, check Lane 5 (QSFP1_1 corresponds to lane 5 of the 8 lanes on KCU). 
The LinkReady register should show True for both RxStatus and TxStauts. 
![ins05_devGui_kcu1500_Lane5_LinkReady](/psdaq/images/ins05_devGui_kcu1500_Lane5_LinkReady.png)
### Wave8 devGui
To start the devGui, we need rogue version 6.1.1. Also, firmware/python/wave8/Top.py should have raise firmware verion check commented out!
```
python scripts/wave8DAQ.py --l 5 --enDataPath 0 --startupMode 1
```
Note that currenly my own clone isn't working so have to run this from `/cds/home/c/cpo/git/wave8_2.4.2/software`. The lane (-l) is 5 and the other parameters help sharing the detadev_N resource in case other processes are using the driver too.

Check PgpMon[1] (QSFP1) LinkReady register
![ins05_wave8gui_LinkReady](/psdaq/images/ins05_wave8gui_LinkReady.png)
Check TimingFrameRx RxLinkUp register
![ins05_wave8gui_TimingFrameRx_RxLinkUp](/psdaq/images/ins05_wave8gui_TimingFrameRx_RxLinkUp.png)
To locate remote id (RxId)
![ins05_wave8_devgui_remoteid](/psdaq/images/ins05_wave8_devgui_remoteid.png)
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
Before running the daq, check that Trigger Delay (ns) or start_ns is correct on the IOC. It should be 99.884k
![ins05_ioc_wave8_start_ns](/psdaq/images/ins05_ioc_wave8_start_ns_99k.png)

The full working cnf file is available here [mona.cnf](https://github.com/slac-lcls/lcls2/blob/dd2850ab95602c3ce772197e74cc0d85cbf30c5a/psdaq/psdaq/cnf/mona.cnf). The line which adds wave8 is
```
{host: 'drp-srcf-cmp004', id:'txi_fim1_0',  flags:'spu', env:epics_env, cmd:drp_cmd0+' -l 0x20 -D wave8 -k epics_prefix=TXI:RP:W8:01'}
```
To access daq-contol,
```
ssh drp-srcf-mon001
cd /path/to/cnf/mona.cnf
procmgr start mona.cnf
```
### Troubleshoots
#### Gateway issue from daq-control
Error:
```
Rogue/pyrogue version v5.16.0. https://github.com/slaclab/rogue^M
--- lanemask 20  lane 5  timebase 186M ---^M
ctxt_put [['TXI:RP:W8:01:Top:TriggerEventManager:TriggerEventBuffer[0]:MasterEnable']] [[0]]^M
ctxt_put [['TXI:RP:W8:01:Top:SystemRegs:timingUseMiniTpg', 'TXI:RP:W8:01:Top:TimingFrameRx:ModeSelEn', 'TXI:RP:W8:01:Top:TimingFrameRx:ModeSel', 'TXI:RP:W8:01:Top:TimingFrameRx:ClkSel', 'TXI:RP:W8:01:Top:TimingFrameRx:RxPllReset']] [[0, 1, 1, 1, 1]]^M
ctxt_put [['TXI:RP:W8:01:Top:TimingFrameRx:RxPllReset']] [[0]]^M
ctxt_put [['TXI:RP:W8:01:Top:TimingFrameRx:RxDown']] [[0]]^M
ctxt_put [['TXI:RP:W8:01:Top:SystemRegs:timingUseMiniTpg', 'TXI:RP:W8:01:Top:TimingFrameRx:ModeSelEn', 'TXI:RP:W8:01:Top:TimingFrameRx:ModeSel', 'TXI:RP:W8:01:Top:TimingFrameRx:ClkSel', 'TXI:RP:W8:01:Top:TimingFrameRx:RxPllReset']] [[0, 1, 1, 1, 1]]^M
ctxt_put [['TXI:RP:W8:01:Top:TimingFrameRx:RxPllReset']] [[0]]^M
ctxt_put [['TXI:RP:W8:01:Top:TimingFrameRx:RxDown']] [[0]]^M
ctxt_put [TXI:RP:W8:01:Top:TriggerEventManager:XpmMessageAligner:TxId] [4194342937]^M
ctxt_put [TXI:RP:W8:01:Top:TriggerEventManager:TriggerEventBuffer[0]:MasterEnable] [0]^M
Traceback (most recent call last):^M
  File "/cds/home/m/monarin/lcls2/psdaq/psdaq/configdb/wave8_config.py", line 169, in wave8_connect^M
    values = int(ctxt_get(epics_prefix+':Top:TriggerEventManager:XpmMessageAligner:RxId'))^M
TypeError: int() argument must be a string, a bytes-like object or a number, not 'NoneType'^M
tst-drp[986]: <C> **** python error^M
```
Some answers from chris:
Yes, I can see that issue from the command line:
```
(ps-4.5.26) drp-srcf-cmp004:software$ pvget TXI:RP:W8:01:Top:TriggerEventManager:XpmMessageAligner:RxId
Timeout
```
But it works for a rix fim:
```
(ps-4.5.26) drp-srcf-cmp004:software$ pvget RIX:FIM:W8:03:Top:TriggerEventManager:XpmMessageAligner:RxId
RIX:FIM:W8:03:Top:TriggerEventManager:XpmMessageAligner:RxId 2023-05-09 16:20:04.966  4281493252 
(ps-4.5.26) drp-srcf-cmp004:software$ 
```
I can make it work by setting this additional environment variable which tells epics to talk directly to the IOC node:
```
(ps-4.5.26) drp-srcf-cmp004:software$ export EPICS_PVA_ADDR_LIST=172.21.136.41
(ps-4.5.26) drp-srcf-cmp004:software$ pvget TXI:RP:W8:01:Top:TriggerEventManager:XpmMessageAligner:RxId
TXI:RP:W8:01:Top:TriggerEventManager:XpmMessageAligner:RxId 2023-05-09 16:24:33.896  4283525129 
(ps-4.5.26) drp-srcf-cmp004:software$ 
```
I think that means we need to get the controls group to modify some epics gateway settings.  I’ll cc you on the slack thread. (edited) 
Solution: gateway has an incorrect permission. Zach reset it and we can run wave8 from daq control.
#### IOC Connection Fail
There was an issue when trying to open IOCManager after PGP 1 is connected to the IOC host. We could see optic signals from wave8 devGui. I think the issue was resolved with the firmware update (see thread between Jyoti and chis). 
