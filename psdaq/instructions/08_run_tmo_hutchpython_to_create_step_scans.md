## Activate Hutch Python at TMO
Login as tmoopr and run daq-control gui
```
ssh tmo-daq -l tmoopr
cd /cds/group/pcds/dist/pds/tmo/scripts
procmgr start tmo_lcls1_gmd_xgmd.cnf
```
Note that tmo_lcls1_gmd_xgmd.cnf was used when we were debugging the step scans issue. Nothing specific to this example.  

On Daq-control, Partition Select > (Select Detectors) > Target State > (Connected)

Start hutch-python at tmo,
```
tmo3
```

Config the scan and run,
```
daq.configure(motors=[sim.fast_motor1, sim.fast_motor2], events=10, record=False)
RE(bp.scan([daq], sim.fast_motor1, 1, 10, sim.fast_motor2, 1, 10, 5))
```
View data on TMO Grafana

