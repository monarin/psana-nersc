# HSD Loopback Mode Recovery — RIX DAQ

This README describes how to detect and recover from an issue where an HSD link enters loopback mode unexpectedly, which can disrupt data acquisition and cause detector failures. The error in teb might look like this:
```
rix-teb[52826]: <W> Fixup Configure, 00a8a632c4c219, size 0, source 8 (hsd_3)
```

## 🛑 Problem Summary

Occasionally, an HSD link may enter **loopback mode** without any clear cause. This disrupts normal detector communication and data flow. The issue can be identified using the `kcuStatus` tool on the affected HSD node.

### Symptom

When running `kcuStatus`, you may observe non-zero loopback values like:

```
-- PgpAxiL Registers --
            loopback :        0        0        0        2        0        0        0        0
```

In this example, lane 3 (index 3) is stuck in loopback mode.

## 🔧 Recovery Procedure

1. **Login to the HSD node** where the issue was observed.

2. **Run `kcuStatus` to confirm loopback condition:**

   ```bash
   kcuStatus
   ```

3. **Reset loopback mode** by running:

   ```bash
   kcuStatus -l 0
   ```

   This clears loopback mode for all lanes.

4. **Verify status again**:

   ```bash
   kcuStatus
   ```

   All loopback values should now read `0`.

## 🧠 Notes

- The cause of entering loopback mode is not always obvious; this reset is a safe first-line fix.
- If the issue recurs frequently, escalate for hardware or firmware diagnostics.
- Resetting loopback does not disrupt other nodes or DAQ processes.

