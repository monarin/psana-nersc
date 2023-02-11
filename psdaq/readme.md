## Online Data System Overview
![Online Data System Overview](/psdaq/Online_Data_Systems_Overview.png)

There are three layers within the Online Data Sytems.
### Data Acquisition (DAQ) 
Overview of an example DAQ system from RIX to SRCF nodes. [DAQ Overview Slides](https://docs.google.com/presentation/d/1zXggROZ05NY4N3eIyy0ydyl0WuofBa2jR7cAse2rPz4/edit?usp=sharing). 
![DAQ-overview](/psdaq/DAQ-overview.png)
### Data Reduction Pipeline (DRP)
All DRP nodes, which receive timing signals and etc. are connected to the Infiniband switch. A group of Software Trigger nodes are also connected to the switch. 
### Fast-feedback (FFB) 
Recorded data are written to the FFB. From this side of the diagram, Online Monitoring is performed on Online Monitoring Nodes. 

There are several platforms that we can run Daq control on. This is indicated at the top of the .cnf file i.e. platform=6.

## Overview
Nodes on each cluster (neh, srcf, or etc.) runs a procmgr program which allow itself to associate to any platforms. The procmgr config file sets up parameters including a list of users (one for each platform) to be used as procmgr user running for that platform. 
```bash
(ps-4.5.24) monarin@drp-srcf-mon001 daq-live 👁)$ cat /etc/procmgrd.conf 
#
# This file is managed by Puppet.
# DO NOT EDIT
#

# procmgrd.conf
PORTBASE=29000
PROCMGRDBIN=/cds/sw/package/procServ/2.6.0-SLAC/x86_64-rhel7-gcc48-opt/bin/procmgrd
PROCSERVBIN=/cds/sw/package/procServ/2.6.0-SLAC/x86_64-rhel6-gcc44-opt/bin/procServ
# comma-delimited list of up to 8 procmgrd users
PROCMGRDUSERS=tmoopr,tstopr,rixopr,tstopr,tstopr,tstopr,tstopr,tstopr
CONDABASE=/cds/sw/ds/ana/conda2/inst
```
For 8 platforms, on each node, we'll see 8 processes running as procmgrdN (where N is the no. of platform).
```bash
(ps-4.5.24) monarin@drp-srcf-mon001 daq-live 👁)$ ps -ef | grep procmgr
tmoopr   10040     1  0  2022 ?        00:04:58 /cds/sw/package/procServ/2.6.0-SLAC/x86_64-rhel7-gcc48-opt/bin/procmgrd0 --allow --ignore ^D -l 29001 --coresize 0 -c /tmp 29000 /bin/tcsh -f
tstopr   10046     1  0  2022 ?        00:05:02 /cds/sw/package/procServ/2.6.0-SLAC/x86_64-rhel7-gcc48-opt/bin/procmgrd1 --allow --ignore ^D -l 29101 --coresize 0 -c /tmp 29100 /bin/tcsh -f
rixopr   10052     1  0  2022 ?        00:05:00 /cds/sw/package/procServ/2.6.0-SLAC/x86_64-rhel7-gcc48-opt/bin/procmgrd2 --allow --ignore ^D -l 29201 --coresize 0 -c /tmp 29200 /bin/tcsh -f
tstopr   10058     1  0  2022 ?        00:05:05 /cds/sw/package/procServ/2.6.0-SLAC/x86_64-rhel7-gcc48-opt/bin/procmgrd3 --allow --ignore ^D -l 29301 --coresize 0 -c /tmp 29300 /bin/tcsh -f
tstopr   10064     1  0  2022 ?        00:05:03 /cds/sw/package/procServ/2.6.0-SLAC/x86_64-rhel7-gcc48-opt/bin/procmgrd4 --allow --ignore ^D -l 29401 --coresize 0 -c /tmp 29400 /bin/tcsh -f
tstopr   10070     1  0  2022 ?        00:05:07 /cds/sw/package/procServ/2.6.0-SLAC/x86_64-rhel7-gcc48-opt/bin/procmgrd5 --allow --ignore ^D -l 29501 --coresize 0 -c /tmp 29500 /bin/tcsh -f
tstopr   10076     1  0  2022 ?        00:05:05 /cds/sw/package/procServ/2.6.0-SLAC/x86_64-rhel7-gcc48-opt/bin/procmgrd6 --allow --ignore ^D -l 29601 --coresize 0 -c /tmp 29600 /bin/tcsh -f
tstopr   10082     1  0  2022 ?        00:04:59 /cds/sw/package/procServ/2.6.0-SLAC/x86_64-rhel7-gcc48-opt/bin/procmgrd7 --allow --ignore ^D -l 29701 --coresize 0 -c /tmp 29700 /bin/tcsh -f
```
These procmgrs are talking to each other to identify tasks that need to be performed.

## Daq Control
Running a Daq control on each platform requires the use of a .cnf file. Examples of the cnf file are in lcls2/psdaq/psdaq/cnf. Procmgr reads configuration in the file to identify several things including:
- User details for accessing the database
- GUI selections (i.e. turnning on by adding a line)
```
procmgr_config = [
 {                         id:'groupca',     flags:'s',   env:epics_env, cmd:f'groupca DAQ:NEH 3 {groups}'},
 {                         id:'procstat',    flags:'p',                  cmd:f'procstat {CONFIGDIR}/p{platform}.cnf.last'},

```
- Detector selections (indicate host and detector detail to read the data from)
```
 {host: 'drp-srcf-cmp019', id:'teb0',        flags:'spu',                cmd:f'{teb_cmd}'},

 {host: 'drp-srcf-cmp029', id:'timing_0',    flags:'spu', env:epics_env, cmd:f'{drp_cmd1} -l 0x1 -D ts'},

 {host: 'drp-srcf-cmp029', id:'tstcam1_0',   flags:'spu',                cmd:f'{drp_cmd0} -l 0x1 -D fakecam -k sim_length=145'},
```
**Note:** You need to where where the required hardware are located. For the example above, cmp029 can be used for the timing system and the fake camera. Each cluster has a different setup.

Depending on which cluster and whether you're running a real system or a teststand, the startup node, the user that you use to login to that node, and the values in the cnf file will be different. On a particular (correct) startup node, run
```
procmgr start mona.cnf
````
to start the process.

## Driver Control
Each node has different hardware installed. To check how the driver is being setup, i.e. on cmp015 with a fake detector
```
monarin@drp-neh-cmp015 ~ 👁)$ locate tdetsim.service
/etc/systemd/system/multi-user.target.wants/tdetsim.service
/usr/lib/systemd/system/tdetsim.service
/usr/lib/systemd/system/tdetsim.service~
monarin@drp-neh-cmp015 ~ 👁)$ less /usr/lib/systemd/system/tdetsim.service
monarin@drp-neh-cmp015 ~ 👁)$ cat /usr/lib/systemd/system/tdetsim.service
[Unit]
Description=SimCam Device Manager
Requires=multi-user.target
After=multi-user.target

