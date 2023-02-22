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
