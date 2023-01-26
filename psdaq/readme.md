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
