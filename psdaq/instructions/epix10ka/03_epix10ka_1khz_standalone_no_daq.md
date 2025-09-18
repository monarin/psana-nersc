
# Epix10ka 1kHz Standalone Register Test (No DAQ)

This README describes how to run and verify standalone camera tests to support **1kHz operation** for the epix10ka using devGuis (camera and kcu1500) and GroupCA (XPM control).

## Summary
We **do not** run the full DAQ stack. Instead, we launch:
- Camera devGui (`epixQuadDAQ.py`)
- KCU1500 devGui (`devGui.py`)
- GroupCA for XPM (`DAQ:ASC` XPM 0 Group 2)

---

## 1. Start Camera devGui
On daq-det-evr01
```bash
cd /cds/home/j/jumdz/epix-quad/software
python scripts/epixQuadDAQ.py --l 0 --dev /dev/datadev_0
```

### Camera Configuration
1. SKIP (UPDATED 2025-07-16: Loading this yml causes the Framesize to reduce to 1600 Bytes) **Load Config YAML**:
    - In System tab:
      ```
      /cds/home/j/jumdz/epix-quad/software/yml/ued/epixQuad_ASICs_allAsics_UED_1080Hz_settings.yml
      ```
    - Click **Load Config**.

2. After loading:
   - Set:
     ```
     SystemRegs.TrigSrcSel = 0x0      # External trigger  
     SystemRegs.AutoTrigEn  = False   # Disable internal trigger  
     AcqCore.AsicRoClkHalfT = 0xAAAA0001 # For running at 1kHz
     ```
   - (Optional) Reset counters in `RdoutStreamMonitoring.Ch[0]` using the **Exec** button next to `CntRst`.

---

## 2. Start kcu1500 devGui

```bash
cd /cds/home/j/jumdz/lcls2-epix-hr-pcie/software
python scripts/devGui.py --dev /dev/datadev_0 --pgp4 1 --serverPort 9004 --pcieBoardType XilinxKcu1500
```

### KCU1500 Configuration
- Navigate to:
  ```
  DevPcie.Application.AppLane[0].EventBuilder
  ```
- Set `Blowoff`:
    - Toggle **True** then **False** to flush stale buffered events.
- Set `Timeout`:
    - The calculation is
      ```
      hex(int(156.25e6 / rate))
      ```
      For 102Hz, Timeout = 0x1763F6.
      For 1020Hz, Timeout = 0x25632.

---

## 3. Start GroupCA (XPM trigger control)

Run this on a machine with access to EPICS:

```bash
groupca DAQ:ASC 0 2
```

> This targets **XPM 0, Group 2**

Click the **Run** button to start trigger stream.

---

## 4. Verify Operation
- In **kcu1500 devGui**: DevRoot, Hit Exec StartRun.
- In **Camera devGui**: `FrameCnt` (under `RdoutStreamMonitoring.Ch[0]`) should be increasing.
- In **kcu1500 devGui**: `DevPcie.Application.AppLane[0].EventBuilder.DataCnt[0-2]` should all be increasing at comparable rates.
More information about DataCnt lanes:
DMA Channel mapping section on this page: https://github.com/slaclab/lcls2-pgp-pcie-apps. 
---

## Note

To verify **which group (partition)** the KCU1500 listens to for triggers:

- Check:
  ```
  TimingRx.TriggerEventManager.TriggerEventBuffer[0].Partition
  ```
- Lane 0 corresponds to the epix10ka data.
- Make sure this value matches the group you're triggering from (i.e. Group 2).

---

## Conclusion

This standalone test setup confirms that the camera can receive and process triggers at 1kHz. If the rates are lower or inconsistent:
- Recheck XPM group configuration
- Verify TrigSrcSel is set to 0
- Ensure `Blowoff` was toggled
- Ensure configuration YAML does not restrict frame rate (e.g. internal trigger pacing)

