## IOC Manager 
is a software that collects all registers from different cameras and devices through EPICS. 
Each hutch has a specific set of hosts and ioc values that they are watching. 
For example, tst hutch has this configuration `/cds/group/pcds/pyps/config/tst/iocmanager.cfg`.  

### IOC Manager Gui
Scientists can use IOCManager gui to view these values. For example, at rix, you can view the gui by
```
kinit    # if not already has the the ticket
ssh rix-daq -l rixopr
/cds/group/pcds/epics/ioc/common/pgpWave8/latest/children/build/iocBoot/ioc-rix-pgpw8-03/edm-ioc-rix-pgpw8-03.cmd
```
To obtain the above cmd:
```
caget -S IM2K0:XTES:CAM:LAUNCH_EDM
```
The epics var name before LAUNCH_EDM comes from the cnf file of this detector.  

IOC Manager for Wave8 at Rix Main
![ins06_ioc_wave8_main](/psdaq/images/ins06_ioc_wave8_main.png)
Click PyRogue Wave8 Diag to see all registers
![ins06_ioc_wave8_registers](/psdaq/images/ins06_ioc_wave8_registers.png)
