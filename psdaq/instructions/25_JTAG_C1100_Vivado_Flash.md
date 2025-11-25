# C1100 JTAG Firmware Flash (drp-srcf-gpu005)

Step-by-step notes for flashing C1100 cards with Vivado on `drp-srcf-gpu005`.

## One-time: install JTAG cable drivers
1. Disconnect all JTAG cables.
2. Run:
   ```bash
   cd /sdf/group/faders/tools/xilinx/2024.2/Vivado/2024.2/data/xicom/cable_drivers/lin64/install_script/install_drivers/
   sudo ./install_drivers
   ```
3. When finished, unplug/replug the JTAG pod to apply udev rules.

## Per-session setup (every time you log in)
1. SSH with X forwarding to the GPU node:
   ```bash
   ssh -X drp-srcf-gpu005
   ```
2. Work around the missing `libtinfo.so.5`:
   ```bash
   mkdir -p ~/vivado-libs
   ln -sf /lib64/libtinfo.so.6 ~/vivado-libs/libtinfo.so.5
   export LD_LIBRARY_PATH=~/vivado-libs:$LD_LIBRARY_PATH
   ```
3. Source Vivado:
   ```bash
   source /sdf/group/faders/tools/xilinx/2024.2/Vivado/2024.2/settings64.sh
   ```
4. (Optional) Start a hardware server in a separate shell if you prefer:
   ```bash
   hw_server -s tcp::3121 &
   ```

## Per-card flashing
Repeat these steps for each C1100 card you need to program:
1. Physically move the JTAG pod to the target card, then unplug/replug the pod USB so it re-enumerates.
2. Start or reuse Vivado GUI (from the same X-forwarded shell where you set `LD_LIBRARY_PATH` and sourced settings):
   ```bash
   vivado &
   ```
3. In Vivado:
   - Open Hardware Manager → **Tools → Auto Connect** (or connect to `localhost:3121` if using a separate `hw_server`).
   - The C1100 device (e.g., `xcu50_u55n_0`) should appear under Hardware.
   - Right-click `xcu50_u55n_0` → **Add Configuration Memory Device**. In the search box type `mt25qu01g-spi-x1_x2_x4` and select that part.
   - Right-click the configuration memory → **Program Configuration Memory Device**.
   - Set the MCS file to:  
     `/sdf/home/m/monarin/firmware/c1100/XilinxVariumC1100Pgp4_10Gbps-0x03000000-20251028015459-ruckman-586133a.mcs`  
     (or whichever MCS you intend to load from that directory).
   - Enable erase/program/verify, then **OK** to flash. Wait for completion.
4. After programming finishes, move the JTAG pod to the next card, unplug/replug USB, then in Vivado use **Tools → Auto Connect** again and repeat from step 3. No need to restart Vivado unless the cable stops enumerating.

## Notes
- If the GUI fails to launch, re-check that `ssh -X` set `DISPLAY`, and that `LD_LIBRARY_PATH` includes the `libtinfo.so.5` shim above.
- If Vivado can’t see the JTAG cable, try another USB port and confirm it appears in `lsusb`.
- Already-flashed cards on this host are `datadev_0` (slot 2002, BDF 46:00.0) and `datadev_1` (slot 5009, BDF c0:00.0); `datadev_*`-missing cards still need flashing.
- Reference: https://confluence.slac.stanford.edu/spaces/ppareg/pages/610476085/Vivado+tips

