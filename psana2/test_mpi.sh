#!/bin/bash
source /img/conda.local/env.sh
source activate psana_base

python test_mpi.py
