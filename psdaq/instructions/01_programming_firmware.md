## Programming FEB (front-end-board/ the "black box") and KCU1500 for Opal
### FEB
- Get the firmware from https://github.com/slaclab/cameralink-gateway/releases/tag/v8.2.3
- On the node where Opal is installed, from cameralink-gateway repo, run
  ```
  python software/scripts/updateFebFpga.py --mcs ~/ClinkFebPgp2b_1ch-0x02000000-20191210103130-ruckman-d6618cc.mcs --lane 0 --pgp4 0
  ```
  Note* replace the above .mcs file with the downloaded one
  Note** lane can be determined from .cnf file
### KCU1500 Data (datadev_0)
1. On psbuild-rhel7 or any other nodes with internet access, wget both the primary and secondary mcs files of the requested version from https://github.com/slaclab/lcls2-pgp-pcie-apps/releases/tag/v3.7.0
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
1. On the node that needs update, go to Matt's copy of pgp-pcie-apps and run the following:
```
cd ~weaver/pgp-pcie-apps-new/software/
source setup_l2si.sh
python scripts/updatePcieFpga.py --dev /dev/datadev_1 --path ~weaver/mcs/drp --type SPIx8
```
where datadev_1 is usually the timing system driver and path is Matt's usual path where he stores the new firmware images.  

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




