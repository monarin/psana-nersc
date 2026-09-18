# ePix10ka / ePixQuad 1kfps notes

Start here for ASC standalone tests and UED DAQ operation. The ASC setup notes and UED deployment notes describe different hosts and software generations; confirm the current DRP log header before using a command. The dated deployment files are historical records.

## Find the symptom

| What you see | Guide | Status |
| --- | --- | --- |
| `subframe[2] size 0` / camera `FrameSize = 0` | [Empty image subframe](troubleshooting/13_troubleshoot_zero_byte_image.md) | Open; compare UED timing, ADC/readout, and restart evidence |
| `subframe[2] size 1600` / camera `FrameSize = 1600` | [1600-byte image](troubleshooting/12_troubleshoot_1600_byte_frame.md) | Historical old-YAML cause documented |
| `subframe count 3 [expected 4]` | [KCU EventBuilder bypass](troubleshooting/11_troubleshoot_missing_data_framcnt.md) | `Bypass=0x4` case documented |
| `AsicMask` verify error during Configure | [AsicMask Configure failure](troubleshooting/14_troubleshoot_asicmask_configure.md) | RTL write-key hypothesis; live fix unverified |
| Quad fails to start / AxiVersion timeout | [Startup failure](troubleshooting/01_troubleshoot_fail_to_start.md) | Historical ASC note |
| Calibration GitHash mismatch | [ADC calibration mismatch](troubleshooting/07_troubleshoot_calibration_mismatch.md) | Historical procedure |

## Setup and operations

- [ASC 1 kHz overview (2025)](setup/asc_1khz_overview_2025.md)
- [ASC DAQ test and setup](setup/02_test_and_setup_at_ASC.md)
- [Standalone camera and KCU devGuis](setup/03_epix10ka_1khz_standalone_no_daq.md)
- [Switch KCU configuration](setup/04_switch_kcu_for_epix10ka.md)
- [Update 1kfps submodules](setup/05_update_submodules_1kfps.md)
- [UED MPOD and IOC guide](setup/09_ePix_UED_MPOD_IOC_Guide.md)

## Deployment history

- [UED 360/1080 Hz deployment, 2025-10-06](deployments/08_UED_ePixQuad_360_1080_Deploy_2025-10-06.md)
- [UED ePixQuad1kfps deployment, 2025-11-04](deployments/10_UED_ePixQuad1kfps_Deployment_20251104.md)

## Reference and support files

- [Trigger delay explanation](reference/00_understand_trigger_delay.md)
- [ASC procmgr config](epix10ka.cnf) and [DRP launch script](launch_drp_test.sh)

For the UED 360 Hz Quad test, the UED operator reports using `ued_seq --a360` on `ued-daq`. The Andor 1 Hz timing sequence is not suitable for the Quad. See the [empty-image guide](troubleshooting/13_troubleshoot_zero_byte_image.md) for checks and the limits of what has been verified.
