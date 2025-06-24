# README_USAGE.md

> _How to launch Munge and Slurmd on `daq-det-evr01` (diskless node) after a reboot or new session._

## ✅ Startup Steps

### 1. 🔧 Set Environment
```bash
export LD_LIBRARY_PATH=$HOME/slurmd_bundle/lib:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=$HOME/munge_tools/lib:$LD_LIBRARY_PATH
export PATH=$HOME/munge_tools/bin:$PATH
```

### 2. 🔐 Run Munge (non-root, socket in user dir)
```bash
munged \
  --key-file=$HOME/my-munge/munge.key \
  --socket=$HOME/my-munge/munge.socket \
  --pid-file=$HOME/my-munge/munged.pid \
  --log-file=$HOME/my-munge/munged.log \
  --seed-file=$HOME/my-munge/munge.seed &
```

Verify it's working:
```bash
munge -n --socket=$HOME/my-munge/munge.socket | unmunge --socket=$HOME/my-munge/munge.socket
```

---

### 3. 🚀 Start `slurmd`
```bash
sudo LD_LIBRARY_PATH=$HOME/slurmd_bundle/lib:$HOME/munge_tools/lib \
  $HOME/slurmd_bundle/bin/slurmd \
  -Dvvv \
  -f $HOME/slurmd_bundle/etc/slurm.conf \
  -d $HOME/slurmd_bundle/sbin/slurmstepd
```

---

## 🛠️ Notes on `slurm.conf`

```ini
# slurm.conf (local override for daq-det-evr01)
AuthInfo=socket=/cds/home/m/monarin/my-munge/munge.socket
PluginDir=/cds/home/m/monarin/slurmd_bundle/usr/lib64/slurm
SlurmdPidFile=/cds/home/m/monarin/slurm_tmp/slurmd.pid
SlurmdSpoolDir=/cds/home/m/monarin/slurm_tmp/spool
SlurmdLogFile=/cds/home/m/monarin/slurm_tmp/slurmd.log
ProctrackType=proctrack/linuxproc
#PrologFlags=X11   # <-- comment this for proctrack/linuxproc

NodeName=daq-det-evr01 NodeAddr=172.21.58.78 CPUs=12 RealMemory=12002 Sockets=2 CoresPerSocket=6 ThreadsPerCore=1

PartitionName=drpq Default=YES Nodes=daq-det-evr01,drp-srcf-cmp[001-056],...
```

> ✅ `NodeName` and `PartitionName` were also added to the central `slurm.conf` on `psslurm-drp` so jobs can be scheduled onto `daq-det-evr01`.
