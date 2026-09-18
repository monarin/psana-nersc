
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

- `start_ns`: The absolute trigger start time, in nanoseconds. This value is typically defined in the experiment setup.
- `clk_period`: Duration of a single timing tick in nanoseconds.
  - For 186 MHz: `clk_period = 1 / 186e6 = 5.37 ns`
  - For 119 MHz: `clk_period = 1 / 119e6 = 8.4 ns`
- `partitionDelay`: Number of ticks to account for message propagation and processing delay (fixed at 91 ticks).
- `msg_period`: Interval between messages (200 for 186M and 238 for 119M)
- `triggerDelay`: How many ticks the XPM should delay before sending the trigger.

## Calculation

The formula for calculating `triggerDelay` is:

```python
triggerDelay = int(rawStart / clk_period - partitionDelay * msg_period)
```

If `triggerDelay < 0`, you'll get an error because the trigger would have to be sent **before** the message arrives — which is obviously too ambitious.

---

## 💡 Example Calculations

#### 1. LCLS-II (186 MHz, clk_period = 5.37 ns)
To make triggerDelay > 0, use start_ns = 99000
```text
triggerDelay = int(99000 / 5.37 - 91 * 200)
             = int(18435.19 - 18200)
             = 235 ticks
```

#### 2. LCLS-I (119 MHz, clk_period = 8.4 ns)
To make triggerDelay > 0, use start_ns = 184000 
```text
triggerDelay = int(184000 / 8.4 - 91 * 238)
             = int(21904.76 - 21658)
             = 247 ticks 
```

---

## 🧷 Notes

- Choosing `start_ns` too small will cause `ValueError: triggerDelay computes to < 0`.
- Choosing it too large adds unnecessary latency.
- You can tune this to account for firmware or system-level delays (like XPM pause threshold or data alignment time).
