## Programming KCU1500 Firmware
1. On psbuild-rhel7 or any other nodes with internet access, wget both the primary and secondary mcs files of the requested version from this [cameralink-gateway releases page](https://github.com/slaclab/cameralink-gateway/releases).
2. Logon to the node with the KCU1500 (that you wish to program)
3. Check the current version:
```
cat /proc/datadev_0       # or datadev_1
```
4. Run update script - this assumes you already clone cameralink-gateway, see cloning instruction [here](https://docs.google.com/presentation/d/1zXggROZ05NY4N3eIyy0ydyl0WuofBa2jR7cAse2rPz4/edit?usp=sharing)
```
cd ~/cameralink-gateway   
python software/scripts/updatePcieFpga.py --path $HOME/Downloads --type SPIx8     # where path is where the mcs files are
```
**Note** If there are two datadev_ (0 and 1), add `--dev /dev/datadev_1`. See full instruction [here](https://confluence.slac.stanford.edu/display/PSDMInternal/Debugging+DAQ#DebuggingDAQ-Opal).
5. Power reset node
```
ssh psdev
/reg/common/tools/bin/psipmi node-name power status   # check status
/reg/common/tools/bin/psipmi node-name power reset.   # reset cpu
```
6. Wait 10 mins
7. Check `/proc/datadev_0` and run devGui to check registers



