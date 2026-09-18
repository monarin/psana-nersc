# ePixQuad1kfps: 1600-byte or empty image subframe

This guide covers the UED ePix Quad on `drp-ued-cmp003` (`/dev/datadev_0`, usually PGP lane 0), and the older ASC standalone test that first documented a 1600-byte frame. Confirm the host, device, lane, and deployed software from the current DRP log before using any procedure below.

## Identify the failure

The ePix Quad DRP expects four DMA subframes. `subframe[2]` carries the image. In `psdaq/drp/EpixQuad.cc`, the DRP marks the event `MissingData` when this subframe is smaller than `4 * 176 * (2 * 192) = 270,336` bytes. Four 352-by-384 panels of 16-bit pixels contain 1,081,344 bytes of pixel data; packet headers can add to the observed stream size.

| Observation | Meaning and first check |
| --- | --- |
| `Missing data: subframe[2] size 1600` or camera `FrameSize = 1600` | An image stream is present but far too short. Check camera configuration and where the size first becomes 1600. |
| `Missing data: subframe[2] size 0` | An empty image subframe; use the separate [zero-byte guide](13_troubleshoot_zero_byte_image.md). |
| `Missing data: subframe count 3 [expected 4]` | A different failure: inspect KCU `AppLane[0].EventBuilder.Bypass`; see [the three-subframe guide](11_troubleshoot_missing_data_framcnt.md). |

A changing `FrameCnt` proves that stream frames complete, not that each frame contains a complete image. Changing XPM rate or EventBuilder timeout alone cannot repair a consistently short camera payload.

## Capture evidence before changing settings

1. Use logs from the same DAQ launch: `epixquad1kfps_0`, `control`, and `teb0`. The DRP header records the actual `-d` device, `-l` lane mask, release, and submodule directory. Note the exact error and whether Configure/Enable succeeded. A lane mask of `0x1` means PGP lane 0.
2. In the **camera GUI**, read `Top.RdoutStreamMonitoring.Ch[0].FrameCnt`, `FrameRate`, `FrameSize`, `FrameSizeMin`, and `FrameSizeMax` while frames arrive. The SURF stream monitor says its size fields are valid for non-interleaved AXI stream frames; compare them with the DRP message. Record `SystemRegs.AsicMask`, `SystemRegs.AdcTestDone`, `SystemRegs.AdcTestFailed`, carrier IDs, and any failed register read or write.
3. In the **KCU1500 GUI**, read `DevPcie.Application.AppLane[0].EventBuilder.Bypass`, `DataCnt[0..2]`, and `TimeoutDropCnt[0..2]`. For the LCLS-II four-subframe path, `Bypass` should be `0x0`. `Bypass = 0x4` points to the separate three-subframe problem. Check timing receiver `RxLinkUp` and error counters if the timing stream is missing.
4. Compare the two size observations. If the camera monitor already reads 1600, investigate the camera configuration first. If the camera shows a full frame but DRP sees 0 or 1600, investigate the PGP/KCU event-builder path. Do not infer the root cause from a single counter.

For example, the UED DRP log from **2026-09-17 15:33:27** on `drp-ued-cmp003` repeatedly reported `subframe[2] size 0` immediately after Enable. Other launches that day reported ADC test failures/timeouts, invalid `CarrierId` reads, or an `AsicMask` write verification error. These are separate evidence of camera startup/communication trouble; see the [zero-byte guide](13_troubleshoot_zero_byte_image.md). The logs do not prove that the old YAML caused the zero-byte events.

## Recover the historical 1600-byte camera state

The [ASC standalone instructions](../setup/03_epix10ka_1khz_standalone_no_daq.md) record that loading `epixQuad_ASICs_allAsics_UED_1080Hz_settings.yml` reduced the camera frame size to 1600 bytes. Do not load that old/manual YAML during this test. Use the detector's current approved base configuration or DAQ configDB settings instead.

1. Record the current firmware identity and relevant camera settings before resetting anything. Stop the Quad DAQ run and close direct devGuis that own `/dev/datadev_0` before launching a different owner; `fuser -v /dev/datadev_0` can show remaining users.
2. Return the camera to the approved base state using the site's normal Quad reboot/reload procedure, then start the camera GUI **without loading the old YAML**. A GUI restart alone may preserve settings already written to hardware.
3. Apply only the current approved settings for the chosen UED/ASC setup. If DAQ owns the device, let DAQ Configure apply its configDB settings; do not run a standalone GUI simultaneously against the same virtual channels.
4. At a known-good trigger rate, verify camera `FrameCnt` increases and `FrameSize` is back near a full image, not 1600. Verify KCU EventBuilder receives the expected streams and the next DRP launch stops reporting short `subframe[2]` data. Check `control` and `teb0` from that same launch.

If the image remains 1600 bytes after a clean base startup, check `AsicMask` readback, `AdcTestDone`/`AdcTestFailed`, carrier IDs, and register transaction errors before another reset. Repeated ADC timeout, all-ones carrier IDs, or `AsicMask` verify errors call for detector/firmware owner investigation; see the [AsicMask Configure guide](14_troubleshoot_asicmask_configure.md). Do not treat a firmware flash as a routine frame-size reset.

## Firmware reload versus PROM programming

`epixQuadLoadFpga.py` in the readable 2025 ePix Quad software **requires `--mcs`**. It calls `CypressS25Fl.LoadMcsFile(...)` to program the Quad PROM and then `AxiVersion.FpgaReload()`. Thus the historical short command `python scripts/epixQuadLoadFpga.py --l 0` was incomplete for that script version; the [2025 deployment note](../deployments/10_UED_ePixQuad1kfps_Deployment_20251104.md) now shows the required argument. The target host's deployed script and firmware image must be checked before any firmware operation. KCU1500 `.mcs` files are a different device and must never be supplied to the Quad loader.

A firmware update needs the detector owner to select and verify the exact Quad `.mcs` image, preserve calibration information, and follow the approved post-update ADC training procedure. See the [ADC calibration guide](07_troubleshoot_calibration_mismatch.md). A reload from the existing PROM or a controlled detector reboot can be considered after confirming its image/version; neither guarantees that the underlying 1600-byte setting or a zero-byte stream is fixed.

## References

- [Three-subframe EventBuilder bypass diagnosis](11_troubleshoot_missing_data_framcnt.md)
- [ASC standalone test and old-YAML warning](../setup/03_epix10ka_1khz_standalone_no_daq.md)
- `lcls2/psdaq/drp/EpixQuad.cc` for the DRP's subframe checks
- ePix Quad `Top.py` and SURF `_AxiStreamMonAxiL.py` in the deployed `epix-quad-1kfps` submodule for camera stream-monitor registers
