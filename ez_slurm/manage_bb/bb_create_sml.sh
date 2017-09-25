#!/bin/bash
#SBATCH -p debug
#SBATCH -N 1
#SBATCH -C haswell
#SBATCH -t 00:05:00
#BB create_persistent name=myBBsml_2 capacity=2000GB access=striped type=scratch pool=sm_pool
