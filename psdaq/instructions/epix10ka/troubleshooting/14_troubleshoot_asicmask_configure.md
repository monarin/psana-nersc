# UED ePixQuad: `AsicMask` verification failure during Configure

**Status (2026-09-17): likely write-key mismatch in the readable 2025 Quad firmware; the exact deployed firmware and recovery procedure have not been verified.** Do not treat a passing Configure as proof that image readout is healthy.

## Exact failure

The 2026-09-17 15:48:44 detector log on `drp-ued-cmp003` contains:

```text
INFO:root:Setting cbase.SystemRegs.AsicMask to 65535
ERROR:pyrogue.Variable.RemoteVariable.Top.SystemRegs.AsicMask:Block::checkTransaction: General Error: Verify error for block Top.SystemRegs.AsicMask with address 0x00100028. Byte: 0. Got: 0x00, Exp: 0xff, Mask: 0xff
```

PyRogue retries the write four times (`Try 0` through `Try 3`), then Configure aborts with a Python error. `Got: 0x00` describes byte 0 of the readback; the log does not show every byte of the register. Matching log:

```text
/sdf/home/u/uedopr/daq/logs/2026/09/17_15:48:44_drp-ued-cmp003:epixquad1kfps_0.log
```

The ConfigDb template in `psdaq/psdaq/configdb/epixquad_config_store.py` sets `expert.EpixQuad.SystemRegs.AsicMask` to `0xffff` (`65535`, type `UINT16`). During Configure, `epixquad1kfps_config.py` calls `config_expert()` → `apply_dict()` → `retry(rogue_node.set, value)`. There is no explicit check in this code to skip the call when the mask already reads `0xffff`. For example, the 17:13:28 launch also logged `Setting cbase.SystemRegs.AsicMask to 65535` and continued past that point. A good pre-existing mask may let verification pass, but it does not stop DAQ from calling `.set()`.

## Why the write may be ignored

The readable ePix Quad software model defines `SystemRegs.AsicMask` as a 32-bit **RW** variable and describes it as set by the MicroBlaze ASIC auto-detect function. Therefore Dan's suggestion that it behaves as read-only is plausible operationally, but it is not declared read-only in this PyRogue model.

More specifically, the readable 2025 `epix-quad-1kfps/firmware/common/EpixQuadCommon/rtl/SystemRegs.vhd` handles address `0x028` with a write shadow (`asicMaskReg`) and a 16-bit readback (`asicMask`). The effective mask updates **only if bits 31:16 of the written word are `0xAAAA`**; bits 15:0 become the new mask. The normal power-up mask is `0x0000` in non-simulation builds. A DAQ write of `0x0000FFFF` lacks the key, so this RTL predicts that a zero mask stays zero and PyRogue verification fails. Confirm that the deployed firmware still uses this logic before treating it as the root cause.

The keyed word corresponding to a 16-ASIC mask is `0xAAAAFFFF`, but this is **not a ready-to-run GUI instruction**: the register reads back the effective 16-bit mask, not the key, so an ordinary 32-bit PyRogue verified write of that word may itself report a mismatch. Dan described a devGui action that produces the correct mask; its exact control, value, and required order have not been recorded. This RTL write shadow may explain that action, but the GUI procedure still needs confirmation.

## What to check and record

1. Before Configure, read `Top.SystemRegs.AsicMask` in the camera GUI. Record the value, firmware version/git hash, carrier IDs, ADC startup status, and detector power/interlock state. After a Quad restart on 2026-09-17, some launches also showed all-ones carrier IDs or ADC test timeouts; these indicate broader startup trouble and should be investigated with the mask.
2. Confirm the active ConfigDb value is `0xffff`/65535 and the deployed `epixquad1kfps_config.py` still writes it through `apply_dict()`. The ConfigDb type (`UINT16`) and the PyRogue variable width (`UInt32`) are different, but the specific failure is the readback mismatch at byte 0; the RTL write key is a concrete explanation to test.
3. Ask Dan or the detector firmware owner for the exact devGui register action and the expected **before/after readback**. Record whether the action uses a raw unverified write, a command, or a different register. Avoid guessing at other controls or repeatedly retrying Configure against a zero mask.
4. After an approved correction, verify `AsicMask=0xffff` by readback, then try a fresh Configure and inspect the detector, control, and TEB logs. Confirm full image frames separately; a passing mask write does not resolve `subframe[2] size 0` by itself.

A proposed code fix would need to honor the firmware key and verify the effective 16-bit readback, or omit a redundant mask write only after establishing that firmware auto-detect produced the desired mask. Neither change has been tested against the deployed Quad, and this guide does not direct a live register or ConfigDb change.
