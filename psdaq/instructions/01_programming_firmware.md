## Programming KCU1500 Firmware
1. On psbuild-rhel7 or any other nodes with internet access, wget both the primary and secondary mcs files of the requested version from this [cameralink-gateway releases page](https://github.com/slaclab/cameralink-gateway/releases).
2. Logon to the node with the KCU1500 (that you wish to program)
3. Check the current version:
```
cat /proc/datadev_0     # or datadev_1
```
5. 
