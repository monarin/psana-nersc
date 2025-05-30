# Timing Recovery After Outage — RIX DAQ

This repository documents the symptoms and recovery procedure for timing misalignment issues observed in the RIX instrument after timing distribution outages.

## 🛑 Problem Summary

After a timing outage, the DAQ system may report misaligned timestamps between `timing_0` and other detectors during the `Configure` transition. The `teb` log shows repeated warnings like:

```
rix-teb[40181]: <W> Fixup Configure, 00a8a5221a0f3b, size 0, source 0 (rix_fim1_0)
rix-teb[40181]: <W> Fixup Configure, 00a8a5221a0f3c, size 0, source 1 (timing_0)
...
Timed-out        Configure 00a8a5221a0f3b, size     0, for  remaining 0000000000000001, RoGs 0003, contract 0000000000000003, age 12012 ms, latency 12013 ms
```

These "Fixup Configure" warnings typically appear for multiple detectors across both `timing_0` and downstream devices, indicating a global timing desynchronization.

## 📋 Symptoms

- `Configure` transitions time out with 0-size contracts.
- `teb` logs show `<W> Fixup Configure` entries across many detectors, including `timing_0`.
- Timestamps from `timing_0` do not align with downstream detectors like HSD, CRIX, ANDOR, etc.

## 🔧 Recovery Procedure

1. **Open `xpmpva` GUI.**

2. **Issue `TxLinkReset` on the following tabs:**
   - **XPM 0 tab:** Click `TxLinkReset` for **XPM3**
   - **XPM 3 tab:** Click `TxLinkReset` for **XPM5**

3. **Wait for link re-synchronization.**
   - Monitor the TEB logs to confirm that subsequent `Configure` attempts proceed without "Fixup" or timeout warnings.

4. **Re-issue `Configure` transition.**

## 🧠 Notes

- This issue may occur after timing network reconfiguration, power cycle, or when an upstream XPM loses sync.
- `TxLinkReset` clears the stale or desynced state and forces a clean handoff of timing information.
- This procedure avoids a full DAQ reboot in most cases.

