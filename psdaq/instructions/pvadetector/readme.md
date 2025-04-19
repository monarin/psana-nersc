# 📦 PvDetector Buffer Allocation Overview

This section documents the buffer allocations involved in setting up a large PvDetector (e.g., 5Mpix Axis camera at RIX producing ~74 MiB images). The memory architecture spans both the **PGP kernel driver** and **DRP user-space process**, with buffer size coordination critical for stable performance.

## 🖼️ Buffer Allocation Flow

![PvDetector Buffer Allocation Flow](/psdaq/images/PvDetector_Buffer_Allocation_Flow.png)

> *The example shows values used for RIX's Axis detector with image size ~74 MiB.*

---

## 📋 Buffer Summary Table

| **Buffer Type**        | **Component**              | **Set By**                                  | **Size**                                  | **Notes**                                                                 |
|------------------------|----------------------------|---------------------------------------------|-------------------------------------------|---------------------------------------------------------------------------|
| **DMA Buffers**        | PGP Kernel Driver          | `cfgRxCount` and `cfgSize`                  | `cfgRxCount × cfgSize`<br>e.g., `80 × 1MiB = 80MiB` | Must hold the entire image (no overrun). Acts as a ring buffer.           |
| **Pebble Buffers**     | `DrpBase::MemPool`         | `pebbleBufCount` and `pebbleBufSize` kwargs (`-k`) | e.g., `128 × 84MiB = 10.8GiB`             | Used by DRP process to store full datagrams. Count defaults to next power of 2 above `cfgRxCount`. |
| **Transition Buffers** | `PvaDetector::PvMonitor`   | Tied to `pebbleBufCount`                    | e.g., `128 × 74MiB = 9.2GiB`               | Cannot be resized directly; size taken from DRP dgram payload. Tied 1:1 with pebble count. |

---

## 🧠 Key Points

- The **PGP DMA Buffers** must be large enough to receive a single full image, otherwise the DMA engine will overrun and data loss will occur.
- The **Pebble Buffers** are user-space buffers used for event building. They are allocated in `DrpBase::MemPool`.
- The **Transition Buffers** are used internally by `PvaDetector::PvMonitor` for holding and staging PV data during acquisition. They are sized based on image payload and cannot be resized via kwargs.
- The buffer counts (`pebbleBufCount`) are typically set to a power-of-two value greater than `cfgRxCount` to avoid indexing and overflow issues.
