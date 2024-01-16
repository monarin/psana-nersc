## configdb cli
To check which hutches are available:
```
(ps-4.5.26) monarin@drp-neh-cmp001 (master *) cnf 👁)$ configdb ls
tmo
ued
rix
tst
asc
```
You can look inside each folder liket this:
```
(ps-4.5.26) monarin@drp-neh-cmp001 (master *) cnf 👁)$ configdb ls tst/BEAM
epix100_0
epixhr_0
hsd_0
hsd_1
hsd_10
hsd_11
hsd_2
hsd_3
hsd_5
hsd_7
timing_0
...
```
To view the values (json) for each detector:
```
configdb cat tst/BEAM/timing_0
```
You can copy a detector item:
```
configdb cp tst/BEAM/timing_0 tst/BEAM/timing_1 --write
```
If copying between hutches, you need to specify the destination hutch in --user:
```
configdb cp --user tmoopr --write tst/BEAM/txi_fim1_0 tmo/BEAM/txi_fim1_0
```
