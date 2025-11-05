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

## 4 . Known and Resolved Issues

| Issue | Resolution |
|--------|-------------|
| **DAQ vs RunTrigger misalignment** | Added `+9` offset in DAQ Trigger delay; validated synchronization. |
| **Incorrect timing register** | Fixed in `lcls2-pgp-fw-lib v7.0.0` – firmware now uses proper 186 MHz clock domain. |
| **Subframe mismatch (3 → 4)** | Updated `EpixQuad.cc` to expect 4 DMA subframes. |

---

## 5 . Verification Summary

- **RunTrigger** confirmed active at 1080 Hz (EVR event code 6).  
- **DAQTrigger** verified at 100 Hz after +9 offset correction.  
- EventBuilder receives synchronized frames with 4 DMA subframes.  
- ADC training validated post-firmware update.

---

### Deployment Complete
✅ **Date:** 2025-11-04  
✅ **System:** UED — ePixQuad-1kfps  
✅ **Maintainers:** Monarin (DAQ), Matt Weaver (FW), Larry Ruckman (FPGA)
