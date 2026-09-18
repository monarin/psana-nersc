# ePixQuad 1 kfps Missing Data Troubleshoot

Date investigated: 2026-05-06

Log file:

```text
/cds/home/opr/uedopr/2026/05/06_09:14:07_drp-ued-cmp003:epixquad1kfps_0.log
```

## Symptom

The DAQ reported damage even though the detector GUI showed `FramCnt` increasing.
The repeated DRP error was:

```text
Missing data: subframe count 3 [expected 4]
```

In this log, the error appeared immediately after `Enable` and repeated for essentially every event.

## What The Error Means

The error is emitted by `psdaq/drp/EpixQuad.cc`.
The ePixQuad DRP event path expects four subframes, but the event builder output only contained three.
When the subframe count does not match, the DRP marks the event with `Damage::MissingData`.

The relevant firmware path is the KCU1500 `DevPcie.Application.AppLane[0].EventBuilder`.

## Key devGui Evidence

In the KCU1500 devGui, under:

```text
DevPcie.Application.AppLane[0].EventBuilder
```

the observed counters were:

```text
DataCnt[0]          non-zero
DataCnt[1]          non-zero
DataCnt[2]          0x0
TimeoutDropCnt[2]   non-zero
Bypass              0x4
NUM_SLAVES_G        3
```

`DataCnt[2] = 0x0` means EventBuilder input 2 was not being accepted/forwarded.
For this AppLane firmware, input 2 is the XPM/event timing message stream.
With `Bypass = 0x4`, bit 2 is set, so input 2 is bypassed. That prevents the timing-message subframe from appearing in the output, leaving the DRP with only three subframes.

## Likely Cause

The normal LCLS-II default for the KCU EventBuilder should have `Bypass = 0x0`.
For the `epixquad1kfps` config path, `DevRoot` is created with the default YAML files disabled, so this setting can depend on stale or reset KCU state.

If `Bypass` remains at `0x4`, the DAQ can produce:

```text
Missing data: subframe count 3 [expected 4]
```

even though the camera frame counter is increasing.

## Recovery If This Happens Again

Use the KCU1500 devGui and go to:

```text
DevPcie.Application.AppLane[0].EventBuilder
```

Set:

```text
Bypass = 0x0
```

Then reset/restart the event builder for the next run, for example with `SoftRst` or the normal stop/start run sequence, and confirm:

```text
DataCnt[2] increments
TimeoutDropCnt[2] stops increasing event-for-event
DRP no longer prints "Missing data: subframe count 3 [expected 4]"
```

## Code Fix Applied Locally

The local config was updated to force the KCU EventBuilder bypass mask during init:

```python
devPtr.EventBuilder.Bypass.set(0x0)
```

File:

```text
psdaq/psdaq/configdb/epixquad1kfps_config.py
```

This makes the `epixquad1kfps` path explicitly configure the LCLS-II EventBuilder bypass state instead of relying on previous KCU state.
