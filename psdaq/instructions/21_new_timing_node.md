## Setting up a new Timing node
Below show how to setup a new timing node at the FEE test stand. The new timing node is drp-neh-cmp012 and it's connected 
to xpm 10 amc 0 port 2 (counting from 0)
### Check KCU firmware
The kcu firmware must be up-to-date. In this case, the working node is drp-neh-cmp002 and its values are
```
monarin@drp-neh-cmp002 ~ cat /proc/datadev_0
---------- Firmware Axi Version -----------
     Firmware Version : 0x5000000
           ScratchPad : 0x0
        Up Time Count : 4291
             Git Hash : 4a82bda096aff08407f49ff1075bdafba89df6b1
            DNA Value : 0x00000000000000000000000000000000
         Build String : DrpTDet: Vivado v2023.1, rdsrv301 (Ubuntu 20.04.6 LTS), Built Thu 05 Sep 2024 03:58:09 PM PDT by weaver
...
```
If the new timing node doesn't show these values, we'll need to update the firmware image. The command is:
```
(daq_20241215) monarin@drp-neh-cmp012 software python scripts/updatePcieFpga.py --path ~weaver/mcs/drp --dev /dev/datadev_0
```
Note that this update needs Rogue and it has to match with the current version running on the node. 
If you see the error below, 
```
(daq_20241215) monarin@drp-neh-cmp012 software python scripts/updatePcieFpga.py --path ~weaver/mcs/drp --dev /dev/datadev_0
Rogue/pyrogue version v6.1.3. https://github.com/slaclab/rogue
Basedir = /cds/home/p/psrel/git/pgp-pcie-apps/firmware/submodules/axi-pcie-core/scripts
Traceback (most recent call last):
  File "/cds/home/p/psrel/git/pgp-pcie-apps/software/scripts/updatePcieFpga.py", line 103, in <module>
    memMap = rogue.hardware.axi.AxiMemMap(args.dev)
rogue.GeneralError: AxiMemMap::AxiMemMap: General Error: Bad kernel driver version detected. Please re-compile kernel driver.
       Note that aes-stream-driver (v5.15.2 or earlier) and rogue (v5.11.1 or earlier) are compatible with the 32-bit address API.       To use later versions (64-bit address API),, you will need to upgrade both rogue and aes-stream-driver at the same time to:
       		aes-stream-driver = v5.16.0 (or later)
		rogue = v5.13.0 (or later)
```
1. You'll need to find the right version of Rogue that was used to install the current firmware image. 
You can do this buy looking at 
```
conda env list
```
and try to look for the older env with the older Rogue.  
2. Use the right version of cameralink_gateway for running the updatePcieFpga.py (above), the available versions are:
```
ls ~cpo/git/cameralink-gateway-*
```
### Check datadev driver
It's also likely that the node will have the old version of datadev.ko, kcuSim, kcuStatus, and tdetsim. Copy them from /usr/local/sbin/ on the current working node. 
### Troubleshoot
* If kcuSim -s shows lDown = 1, you may need to run kcuSim -t, kcuSim -T
* Check FSP lights on xpmpva, QSFP might be broken is the light levels are abnormal.
* Enable lanes with kcuSim -C 0,0,0xff, if running below command doesn't show any transitions when sending it from groupca.
```
(daq_20241215) monarin@drp-neh-cmp012 ~ ~/lcls2/psdaq/build/drp/pgpread -d /dev/datadev_1
setting lane 0, dest 0x0 
setting lane 1, dest 0x100 
setting lane 2, dest 0x200 
setting lane 3, dest 0x300 
setting lane 4, dest 0x400 
setting lane 5, dest 0x500 
setting lane 6, dest 0x600 
setting lane 7, dest 0x700 
device  /dev/datadev_1
dmaCount 4100  dmaSize 2162688
Size 288 B | Dest 1.0 | Transition id 2 | pulse id 9066576779782 (2110.4195785222) | TimeStamp 41919516993541617  (9760148.529421809) | event counter 32 | index 132
env 02000001 | payload 00000000 00000000 00000000 00000000 00000000 00000000
Size 288 B | Dest 2.0 | Transition id 2 | pulse id 9066576779782 (2110.4195785222) | TimeStamp 41919516993541617  (9760148.529421809) | event counter 32 | index 133
env 02000001 | payload 00000000 00000000 00000000 00000000 00000000 00000000
Size 288 B | Dest 3.0 | Transition id 2 | pulse id 9066576779782 (2110.4195785222) | TimeStamp 41919516993541617  (9760148.529421809) | event counter 32 | index 134
env 02000001 | payload 00000000 00000000 00000000 00000000 00000000 00000000
Size 288 B | Dest 0.0 | Transition id 2 | pulse id 9066576779782 (2110.4195785222) | TimeStamp 41919516993541617  (9760148.529421809) | event counter 32 | index 135
env 02000001 | payload 00000000 00000000 00000000 00000000 00000000 00000000
```
