
# Testing `calib_prefetch` at MFX DAQ

## 1. Setup and Initial Test Run

- **DAQ Setup**: At the MFX DAQ, select all `jungfrau_0` to `jungfrau_4` (5 detector instances), totaling **32 segments**.
- **AMI Prefetch**: Ensure that `ami_prefetch` is enabled.
- **Initial Run**: Start a normal DAQ run **(no need to record)**.
  - Observe the output from `ami-node-N` log file.
  - The **first run will be slow** since there's no `calibconst.pkl` in `/dev/shm` yet.

## 2. Re-Run (Cached Load)

- **Repeat the DAQ run**.
- This time, it should **start much faster**.
- Confirm that there is **no warning** like `existing_info doesn't match with latest_info` from `ami-node`.

## 3. Dark Run (Pedestal Scan)

Run the following command:

```bash
jungfrau_pedestal_scan --record 0 --hutch mfx -p 0 -g 1 -v -t 10000 -C drp-srcf-cmp014
```

### Explanation of Flags:
- `--record 0`: Run without writing XTC data.
- `--hutch mfx`: Target the MFX hutch.
- `-p 0`: Platform number.
- `-g 1`: Gain mode.
- `-v`: Verbose output.
- `-t 10000`: Number of events to collect.
- `-C drp-srcf-cmp014`: Use compute node `drp-srcf-cmp014`.

After this step, a new `calibconst.pkl` will be generated on the **AMI node**, e.g. `drp-srcf-mon005`. You can check with:

```bash
ls -lt /dev/shm/*.pkl
```

Check the **modified time** to confirm it was updated.

## 4. Final Re-Run with Dark Calibration

- Start the DAQ again after the dark run.
- `ami-node` should not print warnings about mismatched `existing_info` vs `latest_info`.

## 5. Notes on Turning On Jungfrau Detector

To enable the detector:

```bash
/cds/group/pcds/epics-dev/ddamiani/ioc/common/jungfrau4m/current/children/build/iocBoot/ioc-mfx-jf16m/edm-ioc-mfx-jf16m.cmd
```

Then in the EDM GUI, **click the "On/Off" button** to power on the detector.
