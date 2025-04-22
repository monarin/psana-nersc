# 📦 PvDetector Buffer Allocation Overview

This section documents the buffer allocations involved in setting up a large PvDetector (e.g., 5Mpix Axis camera at RIX producing ~74 MiB images). The memory architecture spans both the **PGP kernel driver** and **DRP user-space process**, with buffer size coordination critical for stable performance.

## 🖼️ Buffer Allocation Flow

![PvDetector Buffer Allocation Flow](/psdaq/images/PvDetector_Buffer_Allocation_Flow.png)

> *The example shows values used for RIX's Axis detector with image size ~74 MiB.*

---

## 📋 Buffer Summary Table

| **Buffer Type**        | **Component**              | **Set By**                                  | **Size**                                  | **Notes**                                                                 |
|------------------------|----------------------------|---------------------------------------------|-------------------------------------------|---------------------------------------------------------------------------|
| **DMA Buffers**        | PGP Kernel Driver          | `cfgRxCount` and `cfgSize`                  | `cfgRxCount × cfgSize`<br>e.g., `80 × 4KB = 320KB` | Must hold the data rate. **For PVA Detector this is just TimingHeaders (32 B + 32 B of ‘overhead’)**. Acts as a ring buffer.           |
| **Pebble Buffers**     | `DrpBase::MemPool`         | `pebbleBufCount` and `pebbleBufSize` kwargs (`-k`) | e.g., `128 × 84MiB = 10.8GiB`             | Used by DRP process to store full datagrams. Count defaults to next power of 2 above `cfgRxCount`. |
| **Transition Buffers** | `PvaDetector::PvMonitor`   | Tied to `pebbleBufCount`                    | e.g., `128 × 74MiB = 9.2GiB`               | Cannot be resized directly; size taken from DRP dgram payload. Tied 1:1 with pebble count. |

---

## 🧠 Key Points

- The **PGP DMA Buffers** must be large enough to receive a single full image header, otherwise the DMA engine will overrun and data loss will occur.
- The **Pebble Buffers** are user-space buffers used for event building. They are allocated in `DrpBase::MemPool`.
- The **Transition Buffers** are used internally by `PvaDetector::PvMonitor` for holding and staging PV data during acquisition. They are sized based on image payload and cannot be resized via kwargs.
- The buffer counts (`pebbleBufCount`) are typically set to a power-of-two value greater than `cfgRxCount` to avoid indexing and overflow issues.

# PvDetector Buffer Allocation and Asymmetry

## 🧠 Understanding Buffer Allocation Differences

In the DAQ system, buffer allocation strategies differ between PGP and PVA detectors:

| Aspect                    | **PGP Detectors**                          | **PVA Detectors**                               |
|---------------------------|--------------------------------------------|-------------------------------------------------|
| **Data Ingress**          | Via KCU1500 (PGP link)                     | Via network protocols (e.g., EPICS PV, UDP)     |
| **DMA Buffer Usage**      | Stores full image data                     | Stores only TimingHeader (~64 bytes)            |
| **Required `cfgSize`**    | Must accommodate full image size           | Can be minimal (e.g., 4 KB)                     |
| **Pebble Buffer Role**    | Receives data from DMA buffers             | Directly receives full image data               |
| **Pebble Buffer Sizing**  | Optional; depends on DMA buffer size       | Crucial; must fit entire image                  |

For PVA detectors, since the image data bypasses the DMA buffers, it's essential to configure `pebbleBufSize` to accommodate the full image size. Conversely, `cfgSize` can remain small, as it's only used for the TimingHeader.

## ⚖️ Asymmetry Between DMA and Pebble Buffers

One important design detail in the DAQ system is the **asymmetry** between how **DMA buffers** and **pebble buffers** are used:

| Aspect              | **DMA Buffers**                              | **Pebble Buffers**                              |
|---------------------|-----------------------------------------------|--------------------------------------------------|
| **Created by**      | Device driver (`cfgRxCount`, `cfgSize`)       | User-space via `pebble.create()`                |
| **Purpose**         | Streaming image fragments via PGP             | Holding a full event (image + metadata)         |
| **Size per buffer** | Small (e.g., 1 MiB)                            | Large (e.g., full image size, e.g., 84 MiB)      |
| **Usage**           | One image spans multiple DMA buffers          | One image fits entirely in one pebble buffer    |
| **Mapping**         | Many DMA buffers per image                    | One pebble buffer per image                     |
| **Memory location** | Kernel-mapped (hardware DMA)                  | User-space (DAQ process)                        |

### 🔍 Why This Matters

- The number of **pebble buffers** is directly tied to the number of DMA buffers (`cfgRxCount`) to ensure every in-flight DMA event has a matching location in user-space memory.
- **Pebble and transition buffers are large**, so increasing `cfgRxCount` (e.g., from 64 → 2048) without caution can lead to **massive memory allocation** (e.g., hundreds of GB).
- To avoid buffer overrun and excessive memory use, you must **balance**:
  - `cfgRxCount × cfgSize` ≥ one image (so DMA doesn’t overflow)
  - `pebbleBufCount × pebbleBufSize` fits in system memory

### 💡 Pro Tip

If you’re handling large images (e.g., 84 MiB), try to **keep `cfgRxCount` low** (just enough to hold one image) and **use `pebbleBufCount`** to control the number of concurrent events. This avoids allocating unnecessary large buffer regions while still ensuring safe operation.
