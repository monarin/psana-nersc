## Activate Hutch Python at TMO
Login as tmoopr and run daq-control gui
```
ssh tmo-daq -l tmoopr
cd /cds/group/pcds/dist/pds/tmo/scripts
source setup_env.sh
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
View data on [TMO Grafana](https://pswww.slac.stanford.edu/system/grafana/d/TqlIHxqWz/l2si-daq?orgId=1&refresh=5s&from=now-5m&to=now&var-instrument=tmo&var-partition=0&var-group=0&var-detname=bld)

The output:
```
Transient Scan ID: 11     Time: 2023-07-10 17:42:58
Persistent Unique Scan ID: 'd0b51629-9c4c-4c54-97dc-1d3b53893682'
New stream: 'primary'
+-----------+------------+-------------+-------------+
|   seq_num |       time | fast_motor1 | fast_motor2 |
+-----------+------------+-------------+-------------+
|         1 | 17:43:01.3 |           1 |           1 |
|         2 | 17:43:01.5 |        3.25 |        3.25 |
|         3 | 17:43:01.7 |         5.5 |         5.5 |
|         4 | 17:43:01.9 |        7.75 |        7.75 |
|         5 | 17:43:02.1 |          10 |          10 |
+-----------+------------+-------------+-------------+
generator scan ['d0b51629'] (scan num: 11)
```
## Troubleshoot
The hutch-python process can hang. Use Ctrl-Z and kill %1 to terminate the process.


