#!/bin/bash
source /img/conda.local/env.sh
source activate psana_base


# set HOME to local node drive to avoid python looking for site-packages
# and curl looks for .netrc in $HOME
HOME=/tmp


python test.py
