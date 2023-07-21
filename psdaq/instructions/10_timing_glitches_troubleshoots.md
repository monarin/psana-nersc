## Bringing up DAQ after timing glitches
In this example, we focus on rix-daq by trying to bring all detectors back after a timing glitch. The list of detectors currently on rix.cnf (20230721) is shown below:
```
DETECTORS           NODE        STATUS
tptrig                          SHUTDOWN
rix_fim0_0                      SHUTDOWN
rix_fim1_0                      SHUTDOWN
groupca                         SHUTDOWN
andor_dir_0         cmp002      
andor_norm_0        cmp002
andor_vls_0         cmp002
epics_0             cmp002
mono_encoder_0      cmp002
control             cmp004      Y
rix_fim2_0          cmp004
mebuser0            cmp008
hsd_0               cmp009      
hsd_1               cmp009
hsd_2               cmp005
hsd_3               cmp005
timing_0            cmp010      Y
piranha_0           cmp012      Y (with bug)
teb0                cmp013      Y
manta_0             cmp025
gmdstr0_0           cmp025
gmdstr2_0           cmp025
xgmdstr0_0          cmp025
xgmdstr1_0          cmp025
xgmdstr2_0          cmp025
atmopal_0     
```
