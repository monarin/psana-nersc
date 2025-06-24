# README_INSTALL.md

> _How to set up `munged`, `munge`, `unmunge`, and `slurmd` for a diskless node like `daq-det-evr01`._

## 🧱 Dependencies:
- Source of software bundle: Copied from a working RHEL-compatible node with full Slurm/Munge installation.
- Node: `daq-det-evr01` (diskless)
- Custom install directories used:
  - `$HOME/munge_tools/`
  - `$HOME/munged_bundle/`
  - `$HOME/slurmd_bundle/`

---

## 🔧 Step-by-step Installation:

### 1. 📦 Install Munge and Slurmd Binaries
From a working node (e.g., `drp-srcf-cmp002`):
```bash
# Assuming these dirs already exist and contain binaries/libraries:
scp -r /usr/sbin/munge /usr/sbin/unmunge /usr/sbin/munged monarin@daq-det-evr01:~/munge_tools/bin/
scp -r /usr/lib64/libmunge.so* monarin@daq-det-evr01:~/munge_tools/lib/

scp -r /usr/sbin/slurmd /usr/sbin/slurmstepd monarin@daq-det-evr01:~/slurmd_bundle/sbin/
scp -r /usr/lib64/slurm monarin@daq-det-evr01:~/slurmd_bundle/usr/lib64/slurm/
scp -r /usr/lib64/libslurm*.so* monarin@daq-det-evr01:~/slurmd_bundle/lib/
```

### 2. 🔐 Generate a Munge Key
```bash
cd ~/my-munge/
create-munge-key -f
```

### 3. 🗂️ Directory Structure on `daq-det-evr01`
Ensure the following structure:
```
~/munge_tools/bin/munge
~/munge_tools/lib/libmunge.so.2
~/slurmd_bundle/bin/slurmd
~/slurmd_bundle/sbin/slurmstepd
~/slurmd_bundle/usr/lib64/slurm/
~/slurmd_bundle/etc/slurm.conf
~/slurm_tmp/spool/         # Used for SpoolDir
```

### 4. 🧪 Test Munge
```bash
export LD_LIBRARY_PATH=$HOME/munge_tools/lib:$LD_LIBRARY_PATH
export PATH=$HOME/munge_tools/bin:$PATH
munge -n --socket=$HOME/my-munge/munge.socket | unmunge --socket=$HOME/my-munge/munge.socket
```

You should see a `STATUS: Success`.
