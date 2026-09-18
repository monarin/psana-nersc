
# epix10ka Test on ASC DAQ Node

This document describes how to test the epix10ka detector on the `daq-det-evr01` node, and current known issues.

## Setup and Test Steps

1. **SSH to the DAQ node**:
   ```bash
   ssh daq-det-evr01
   ```

2. **Run the DRP process**:
   ```bash
   ./launch_drp_test.sh
   ```

3. **In a separate terminal, SSH to det-daq**:
   Make sure your kerboros ticket is up-to-date.
   ```bash
   ssh det-daq -l detopr
   cd scripts
   procmgr start epix10ka.cnf
   ```

4. **Hardware Note**:
   - epix10ka (1kHz) is plugged into QSFP0 (left - lane 0)
   - Timing (DAQ:ASC:XPM:0 AMC0 Port 3) is plugged into QSFP1 (right - lane 1)
   - Location: ASC Lab (Ground Floor Room 1040)

## Dev GUI Commands

### KCU1500 Board GUI

To run KCU1500 devGui:
```bash
cd /cds/home/j/jumdz/lcls2-epix-hr-pcie/software
python scripts/devGui.py --dev /dev/datadev_0 --pgp4 1 --serverPort 9004 --pcieBoardType XilinxKcu1500
```

Or if the DAQ is running:
```bash
python -m pyrogue gui --server='localhost:9004'
```

### Camera GUI

To run the epixQuadDAQ GUI:
```bash
cd /cds/home/j/jumdz/epix-quad/software
python scripts/epixQuadDAQ.py --l 0 --dev /dev/datadev_0
```

Or if the DAQ is running:
```bash
python -m pyrogue gui --server='localhost:9103'
```

## Buffer Fix for Jumping Events

We encountered a `Jump in TimingHeader evtCounter`   
This was fixed by reloading the kernel module with updated buffer settings:

```bash
sudo rmmod datadev
sudo insmod /usr/local/sbin/datadev.ko cfgTxCount=4 cfgRxCount=1020 cfgSize=2097152 cfgMode=0x2
```

## Current Issues

1. **1kHz Run Issues**:
   - At 1kHz, DRP reports:
     ```
     Missing data: subframe[2] size 0
     ```
   - This suggests a data stream drop, possibly due to buffer underrun or firmware bottleneck.

2. **Pause/Resume Crash**:
   - Pausing the DRP process (e.g. from procmgr) correctly sets deadtime = 1.
   - But resuming the process causes a segfault:
     ```
     *** Error in `drp': corrupted size vs. prev_size: ...
     ```

## Additional Notes

- Timeout value was adjusted to match 1000 Hz operation:
  ```python
  # epixquad_config.py
  devPtr.EventBuilder.Timeout.set(int(156.25e6 / 1000))
  ```

  This shows as `0x2625a` in the `EventBuilder.Timeout` register.
