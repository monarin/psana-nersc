# epix10ka Integration for UED DAQ

This project documents the integration process of a 1kHz epix10ka detector into the UED DAQ system. The detector is currently hosted on `daq-det-evr01` with development GUIs and configuration tools available under the `lcls2-epix-hr-pcie` software tree.

---

## 📍 Detector Setup

- **Host node:** `daq-det-evr01`
- **PCIe Device Path:** `/dev/datadev_03`
- **KCU Type:** `XilinxKcu1500`

---

## 🚀 Dev GUIs

### KCU Board GUI

To launch the board-level development GUI:

```bash
python scripts/devGui.py --dev /dev/datadev_03 --pgp4 1 --serverPort 9004 --pcieBoardType XilinxKcu1500
```

**Location:**  
`/cds/home/j/jumdz/lcls2-epix-hr-pcie/software`

---

### Camera GUI

To launch the epix10ka QuadDAQ GUI:

```bash
python scripts/epixQuadDAQ.py --l 0 --dev /dev/datadev_03
```

**Location:**  
`/cds/home/j/jumdz/epix-quad/software`

Check FrameCnt and FrameRate registers  

![epix10ka frame count](/psdaq/instructions/epix10ka/ePix10ka_FrameCnt.png)

---

## 🛠 Status

| Component     | Host           | Status     |
|---------------|----------------|------------|
| epix10ka      | daq-det-evr01  | In Progress |
| devGui        | Installed      | ✅          |
| QuadDAQ GUI   | Installed      | ✅          |
| DAQ Pipeline  | Not Connected  | ❌          |

---

## 📝 Notes

- Update this README as new integration steps, issues, or configurations are discovered.
- Remember to verify DMA memory allocation and `pgp` lane configuration.
- Use `kcuStatus` or `rogue` tools to inspect link and hardware readiness.

---

## 📎 To Do

- [ ] Confirm detector data path in the UED DAQ system
- [ ] Integrate into DAQ configure JSONs
- [ ] Validate 1kHz operation with timing triggers
- [ ] Verify image data integrity and pedestal stability
- [ ] Connect to FFB and Smalldata pipeline
