# UED ePixQuad: `subframe[2] size 0`

**Status (2026-09-17): unresolved.** A Quad restart or a corrected UED timing sequence might help, but neither is established as the cause or a reliable fix. This guide records what to compare before and after a change.

## Exact symptom and evidence

The DRP prints:

```text
Missing data: subframe[2] size 0
```

The 2026-09-17 15:33:27 launch on `drp-ued-cmp003` used `/dev/datadev_0`, lane mask `0x1` (PGP lane 0), and `timebase=119M`. Its detector log has `Adc Test Failed - restarting!` at line 1694, `Adc Test Timedout` at 1695, then repeated zero-byte errors beginning at line 2903 immediately after Enable. Configure completed; the image data was empty when the event path ran. The matching TEB and control logs did not identify a prior Configure failure. A second launch at 14:41:36 also logged zero-byte image subframes.

Log example:

```text
/sdf/home/u/uedopr/daq/logs/2026/09/17_15:33:27_drp-ued-cmp003:epixquad1kfps_0.log
```

`psdaq/drp/EpixQuad.cc` expects four subframes and treats subframe 2 as the image. A zero-byte image is different from a 1600-byte short image or a **three-subframe** event. A camera GUI `FrameSize=0` is a separate stream-monitor reading; if its `FrameCnt` is not advancing, zero can simply mean no completed frame has been measured. Compare both counters with the DRP log. See [1600-byte images](12_troubleshoot_1600_byte_frame.md) and [three-subframe EventBuilder bypass](11_troubleshoot_missing_data_framcnt.md). The ADC warnings are another finding, but the logs alone do not establish which fault caused the empty image. The checked-in `epixquad1kfps_config.py` calls `_checkADCs()` without using its return value, so an ADC timeout can be followed by a completed Configure.

## Read-only checks

1. Compare the `epixquad1kfps_0`, `control`, and `teb0` logs from one launch. Identify the first failure and whether the DAQ reached Configure and Enable. The DRP header gives the actual device, lane, release, and submodule bundle.
2. In the camera GUI, read `Top.RdoutStreamMonitoring.Ch[0].FrameCnt`, `FrameRate`, `FrameSize`, `FrameSizeMin`, and `FrameSizeMax` while triggers arrive. Also read `SystemRegs.AdcTestDone`, `AdcTestFailed`, `AsicMask`, carrier IDs, `RdoutCore.RdoutEn`, and register errors. A rising `FrameCnt` alone does not prove image pixels are present.
3. In the KCU1500 GUI, read `DevPcie.Application.AppLane[0].EventBuilder` counters, `Bypass`, and timing receiver `RxLinkUp`/error counters. `Bypass=0x4` belongs to the separate three-subframe diagnosis; `Bypass=0x0` is expected for this LCLS-II path.
4. Check the UED XPM/sequence selected for the test and partition 0 input/accepted rates. The Quad needs the UED timing sequence for its DAQ/readout triggers. The Andor 1 Hz sequence is not suitable for a Quad 360 Hz test. The Quad's continuous run trigger and its DAQ trigger are separate in the 1kfps configuration; compare both with the current deployment settings rather than changing the readout rate alone.

## Controlled recovery experiments

- **Timing hypothesis:** UED operators report `ued_seq --a360` as the command to select the 360 Hz sequence from the `uedopr` account on `ued-daq`. Before running it, identify the installed command with `type ued_seq` and inspect `ued_seq --help`; this exact wrapper was not found in the checked-in `lcls2` source. Run it only for an approved UED timing change, since it changes live XPM sequencing and may affect other detectors. Then confirm the selected sequence, partition 0 readout rate near 360 Hz, and the Quad's separate run-trigger rate.
- **Quad startup hypothesis:** after recording the failing state, use the site's approved Quad restart procedure with the DAQ stopped and direct GUIs closed. Confirm device ownership before opening a new GUI or DAQ process. A restart can expose a different failure, including the [AsicMask Configure error](14_troubleshoot_asicmask_configure.md); record the new first error rather than assuming the empty-frame problem is fixed.

A successful trial needs camera `FrameSize` near a full image (about 1 MiB), no new `subframe[2] size 0` errors, and healthy matched TEB/control logs at the intended rate. Record the sequence, trigger counters, camera counters, firmware identity, and log group for both the failing and recovered state. There is no confirmed working solution yet.
