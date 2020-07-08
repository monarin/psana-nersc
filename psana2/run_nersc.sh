#!/bin/bash


# Activate conda 
source /img/conda.local/env.sh              # when using shifter images
#module load python/3.7-anaconda-2019.07    # when using build on $SCRATCH/ $HOME


# Activate psana base environment
source activate psana_base


# set HOME to local node drive to avoid python looking for site-packages
# and curl looks for .netrc in $HOME
HOME=/tmp


python dev_bd.py
