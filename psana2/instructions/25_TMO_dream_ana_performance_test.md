## 🔪 Dream Pipeline – Independent Test Setup (Mona)

**Goal:**  
Run the TMO Dream pre-processing pipeline in a **fully independent environment** (custom config, logs, and outputs) without interfering with the shared `/scratch/arp` runs.

---

### 📝 Environment Setup

#### 1. Create hybrid Dream environment
File: `~/lcls2/setup_env_dream.sh`

This environment:
- Activates the Dream conda environment
- Adds your local psana2 install for development
- Includes MPI/OpenMPI tools from `ps_20241122`
- Uses your private Dream config directory

```bash
source /sdf/group/lcls/ds/ana/sw/conda2-v4/inst/etc/profile.d/conda.sh
conda activate dream

# Add working psana + OpenMPI
export PATH=/sdf/group/lcls/ds/ana/sw/conda2/inst/envs/ps_20241122/bin:$PATH
export PYTHONPATH=/sdf/home/m/monarin/lcls2/install/lib/python3.9/site-packages:$PYTHONPATH
export CONFIGDIR=/sdf/data/lcls/ds/tmo/tmo101347825/scratch/mona/config/
```

Check:
```bash
which python
which mpirun
python -c "import psana; print(psana.__file__)"
```
✅ should show Dream’s python, psana from your local path, and mpirun from ps_20241122.

---

### ⚙️ 2. Custom Dream configuration

Copied from Xiang’s repo:
```
/sdf/home/x/xiangli/gitd/dream/config_live/
```
to:
```
/sdf/data/lcls/ds/tmo/tmo101347825/scratch/mona/config/
```

Then edited these YAMLs:
```yaml
h5:
  path1: /sdf/data/lcls/ds/tmo/
  path2: scratch/mona/h5/
log:
  path1: /sdf/data/lcls/ds/tmo/
  path2: scratch/mona/log/
```

✅ This ensures Dream writes to:
```
/sdf/data/lcls/ds/tmo/tmo101347825/scratch/mona/h5/
```
and logs to:
```
/sdf/data/lcls/ds/tmo/tmo101347825/scratch/mona/log/
```
(no overwriting shared `/scratch/arp` results)

---

### 🚀 3. Submission script – `preproc_dev_mona.sh`

Before running, go to the script directory:
```bash
cd /sdf/data/lcls/ds/tmo/tmo101347825/scratch/mona/sh
```

Then run:
```bash
./preproc_dev_mona.sh <experiment> <run>
```

#### Script contents:
```bash
#!/bin/bash
# Usage: ./preproc_dev_mona.sh <exp> <run>

EXP=$1
RUN=$2
LOGDIR="/sdf/data/lcls/ds/tmo/${EXP}/scratch/mona/log"
mkdir -p "$LOGDIR"

sbatch <<EOT
#!/bin/bash
#SBATCH --job-name=dream_${EXP}_${RUN}
#SBATCH --output=${LOGDIR}/%j.out
#SBATCH --error=${LOGDIR}/%j.err
#SBATCH --partition=milano
#SBATCH --account=lcls:${EXP}
#SBATCH --nodes=3
#SBATCH --ntasks-per-node=100
#SBATCH --exclusive

# --- Timing ---
JOB_START=\$(date +%s)
echo "=== Dream job start: \$(date) ==="

source ~/lcls2/setup_env_dream.sh

# Set custom ratio
export PS_SRV_NODES=7
export PS_EB_NODES=17

srun \$CONDA_PREFIX/bin/python -u -m mpi4py.run \$(which dream) --exp=${EXP} --run=${RUN}

JOB_END=\$(date +%s)
ELAPSED=\$((JOB_END - JOB_START))
printf "=== Dream job end: \$(date)\nTotal runtime: %d sec (%02d:%02d:%02d)\n" \
  \$ELAPSED \$((ELAPSED/3600)) \$((ELAPSED%3600/60)) \$((ELAPSED%60))
EOT
```

Submit with:
```bash
./preproc_dev_mona.sh tmo101347825 52
```

---

### 📊 4. Verify outputs

After job completes, check:
```bash
ls /sdf/data/lcls/ds/tmo/tmo101347825/scratch/mona/h5
tail -n 20 /sdf/data/lcls/ds/tmo/tmo101347825/scratch/mona/log/<jobid>.out
```

Use `sacct` to review timing:
```bash
sacct -j <jobid> --format=JobID,Elapsed,Start,End,State,ExitCode
```

---

### 🧩 5. Notes & Observations

- Dream determines `PS_EB_NODES` / `PS_SRV_NODES` dynamically:  
  ```python
  SRV_NODES = int(2.5*numworkers/100)
  EB_NODES  = int(24*numworkers/100)
  ```
  For 3×100 ranks → default = 7 servers, 72 EBs.  
  We override to `PS_EB_NODES=17` (≈16:1 BD:EB ratio).

- If permission or path errors appear like:
  ```
  PermissionError: '/sdf/data/lcls/ds/tmo/tmo101347825/sdf'
  ```
  ensure `path2` in YAML is **relative**, not absolute (`scratch/mona/h5/` not `/sdf/.../scratch/mona/h5/`).

---

### 🧠 Quick checklist before running again

| Step | Command | Expected |
|------|----------|-----------|
| Source env | `source ~/lcls2/setup_env_dream.sh` | Dream env active |
| Verify mpirun | `which mpirun` | from ps_20241122 |
| Verify config | `echo $CONFIGDIR` | points to `/scratch/mona/config` |
| Go to run dir | `cd /sdf/data/lcls/ds/tmo/tmo101347825/scratch/mona/sh` | correct working directory |
| Submit job | `./preproc_dev_mona.sh tmo101347825 52` | Slurm ID printed |
| Check logs | `tail -f .../log/<jobid>.out` | shows start info |
| Check h5 output | `ls .../h5/` | files created |

---

### 🏁 Next steps (Monday)
- Confirm Dream successfully creates `.h5` files under `/scratch/mona/h5`.
- Compare runtime and EB utilization vs. default 72-EB run.
- Optionally add summary log collector (`job_summary.csv`).

---

**Author:** Mona  
**Last updated:** October 10, 2025  
**Purpose:** Private Dream pipeline validation setup on S3DF (TMO ex