## Switching between two network cards
One network card with fiber connection on mon001 isn't working properly. From `/var/log/messages`, it looks the link has been going up and down.
```
sudo vi /var/log/messages
...
Jul 20 16:36:06 drp-srcf-mon001 kernel: myri10ge 0000:41:00.0 enp65s0: link down
Jul 20 16:36:06 drp-srcf-mon001 kernel: myri10ge 0000:41:00.0 enp65s0: link up
Jul 20 16:36:07 drp-srcf-mon001 kernel: myri10ge 0000:41:00.0 enp65s0: link down
Jul 20 16:36:07 drp-srcf-mon001 kernel: myri10ge 0000:41:00.0 enp65s0: link up
Jul 20 16:36:09 drp-srcf-mon001 kernel: myri10ge 0000:41:00.0 enp65s0: link down
Jul 20 16:36:09 drp-srcf-mon001 kernel: myri10ge 0000:41:00.0 enp65s0: link up
Jul 20 16:36:13 drp-srcf-mon001 kernel: myri10ge 0000:41:00.0 enp65s0: link down
Jul 20 16:36:13 drp-srcf-mon001 kernel: myri10ge 0000:41:00.0 enp65s0: link up
Jul 20 16:36:14 drp-srcf-mon001 kernel: myri10ge 0000:41:00.0 enp65s0: link down
...
```
This shows that enp65s0 link has been up and down.  
From ifconfig, we see that there's another network card that is unused.  
```
ifconfig -a
eno2d1: flags=4098<BROADCAST,MULTICAST>  mtu 9000
        ether 3c:ec:ef:42:1f:f5  txqueuelen 1000  (Ethernet)
        RX packets 34677  bytes 3355337 (3.1 MiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 38372  bytes 3637682 (3.4 MiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

enp65s0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 9000
        inet 10.0.0.3  netmask 255.255.240.0  broadcast 10.0.15.255
        inet6 fe80::260:ddff:fe44:4e7c  prefixlen 64  scopeid 0x20<link>
        ether 00:60:dd:44:4e:7c  txqueuelen 1000  (Ethernet)
        RX packets 862842268  bytes 130555940015 (121.5 GiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 916547192  bytes 69618657210 (64.8 GiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
...
```
This is eno2d1 (copper connector but we have a converter). We want to move the fiber from enp65s0 to the converter plugged into eno2d1. 
Prior to this, we bring eno2d1 up by assigning the inet and netmask to it. Note that by assiging the inet, we were able to bring it up too.
```
sudo ifconfig eno2d1 10.0.0.4
sudo ifconfig eno2d1 netmask 255.255.240.0
ifconfig -a
...
eno2d1: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 9000
        inet 10.0.0.4  netmask 255.255.240.0  broadcast 10.0.15.255
        inet6 fe80::3eec:efff:fe42:1ff5  prefixlen 64  scopeid 0x20<link>
        ether 3c:ec:ef:42:1f:f5  txqueuelen 1000  (Ethernet)
        RX packets 25269350  bytes 4046995412 (3.7 GiB)
        RX errors 0  dropped 0  overruns 0  frame 98049
        TX packets 27762740  bytes 2058647294 (1.9 GiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```
We moved the fiber and brought enp65s0 down.
```
sudo ifdown enp65s0
```
We tried to ping xpm0 (mon001 collects data from xpms).
```
monarin@drp-srcf-mon001 ~ 👁)$ ping 10.0.1.102
PING 10.0.1.102 (10.0.1.102) 56(84) bytes of data.
64 bytes from 10.0.1.102: icmp_seq=1 ttl=32 time=0.028 ms
64 bytes from 10.0.1.102: icmp_seq=2 ttl=32 time=0.035 ms
64 bytes from 10.0.1.102: icmp_seq=3 ttl=32 time=0.036 ms
64 bytes from 10.0.1.102: icmp_seq=4 ttl=32 time=0.027 ms
```
Note that updating the network card on mon001 can cause xpm connections to freeze (xpmpva froze is one of the symptoms). 
We can restart xmp base processes by following these instructions:  
1. Login to tmo-daq
```
ssh tmo-daq -l tmoopr
tmo-daq:~> cd /cds/group/pcds/dist/pds/tmo/scripts
tmo-daq:scripts> source setup_env.sh
```
2. Check status of neh base processes
```
ps-4.6.0) tmo-daq:scripts> procmgr status neh-base.cnf
/cds/home/opr/tmoopr/git/lcls2_071823/install/bin/procmgr: using config file 'neh-base.cnf'
Not running.
Host           UniqueID     Status     PID     PORT   Command+Args
drp-neh-ctl002 pvrtmon-fee  RUNNING    114139  29462  epics_exporter -H tst -I xpm-10 -M /cds/group/psdm/psdatmgr/etc/config/prom -P DAQ:NEH:XPM:10 -G Us:RxLinkUp RunTime Run NumL0Acc L0AccRate NumL0Inp L0InpRate DeadFrac
drp-neh-ctl002 pyxpm-fee    RUNNING    114138  29457  pyxpm --ip 10.0.5.102 --db https://pswww.slac.stanford.edu/ws-auth/configdb/ws/,configDB,tmo,XPM -P DAQ:NEH:XPM:10
drp-srcf-mon001 pvrtmon      RUNNING    54506   29460  epics_exporter -H tmo -I xpm-2 -M /cds/group/psdm/psdatmgr/etc/config/prom -P DAQ:NEH:XPM:2 -G Us:RxLinkUp RunTime Run NumL0Acc L0AccRate NumL0Inp L0InpRate DeadFrac
...
```
3. Stop and restart the permanent processes
```
(ps-4.6.0) tmo-daq:scripts> procmgr stopall neh-base.cnf
/cds/home/opr/tmoopr/git/lcls2_071823/install/bin/procmgr: using config file 'neh-base.cnf' to stop
(ps-4.6.0) tmo-daq:scripts> procmgr start neh-base.cnf
/cds/home/opr/tmoopr/git/lcls2_071823/install/bin/procmgr: using config file 'neh-base.cnf' to start
```