[Service]
Type=forking
ExecStartPre=-/sbin/rmmod datadev.ko
#2023/01/05 commented out by RMelchiorri dma map memory error, switch to second line
#ExecStart=/sbin/insmod /usr/local/sbin/datadev.ko cfgTxCount=4 cfgRxCount=1048572 cfgSize=4096 cfgMode=0x2
ExecStart=/sbin/insmod /usr/local/sbin/datadev.ko cfgTxCount=4 cfgRxCount=2044 cfgSize=262144 cfgMode=0x2
ExecStartPost=/usr/local/sbin/kcuSim -s -d /dev/datadev_1
#ExecStartPost=/usr/bin/sh -c "/usr/bin/echo 4 > /proc/irq/368/smp_affinity_list"
#modified 2023/01/05 by RMelchiorri in neh-cmp015 is causing an error, cannot write in directory
#ExecStartPost=/usr/bin/sh -c "/usr/bin/echo 4 > /proc/irq/369/smp_affinity_list"
#ExecStartPost=/usr/bin/sh -c "/usr/bin/echo 5 > /proc/irq/370/smp_affinity_list"
KillMode=none
IgnoreSIGPIPE=no
StandardOutput=syslog
StandardError=inherit

[Install]
WantedBy=multi-user.target
```
**Note:** The module insmod inserts the given driver with parameters to the system. In this case, the driver is datadev.ko with 2044 buffers (each buffer is 262144 bytes). 
### Updating Driver Parameters
1. Update values in the driver file, i.e. for fake cam
```
vi /usr/lib/systemd/system/tdetsim.service
```
2. Reload daemon then restart the driver service (sudo is required).
```
systemctl daemon-reload
systemctl restart tdetsim.service
```
3. Check if the values are correct:
```
cat /proc/datadev_1
```

## Running Daq
After all the GUIs are present, use Daq Control `Partition > Select` to select detectors that you want to obtain data from. Choose `Recording` to write data to disk. Choose `Target State: Configure` and select DAQ:NEH (separate GUI) Fixed Rate LOSelect mkHz to change the rate from the previous run. You can also choose `Target State: Running` to start running with the saved rate. When done, choose `Unallocated` to finish the run.

The log files are written to your $HOME/yyyy/mm/d-{a combination of date, detector name, etc}. 

## Troubleshooting
### Rebooting a node
For srcf nodes, hop on psdev
```ssh psdev```
Use psipmi to query status, reboot, and power a node. 
To check status:
```
monarin@psdev01 ~ 👁)$ /reg/common/tools/bin/psipmi drp-srcf-cmp010 power status

PCDS IPMI Tool
System power status
Chassis Power is on
```
To reset cpu (not taking away the power):
```
bash-4.2$ /reg/common/tools/bin/psipmi drp-srcf-cmp010 power reset

PCDS IPMI Tool
System power reset
Chassis Power Control: Reset
```
To power cycle a node (Warning!!! Only use this as the last resource)
```
bash-4.2$ /reg/common/tools/bin/psipmi drp-srcf-cmp010 power cycle
```

