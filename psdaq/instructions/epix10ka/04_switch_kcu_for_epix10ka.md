```
ssh drp-det-cmp001
sudo vim /usr/lib/systemd/system/kcu.service

comment out/uncomment relevant detector preset:

#  epixUHR at 35kHz
ExecStart=/sbin/insmod /usr/local/sbin/datadev.ko cfgTxCount=4 cfgRxCount=16380 cfgSize=262144 cfgMode=0x2
#  epix10ka at 1kHz
#ExecStart=/sbin/insmod /usr/local/sbin/datadev.ko cfgTxCount=4 cfgRxCount=1020 cfgSize=2097152 cfgMode=0x2

sudo systemctl daemon-reload
sudo systemctl restart kcu.service
```
