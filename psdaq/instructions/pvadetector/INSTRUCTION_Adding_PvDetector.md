# 🛠️ Adding a New PvDetector to the DAQ

This guide walks you through the process of integrating a new EPICS PVA detector into the DAQ system. The steps below are based on recent integration of a RIX 5Mpix Axis camera.

---

## 1. 📐 Determine Image Size and Data Rate

- Use EDM or `pvinfo` to inspect image dimensions and data type.
- Multiply width × height × (bytes per pixel) to get **image size in bytes**.
  - For a 5Mpix `uint16` image: `6144 × 6144 × 2 = ~74 MiB`
- Estimate frame rate requirements to understand throughput demands.

---

## 2. ⚙️ Update Kernel Driver Buffer Settings

Edit the driver service file (typically `tdetsim.service`) and update the line that loads the PGP kernel module:

```
ExecStart=/sbin/insmod /usr/local/sbin/datadev.ko cfgTxCount=4 cfgRxCount=80 cfgSize=1048576 cfgMode=0x2
```

- **cfgRxCount**: Number of DMA buffers (ring buffer slots).
- **cfgSize**: Size of each DMA buffer in bytes (e.g., 1 MiB = 1048576).

> 💡 Total buffer size (cfgRxCount × cfgSize) must be greater than or equal to the image size. Otherwise, a buffer overrun may occur.

Restart the driver:
```bash
sudo systemctl daemon-reload
sudo systemctl restart tdetsim.service
```

---

## 3. 🧾 Add Detector Entry in DAQ Config (e.g., `rix.py`)

Update the DAQ configuration file (e.g., `rix.py`) to include the detector:

```python
{ host: 'drp-srcf-cmp025',
  id: 'axis_svls_0',
  flags: 'spu',
  env: epics_env,
  cmd: pva_cmd1 + ' -l 0x2 RIX:SVLS:CAM:01:IMAGE1:Pva:Image -k pebbleBufSize=84000000' },
```

- `-l 0x2`: Lane mask. Set a free lane bit corresponding to the timing connection.
- `-k pebbleBufSize=84000000`: Optional kwargs. Set `pebbleBufSize` to image size (in bytes).
- You can also add `pebbleBufCount=N` if you want to override the buffer count (must be > `cfgRxCount`).

---

## ✅ Final Checks

- Ensure the image size and data rate are sustainable on the selected host.
- Verify buffer allocation logs in `drp_pva` show reasonable `m_payloadSize`, `Queue depth`, and `Total buffer size`.
- Test with `drp_pva` and check for segmentation faults or warnings.

Good luck! 🎉