# UED ePix-Quad-1kfps Deployment — November 4 2025

**DAQ Release:** `/cds/home/opr/uedopr/git/lcls2_251031`  
**Submodules:** `/cds/sw/ds/ana/conda2/rel/lcls2_submodules_11032025`

---

## 1 . Software / Firmware Versions

| Component | Repository | Commit / Tag | Notes |
|------------|-------------|---------------|-------|
| **ePix-Quad-1kfps** | `epix-quad-1kfps` | `239cbd54` (main) | “Updating PCIe FW version check for ≥ v4.2.0” |
| **PCIe Application** | `lcls2-pgp-pcie-apps` | `ccbe3de` (tag: v4.2.0) | Updated timing constraints |
| **Firmware Libraries** | `lcls2-pgp-fw-lib` | `d000e96` (tag: v7.0.0) | Pre-release merge, timing register update |
| **Submodule Bundle** | `lcls2_submodules_11032025` | — | Installed at `/cds/sw/ds/ana/conda2/rel/` |
| **DAQ Software Branch** | `lcls2` | `master` (local: lcls2_251031) | Includes new `epixquad1kfps_config.py` trigger logic |

---

## 2 . Firmware Update Procedure

Performed on **drp-ued-cmp003** using `/dev/datadev_0` (lane 3).

### Step 1 — Program the FPGA
```bash
python scripts/epixQuadLoadFpga.py --l 0
```

### Step 2 — Run ADC Training
```bash
python scripts/epixQuadADCTrain.py --l 0
```

> **Note:**  
> Lane 3 is shared with `iocMon`.  
> To free it before training:
> ```bash
> telnet localhost 30001
> ```
> then press **Ctrl-T** followed by **Ctrl-X**.  
>   
> To restart IOC later:
> ```bash
> sudo /usr/lib/systemd/scripts/ioc.sh
> ```
> or reconnect via telnet to start manually.

---

## 3 . DAQ Configuration Highlights

### New Trigger Scheme
Dual-buffer trigger implementation:

| Buffer Index | Source | Function | Typical Rate |
|---------------|---------|-----------|---------------|
| `TriggerEventBuffer[lane + 4]` | **EVR (Event Code 6)** | **Run Trigger** – continuous frame clock | 1080 Hz |
| `TriggerEventBuffer[lane]` | **XPM** | **DAQ Trigger** – acquisition trigger | ~100 Hz |

- RunTrigger keeps detector continuously clocked.  
- DAQTrigger arms/disarms with `StartRun()` / `StopRun()`.

### Delay Computation
- **DAQ Trigger:**  
  ```
  triggerDelay = (user.start_ns / clk_period)
                 - partitionDelay * msg_period
                 + 9
  ```
  → `+9` tick offset required after firmware clock fix.

- **Run Trigger:**  
  ```
  triggerDelay = user.start_ns / clk_period
  ```

### New Helper Functions
- `get_trigger_buffers()` → derive `(run_buf, daq_buf)` from current lane  
- `calc_daq_trigger_delay()` and `calc_run_trigger_delay()`  
- `epixquad_enable_runtrigger()` / `epixquad_disable_runtrigger()`  

### Firmware Dependency
`lcls2-pgp-fw-lib v7.0.0` corrected the timing register selection and ensures consistent EVR clock domain for RunTrigger.

---

## 4 . ADC Training Values Decoding

After firmware flashing, **ADC retraining** must be performed before data taking.

### Enabling Debug Output
In `epixquad1kfps_config.py`, set:
```python
DEBUG_ADC_TRAIN_WRITE = True
```

### Procedure
Run the unpacking script:
```bash
/cds/home/m/monarin/firmware/update_notes/epixquad1kfps_deploy_20251031/unpack_adc_training.py
```

### Example Output
```
Decoded 90 ADC delay values:
ADC00: frame= 221, lanes=[213 191 219 206 244 246 227 217]
ADC01: frame= 389, lanes=[376 405 382 408 423 424 433 430]
ADC02: frame= 281, lanes=[279 269 277 270 286 265 296 301]
ADC03: frame= 101, lanes=[ 97  78  93  55 104  93 110  60]
ADC04: frame= 217, lanes=[207 203 210 196 237 201 248 238]
ADC05: frame= 405, lanes=[429 428 433 444 453 453 456 446]
ADC06: frame= 382, lanes=[364 331 373 378 402 402 399 378]
ADC07: frame= 325, lanes=[368 355 367 374 375 388 382 387]
ADC08: frame= 226, lanes=[237 217 250 243 220 225 235 234]
ADC09: frame= 250, lanes=[268 276 227 249 220 226 212 228]
```

### Important Notes
- Perform ADC training **when the detector temperature is stable (≈ 65–70 °C)**.  
  Cold training values may result in unstable operation or image artifacts.
- Keep a record of trained values **before and after firmware update** for comparison.

---

## 5 . Known and Resolved Issues

| Issue | Resolution |
|--------|-------------|
| **DAQ vs RunTrigger misalignment** | Added `+9` offset in DAQ Trigger delay; validated synchronization. |
| **Incorrect timing register** | Fixed in `lcls2-pgp-fw-lib v7.0.0` – firmware now uses proper 186 MHz clock domain. |
| **Subframe mismatch (3 → 4)** | Updated `EpixQuad.cc` to expect 4 DMA subframes. |

---

## 6 . Verification Summary

- **RunTrigger** confirmed active at 1080 Hz (EVR event code 6).  
- **DAQTrigger** verified at 100 Hz after +9 offset correction.  
- EventBuilder receives synchronized frames with 4 DMA subframes.  
- ADC training validated post-firmware update.

---

### Deployment Complete
✅ **Date:** 2025-11-04  
✅ **System:** UED — ePixQuad-1kfps  
✅ **Maintainers:** Monarin (DAQ), Matt Weaver (FW), Larry Ruckman (FPGA)
