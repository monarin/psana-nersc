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
### Restart hsd base processes
Some detectors rely on PV values received through base processes. Hsd for example, is one of them. With timing glitches, these base processes might need to be restarted. Follow the following instrutions:
1. Login to rixdaq
```
ssh rix-daq -l rixopr
rix-daq:~> cd /cds/group/pcds/dist/pds/rix/scripts/
rix-daq:scripts> source setup_env.sh
```
2. Check rix-hsd statuses
```
(ps-4.6.0) rix-daq:scripts> procmgr status rix-hsd.cnf 
/cds/home/opr/rixopr/git/lcls2_071823/install/bin/procmgr: using config file 'rix-hsd.cnf'
Not running.
Host           UniqueID     Status     PID     PORT   Command+Args
daq-rix-hsd-01 hsdioc_rix_1a RUNNING    104530  28076  hsd134PVs -P DAQ:RIX:HSD:1_1A -d /dev/pcie_adc_1a
daq-rix-hsd-01 hsdioc_rix_1b RUNNING    104529  28075  hsd134PVs -P DAQ:RIX:HSD:1_1B -d /dev/pcie_adc_1b
drp-srcf-mon001 hsdpvs_rix_1a_a RUNNING    11476   28073  hsdpvs -P DAQ:RIX:HSD:1_1A:A
drp-srcf-mon001 hsdpvs_rix_1a_b RUNNING    11477   28074  hsdpvs -P DAQ:RIX:HSD:1_1A:B
drp-srcf-mon001 hsdpvs_rix_1b_a RUNNING    11473   28071  hsdpvs -P DAQ:RIX:HSD:1_1B:A
drp-srcf-mon001 hsdpvs_rix_1b_b RUNNING    11474   28072  hsdpvs -P DAQ:RIX:HSD:1_1B:B
```
3. Stop all permanent processes (identified by PORT given in the rix.cnf or as shown in the status above).
```
(ps-4.6.0) rix-daq:scripts> procmgr stopall rix-hsd.cnf
```
Note that for a permanent process, you can also use `procmgr stop rix-hsd.cnf UniqueID` to stop just that persisting process.  
4. Start all the processes again
```
(ps-4.6.0) rix-daq:scripts> procmgr start rix-hsd.cnf
```
## Cutting PV communication
Like mentioned earlier, detectors often depend on PV communications. For atmopal, this is bi-directional. The detector receives the PV values, acts accordingly, and push the values back. In rix.cnf, this is -k PV:NAME. Sometimes, expected PVs are not available but we can still test if this detector is working w/o the PV values. You can do this removing -k in the cnf file.  
Original:   
```
{ host: 'drp-srcf-cmp027', id:'atmopal_0',   flags:'spu', env:epics_env,  cmd:drp_cmd0+' -l 0x1 -D opal -k ttpv=RIX:TIMETOOL:TTALL'}
```
Afer:       
```
{ host: 'drp-srcf-cmp027', id:'atmopal_0',   flags:'spu', env:epics_env,  cmd:drp_cmd0+' -l 0x1 -D opal'}
```
