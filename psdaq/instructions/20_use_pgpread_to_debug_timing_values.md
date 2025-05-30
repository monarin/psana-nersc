# Timing Debug with `pgpread`

This README describes how to use `pgpread` and supporting tools to debug timing-related issues in the DAQ system, especially when `Configure` or `L1Accept` transitions are missing or inconsistent.

---

## 🧩 Timing Node Schematic

```
                                                              drp-neh-cmp001
[ xpm 11 amc 1 port 0 ] --> (4-lane fiber pair) --> [ kcu bus a datadev_0 --- lane 0 ] *         
                                                                           --- lane 1
                                                                           --- lane 2
                                                                           --- lane 3
                                                           bus b datadev_1 --- lane 4 (optional)
                                                                           --- lane 5
                                                                           --- lane 6
                                                                           --- lane 7
* Each lane is split by switch and carries 4 virtual channels (VC)
```

For detectors, the fiber pair maps to either `datadev_0` or `datadev_1` directly, with VC routing defined in detector settings.

---

## 🔧 Running `pgpread` for Debug

### 1. Start `groupca` for XPM 11 Group 0

```bash
groupca DAQ:NEH 11 0
```

### 2. Launch `pgpread` on the Timing Node

```bash
~/lcls2/psdaq/build/drp/pgpread -d /dev/datadev_1
```

### 3. Trigger Transitions in GroupCA

Go to the **Transitions** tab in `groupca` and click **Configure** a few times. You should see output like this:

```
Size 288 B | Dest 1.0 | Transition id 2 | pulse id 7873554013149 | event counter 4 | index 105706
env 02080001 | payload ...
```

Each entry indicates a transition event for a lane and VC.

---

## ⚙️ Enable Lanes with `kcuSim`

To enable all 8 lanes for test/debug purposes:

```bash
kcuSim -C 0,0,0xff
```

> Format: `-C <group>,<length>,<lane_mask>`

Check status with:

```bash
kcuSim -s
```

> Note:  
> - **Right 4 columns** = `datadev_0`  
> - **Left 4 columns** = `datadev_1`

---

## 🛠 Troubleshooting

### Problem: No Transitions or L1Accept Events?

If `pgpread` shows no output when triggering transitions:

1. Open the **Events** tab in `groupca`
2. Click the **Clear** button

This resets internal counters and may restore visibility of events in `pgpread`.

---

## 🧠 Additional Notes

- `pgpread` helps verify presence of transitions (e.g., `Configure`, `Enable`, `L1Accept`) and lane activity.
- Make sure you're using the correct `datadev` path (`/dev/datadev_0` or `/dev/datadev_1`).
- Check fiber and VC routing if some lanes are missing events.

---


