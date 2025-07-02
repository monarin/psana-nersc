
# 📐 Timing Delay Calculation: `start_ns` and `triggerDelay`

In the LCLS timing system, delays are defined in **ticks**, where each tick represents a clock cycle. The `triggerDelay` parameter specifies **how many ticks after the start of a timing message** the system should issue a trigger to the detector.

---

## 🧮 Tick Duration per Clock Frequency

| Timing System | Frequency | Tick Duration (ns) |
|---------------|-----------|--------------------|
| LCLS-I        | 119 MHz   | 8.4 ns             |
| LCLS-II       | 186 MHz   | 5.37 ns            |

---

## 🧠 Key Variables

- `start_ns`: The nanoseconds to wait after receiving a timing message before sending a trigger.
- `partitionDelay`: The number of ticks it takes for a trigger message to propagate through the system.
- `triggerDelay`: How many ticks after the message the trigger should be sent (must be ≥ 0).

```python
triggerDelay = int(start_ns / tick_duration) - partitionDelay
```

If `triggerDelay < 0`, you'll get an error because the trigger would have to be sent **before** the message arrives — which is obviously too ambitious.

---

## 💡 Example Calculations

Let’s say `partitionDelay = 18200` ticks.

### For LCLS-II (186 MHz):
- Tick = 5.37 ns
- `start_ns = 99000`
- Ticks after message = 99000 / 5.37 ≈ **18435**
- `triggerDelay = 18435 - 18200 = 235 ticks ✅`

### For LCLS-I (119 MHz):
- Tick = 8.4 ns
- `start_ns = 99000`
- Ticks after message = 99000 / 8.4 ≈ **11785**
- `triggerDelay = 11785 - 18200 = -6415 ❌` (not enough delay)

So, for **LCLS-I**, you’d need a **larger `start_ns`** to avoid a negative `triggerDelay`.

---

## 🧷 Notes

- Choosing `start_ns` too small will cause `ValueError: triggerDelay computes to < 0`.
- Choosing it too large adds unnecessary latency.
- You can tune this to account for firmware or system-level delays (like XPM pause threshold or data alignment time).
