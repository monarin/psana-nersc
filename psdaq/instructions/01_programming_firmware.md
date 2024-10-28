## Wave8/FIM 
### KCU1500
- MCS files: https://github.com/slaclab/pgp-pcie-apps/releases/tag/v2.5.0 (kcu1500 firmware that "only receive" data).
  see the update instruction in the KCU1500 Data section below.
## Opal/piranha (Camera-link gateway)
### FEB (front-end-board or the black box)
- Get the firmware from https://github.com/slaclab/cameralink-gateway/releases/tag/v8.2.3
- On the node where Opal is installed, from cameralink-gateway repo, run
  ```
  python software/scripts/updateFebFpga.py --mcs ~/ClinkFebPgp2b_1ch-0x02000000-20191210103130-ruckman-d6618cc.mcs --lane 0 --pgp4 0
  ```
  Note* replace the above .mcs file with the downloaded one
  Note** lane can be determined from .cnf file
### KCU1500 Data (datadev_0)
- MCS files: https://github.com/slaclab/lcls2-pgp-pcie-apps (kcu1500 that take timing and data). 
1. On psbuild-rhel7 or any other nodes with internet access, wget both the primary and secondary mcs files of the requested version from the above repo.
2. Logon to the node with the KCU1500 (that you wish to program)
3. Check the current version:
```
cat /proc/datadev_0       # or datadev_1
```
4. Run update script - this assumes you already clone cameralink-gateway, see cloning instruction [here](https://docs.google.com/presentation/d/1zXggROZ05NY4N3eIyy0ydyl0WuofBa2jR7cAse2rPz4/edit?usp=sharing)
```
cd ~/cameralink-gateway   
python software/scripts/updatePcieFpga.py --path $HOME/Downloads     # where path is where the mcs files are
```
**Note** If there are two datadev_ (0 and 1), add `--dev /dev/datadev_1`. See full instruction [here](https://confluence.slac.stanford.edu/display/PSDMInternal/Debugging+DAQ#DebuggingDAQ-Opal).
5. Power reset node
### KCU1500 Timing System (datadev_1)
1. On the node that needs update, source setup_env.sh and go to:
```
cd /cds/home/p/psrel/git/pgp-pcie-apps/software
python scripts/updatePcieFpga.py --path ~weaver/mcs/drp --dev /dev/datadev_1
```
2. Copy the new kcuSim from locally built lcls2 to the local folder on the node
```
sudo cp ~/lcls2/install/bin/kcuSim /usr/local/sbin/
```
3. Reboot the node
4. To check the version and whether the new firmware is working
```
monarin@drp-srcf-cmp028 ~ kcuSim -s
-- Core Axi Version --
  firmware version  :  4000300
  scratch           :  0
  uptime count      :  4608
  build string      :  DrpTDet: Vivado v2022.1, rdsrv301 (Ubuntu 20.04.6 LTS), Built Thu 25 Jan 2024 09:19:24 AM PST by weaver
```
linkUp should be 1 and remoteId should be correct.
### XPM
Step 0: Check the version of XPM firmware:
```
ssh psdev
source /cds/sw/package/IPMC/env.sh
amcc_dump_bsi --all <AMCc address>
```
where AMCc address is the rack that hosts the XPMs. The list of AMCc addresses and available slots (in parentheses):
1. shm-neh-daq01 (slot1: Network, slot2: XPM0, slot3: None, slot4: XPM5, slot5: XPM6, slot6: None,   slot7: hxr XPM) 
2. shm-tmo-daq01 (slot1: Network, slot2: None, slot3: XPM2, slot4: None, slot5: XPM4, slot6: fanout, slot7: fanout)
3. shm-rix-daq01 (slot1: Network, slot2: XPM1, slot3: XPM3, slot4: None, slot5: None, slot6: fanout, slot7: None)
4. shm-fee-daq01 (slot1: Network, slot2: XPM10,slot3: None, slot4: XPM11,slot5: None, slot6: None,   slot7: None)

The dump shows what type of xpm mcs file is needed. As of 20240202, the following shows xpm and its firmware version:
```
XPM0: xpm
XPM1: xpm_noRTM
XPM2: xpm
XPM3: xpm
XPM4: xpm_noRTM
XPM5: xpm_noRTM
XPM6: xpm_noRTM
hxrXPM: xtpg
XPM10: xtpg
XPM11: xpm_noRTM
```
Step 1: (Use XPM6 as an example) Stop the long-live pyxpm process  
Check the status of pyxpm
```
ssh tmo-daq -l tmoopr
procmgr status neh-base.cnf
Host           UniqueID     Status     PID     PORT   Command+Args
drp-srcf-mon001 pyxpm-0      RUNNING    25914   29451  pyxpm --ip 10.0.1.102 --db https://pswww.slac.stanford.edu/ws-auth/configdb/ws/,configDB,tmo,XPM -P DAQ:NEH:XPM:0
drp-srcf-mon001 pyxpm-1      RUNNING    25933   29459  pyxpm --ip 10.0.2.102 --db https://pswww.slac.stanford.edu/ws-auth/configdb/ws/,configDB,tmo,XPM -P DAQ:NEH:XPM:1
drp-srcf-mon001 pyxpm-2      RUNNING    25935   29453  pyxpm --ip 10.0.3.103 --db https://pswww.slac.stanford.edu/ws-auth/configdb/ws/,configDB,tmo,XPM -P DAQ:NEH:XPM:2
drp-srcf-mon001 pyxpm-3      RUNNING    25929   29452  pyxpm --ip 10.0.2.103 --db https://pswww.slac.stanford.edu/ws-auth/configdb/ws/,configDB,tmo,XPM -P DAQ:NEH:XPM:3
drp-srcf-mon001 pyxpm-4      RUNNING    25936   29454  pyxpm --ip 10.0.3.105 --db https://pswww.slac.stanford.edu/ws-auth/configdb/ws/,configDB,tmo,XPM -P DAQ:NEH:XPM:4
drp-srcf-mon001 pyxpm-5      RUNNING    25934   29456  pyxpm --ip 10.0.1.104 --db https://pswww.slac.stanford.edu/ws-auth/configdb/ws/,configDB,tmo,XPM -P DAQ:NEH:XPM:5
drp-srcf-mon001 pyxpm-6      RUNNING    36351   29455  pyxpm --ip 10.0.1.105 --db https://pswww.slac.stanford.edu/ws-auth/configdb/ws/,configDB,tmo,XPM -P DAQ:NEH:XPM:6
drp-srcf-mon001 pyxpm-7      RUNNING    15030   29458  pyxpm --ip 10.0.1.107 --db https://pswww.slac.stanford.edu/ws-auth/configdb/ws/,configDB,tmo,XPM -P DAQ:NEH:XPM:7
drp-neh-ctl002 pyxpm-10     NOCONNECT  -       29457  pyxpm --ip 10.0.5.102 --db https://pswww.slac.stanford.edu/ws-auth/configdb/ws/,configDB,tmo,XPM -P DAQ:NEH:XPM:10
drp-neh-ctl002 pyxpm-11     NOCONNECT  -       29450  pyxpm --ip 10.0.5.104 --db https://pswww.slac.stanford.edu/ws-auth/configdb/ws/,configDB,tmo,XPM -P DAQ:NEH:XPM:11
```
Stop the selected pyxmp
```
procmgr stop neh-base.cnf pyxpm-6
```
Step 2: Install the firmware for the xpm.  
- Pick the current version by viewing the output of amcc_dump_bsi in Step 0. The new mcs files are usually given by Matt, for example:
```
/cds/home/w/weaver/mcs/xpm/xpm-0x03090100-20240124215526-weaver-1af94a4.mcs
/cds/home/w/weaver/mcs/xpm/xpm_noRTM-0x03090100-20240125105637-weaver-93a4570.mcs
/cds/home/w/weaver/mcs/xpm/xtpg-0x03090100-20240124215328-weaver-1af94a4.mcs
```
- Find the ipaddress of the selected xpm from the neh-base.cnf status.    
- Hop on the correct node (drp-srcf-mon001 for production and drp-srcf-ctl002 for the fee teststand) then run:
```
~weaver/FirmwareLoader/rhel6/FirmwareLoader -a 10.0.1.105 /cds/home/w/weaver/mcs/xpm/xpm_noRTM-0x03090100-20240125105637-weaver-93a4570.mcs
```  
- Restart the rack (from psdev terminal)
```
fru_deactivate shm-neh-daq01/5
fru_activate shm-neh-daq01/5
```
- Restart the pyxmp process (from tmo-daq as tmoopr terminal)
```
procmgr start neh-base.cnf pyxpm-6
```
