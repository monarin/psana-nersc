## Updating values in datadev.service (sudo needed)
1. Locate datadet.service and update values (e.g. cfgCount, etc.). 
```
(daq_20250402) monarin@drp-neh-cmp012 (main) cb_dld_event locate datadev.service
/etc/systemd/system/datadev.service
(daq_20250402) monarin@drp-neh-cmp012 (main) cb_dld_event sudo vi /etc/systemd/system/datadev.service
```
2. After saving the change, run below commands:
```
sudo rmmod datadev
sudo systemctl daemon-reload
sudo systemctl start datadev.service
sudo systemctl enable datadev.service
```
3. Check if the values are correct:
```
cat /proc/datadev_0
```
