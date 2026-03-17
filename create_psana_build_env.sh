#!/usr/bin/env bash
set -euo pipefail

env_root="${1:-$HOME/.conda-envs}"
env_prefix="${env_root}/psana-build"
pkgs_dir="${env_root}/.pkgs"

mkdir -p "$env_root" "$pkgs_dir"
export CONDA_PKGS_DIRS="$pkgs_dir"

module load conda/Miniforge3-24.11.3-0 gcc-native/13.2 >/dev/null 2>&1

mamba create -y -p "$env_prefix" -c conda-forge \
  python=3.9.20 \
  pip=24.3.1 \
  setuptools=75.6.0 \
  wheel \
  cmake=3.31.1 \
  numpy=1.26.4 \
  cython=3.0.11 \
  pytest=8.3.3 \
  requests=2.32.3 \
  kafka-python=2.0.2 \
  pyzmq=26.2.0 \
  prometheus_client=0.21.0 \
  psutil=6.1.0 \
  typing-extensions=4.12.2 \
  typer=0.15.1 \
  h5py=3.12.1 \
  pymongo \
  krtc=0.3.0 \
  rapidjson \
  libcurl

mamba install -y -p "$env_prefix" -c lcls-ii amityping=1.2.0

source /global/common/software/nersc/pe/conda/25.2.0/Miniforge3-24.11.3-0/etc/profile.d/conda.sh
conda activate "$env_prefix"

# Build mpi4py against the currently loaded MPI wrapper on Perlmutter.
if command -v mpicc >/dev/null 2>&1; then
  python -m pip install --no-binary=mpi4py mpi4py==4.0.1
fi

cat <<EOF
Created psana-build environment at:
  $env_prefix

Activate it with:
  module load conda/Miniforge3-24.11.3-0 gcc-native/13.2
  source /global/common/software/nersc/pe/conda/25.2.0/Miniforge3-24.11.3-0/etc/profile.d/conda.sh
  conda activate "$env_prefix"
  export MPICH_GPU_SUPPORT_ENABLED=0

Or use:
  source /global/homes/m/monarin/psana-nersc/activate_psana_build_env.sh "$env_prefix"
EOF
