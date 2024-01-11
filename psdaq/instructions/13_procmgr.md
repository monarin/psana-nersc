## Procmgr
To kill a persistent process (process started with port no.)
```
procmgr stop hsd.conf hsdioc_tmo_1a    # specify the name of the process
```
or use stopall
```
procmgr stopall hsd.conf
```
Note: increase timeout (sometimes start/stop don't succeed), you can increase the timeout by
```
procmgr stop rix.cnf -t 20
```
