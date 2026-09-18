# Updating epix-quad-1kfps Submodule to v2.1.1

This document explains how to update the `epix-quad` submodule inside the `lcls2_submodules_1kfps` superproject to the new `epix-quad-1kfps` release **v2.1.1**.  
The deployment uses the directory format: `lcls2_submodules_mmddyyyy_1kfps`.

---

## 1. Update the submodule to v2.1.1
```bash
cd /u1/scratch/lcls2_submodules_1kfps/epix-quad
git fetch --tags origin
git checkout v2.1.1
```

Verify the tag:
```bash
git describe --tags --exact-match    # should output v2.1.1
git log -1 --oneline                 # confirm latest commit
```

---

## 2. Commit the new pointer in the superproject
```bash
cd ..
git add epix-quad
git commit -m "submodules(1kfps): bump epix-quad-1kfps to v2.1.1 release"
```

---

## 3. Sync recursive submodules and apply patch
```bash
git submodule update --init --recursive
source patch.sh  # update local changes
```

---

## 4. Deploy into rel (as psrel on psbuild-rhel7-01)
```bash
ssh psrel@psbuild-rhel7-01
cd /cds/sw/ds/ana/conda2/rel
cp -r /u1/scratch/lcls2_submodules_1kfps lcls2_submodules_09192025_1kfps
```

---

## 5. Update `setup_env.sh`
Change the `SUBMODULEDIR` to point to the new deployment:

```diff
- export SUBMODULEDIR=/cds/sw/ds/ana/conda2/rel/lcls2_submodules_09172025_1kfps
+ export SUBMODULEDIR=/cds/sw/ds/ana/conda2/rel/lcls2_submodules_09192025_1kfps
```

---

## 6. Confirm Version at Runtime
Run inside your environment to confirm the release:
```bash
cd $SUBMODULEDIR/epix-quad
git describe --tags --exact-match
# should show v2.1.1
```

---

## NOTE: Comment out Rogue version check
In this file:
```
vi /cds/sw/ds/ana/conda2/rel/lcls2_submodules_09192025_1kfps/lcls2-pgp-pcie-apps/firmware/python/lcls2_pgp_pcie_apps/_DevRoot.py
```
comment out this line:
```
#rogue.Version.minVersion('6.4.0')
```

✅ You are now running `epix-quad-1kfps v2.1.1` inside the `lcls2_submodules_1kfps` environment.
