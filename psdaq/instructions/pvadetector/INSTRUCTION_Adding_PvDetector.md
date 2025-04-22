# INSTRUCTION: Adding a PvDetector

## 🛠️ Steps to Add a New PVA Detector

1. **Determine the Size of the Image and Data Rate**

   - Estimate the payload size per event (e.g., 84 MiB for a 5Mpix image).
   - Decide the acquisition rate (e.g., 100 Hz) and verify system throughput.

2. **Update the DMA Driver (`tdetsim.service`)**

   Since PVA detectors only use DMA for TimingHeaders:

   - Set `cfgSize` to a small value (e.g., 4096 bytes).
   - Set `cfgRxCount` based on expected rate (e.g., 60).

   Example line in `tdetsim.service`:

   ```
   ExecStart=/sbin/insmod /usr/local/sbin/datadev.ko cfgTxCount=4 cfgRxCount=60 cfgSize=4096 cfgMode=0x2
   ```

3. **Configure the DAQ Conf File (e.g., `rix.py`)**

   - Add an entry using an available timing node and lane mask.
   - Set `pebbleBufSize` to image size (e.g., 84000000 for 84 MiB).
   - Set `pebbleBufCount` > `cfgRxCount` (e.g., 128).

   Example:

   ```python
   { host: 'drp-srcf-cmp025',
     id: 'axis_svls_0',
     flags: 'spu',
     env: epics_env,
     cmd: pva_cmd1 + ' -l 0x2 RIX:SVLS:CAM:01:IMAGE1:Pva:Image -k pebbleBufSize=88000000,pebbleBufCount=128' },
   ```

## ⚠️ Notes and Best Practices

- `cfgRxCount` and `cfgSize` affect all DRPs on a node.
- `pebbleBufSize` and `pebbleBufCount` are per-detector (per DRP process).
- Transition buffers are sized via `maxTrSize` and are independent of image payload size.
