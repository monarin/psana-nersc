## Useful commands for pv management
```
(ps-4.5.26) monarin@drp-srcf-cmp012 ~ 👁)$ pvget DAQ:NEH:XPM:0:PART:0:L0Delay
DAQ:NEH:XPM:0:PART:0:L0Delay 2023-01-30 18:26:49.900  99 
(ps-4.5.26) monarin@drp-srcf-cmp012 ~ 👁)$ pvinfo DAQ:NEH:XPM:0:PART:0:L0Delay
DAQ:NEH:XPM:0:PART:0:L0Delay
Server: 172.21.152.78:41807
Type:
    epics:nt/NTScalar:1.0
        uint value
        alarm_t alarm
            int severity
            int status
            string message
        time_t timeStamp
            long secondsPastEpoch
            int nanoseconds
            int userTag

(ps-4.5.26) monarin@drp-srcf-cmp012 ~ 👁)$ host 172.21.152.78
78.152.21.172.in-addr.arpa domain name pointer drp-srcf-mon001.pcdsn.
```
Other pv commands:
```
pvput PV:VAR value
```
```
pvmonitor PV:VAR
```
## xpmpva
You need to be on the right node to access PV values:
- For room208 xpms, hop on drp-srcf-mon001
- For FEE Alcove, hop on drp-neh-ctl002  

For each XPM, you can use xpmpva tool to view the channel
```
xpmpva DAQ:NEH:XPM:5 DAQ:NEH:XPM:6
```
For viewing XPM 5 and 6.
![example of xpmvpa tool](/psdaq/images/ex-xpmvpa_xpm5_amc0.png)
## hsdpva
```
hsdpva DAQ:TMO:HSD:1_1A:B DAQ:TMO:HSD:1_3D:B DAQ:TMO:HSD:1_3D:A DAQ:TMO:HSD:1_DA:A DAQ:TMO:HSD:1_DA:B
```
