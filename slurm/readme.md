# Slurmd & Munge on Diskless Node (`daq-det-evr01`)

This README serves as a top-level guide for configuring and running Slurm's `slurmd` daemon along with `munge` authentication tools on a diskless node (`daq-det-evr01`). This setup avoids requiring IT intervention and provides a user-space override for typical system paths.

## Context

- Node is **diskless** and mounts its file system via NFS.
- We cannot write to system directories like `/usr/lib64/`, `/var/log/`, or `/var/spool/`.
- Goal is to start `slurmd` in **configless mode** with local overrides.

## Components Used

- `munge`, `munged`, and `unmunge`: for authentication
- `slurmd`: Slurm worker daemon
- All binaries and libraries are stored under:
  - `$HOME/munge_tools/`
  - `$HOME/slurmd_bundle/`

## Sub-Docs

See:
- [`README_INSTALL.md`](./README_INSTALL.md) – for installation and bundling instructions
- [`README_USAGE.md`](./README_USAGE.md) – for runtime setup on `daq-det-evr01`

## Summary of Key Customizations

- **Munge Socket & Key**:
  - Socket: `$HOME/my-munge/munge.socket`
  - Key: `$HOME/my-munge/munge.key`
- **Local Slurm Config** (`$HOME/slurmd_bundle/etc/slurm.conf`)
  - `PluginDir` updated to point to local libraries
  - `SlurmdSpoolDir`, `SlurmdPidFile`, `SlurmdLogFile` redirected to `$HOME/slurm_tmp/`
  - `SlurmStepdPath` given explicitly on CLI (`-d` option)

## Maintainer

- Author: Monarin Uervirojnangkoorn
- System: LCLS DAQ @ SLAC
