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
### Use loopback to wake up the KCU
This is observed on cmp002 and cmp025. Running kcuSim cmd shows that remoteid is incorrect (all ones) and linkUp is 0. 
```
(ps-4.5.26) monarin@drp-srcf-cmp002 ~ 👁)$ kcuSim -s
-- Core Axi Version --
  firmware version  :  4000300
  scratch           :  0
  uptime count      :  70192
  build string      :  DrpTDet: Vivado v2022.1, rdsrv301 (Ubuntu 20.04.6 LTS), Built Thu 20 Jul 2023 12:37:07 PM PDT by weaver
...
            remoteid ffffffff
...
              linkUp        0

```
On cmp002, we tried different things including hitting TxLinkReset on xmppva, swapping connections on the BOS with other known xpm, etc. What worked was we use a loopback fiber on the dead lane, see the linkUp (should be 1) and swap back to the correct fiber (possibly powe cycle the nodes in between). At the end, we saw that linkUp stayed at 1.
Note that on cmp025, the node seems to fix itself.
### 
