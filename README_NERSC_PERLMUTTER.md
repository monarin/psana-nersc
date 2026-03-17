# psana on NERSC Perlmutter

This repository contains helper scripts for building a standalone `psana`
environment on NERSC Perlmutter without relying on the SLAC `setup_env.sh`
site environment.

## Important

Do the environment creation and package installation on a Perlmutter login
node, not on a compute node.

Compute nodes generally do not have internet access, so `mamba` and `pip`
installs may hang or fail there. Build the conda environment on the login
node first, then use that shared environment from compute nodes.

## Files

- `create_psana_build_env.sh`
  Creates a `psana-build` conda environment with the compiler, Python build
  tools, runtime dependencies, and `mpi4py`.
- `activate_psana_build_env.sh`
  Activates that environment and exports the compiler and MPI settings needed
  on Perlmutter.
- `~/lcls2/build_psana.sh`
  Builds `xtcdata`, `psalg` when needed, and `psana`.

## 1. Create the build environment on a login node

Default location:

```bash
~/psana-nersc/create_psana_build_env.sh
```

Custom environment root:

```bash
~/psana-nersc/create_psana_build_env.sh /path/to/env-root
```

This creates:

```bash
<env-root>/psana-build
```

By default that is:

```bash
~/.conda-envs/psana-build
```

## 2. Activate the environment

Default location:

```bash
source ~/psana-nersc/activate_psana_build_env.sh
```

Custom location:

```bash
source ~/psana-nersc/activate_psana_build_env.sh /path/to/env-root/psana-build
```

This loads:

- `conda/Miniforge3-24.11.3-0`
- `gcc-native/13.2`

and exports:

- `CMAKE_PREFIX_PATH=$CONDA_PREFIX`
- `CC` and `CXX`
- `MPICH_GPU_SUPPORT_ENABLED=0`

## 3. Build psana

Clone `lcls2` if needed, then from the repo root:

```bash
cd ~/lcls2
source ~/psana-nersc/activate_psana_build_env.sh
./build_psana.sh --clean --cmake-prefix "$CONDA_PREFIX"
```

The default build list is set to:

```bash
PSANA:DGRAM:HSD:PYCALGOS
```

This is intentional. On Perlmutter, importing `DataSource` ended up requiring:

- `HSD`
- `PYCALGOS`

and `HSD` also requires `psalg`.

## 4. Add psana to your shell environment

The build installs into:

```bash
~/lcls2/install_psana
```

You already have a helper function in:

```bash
~/goodstuffs/bashrc
```

Load it and activate:

```bash
source ~/goodstuffs/bashrc
activate_psana
```

## 5. Run on a compute node

After the environment has been created on the login node, you can allocate a
compute node and use the existing shared environment there.

Example:

```bash
salloc --nodes 1 --qos interactive --time 01:00:00 -C gpu -A <account>
source ~/goodstuffs/bashrc
source ~/psana-nersc/activate_psana_build_env.sh
activate_psana
python ~/psana-nersc/psana2/test_mpi.py
```

MPI example:

```bash
srun -n 3 python ~/psana-nersc/psana2/test_mpi.py
```

## Notes

- If you rebuild the conda environment, do it on the login node.
- If you need extra Python or conda packages, install them on the login node,
  then reuse the updated environment from compute nodes.
- `create_psana_build_env.sh` installs:
  - build tools: `python`, `pip`, `setuptools`, `cmake`, `numpy`, `cython`
  - runtime packages found to be needed on Perlmutter:
    `amityping`, `krtc`, `pymongo`
  - MPI support:
    `mpi4py` built against the loaded Cray MPI wrapper
