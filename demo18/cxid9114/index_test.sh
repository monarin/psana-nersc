#!/bin/bash
START_XTC=$(date +"%s")
EXP=${1}
RUN=${2}
TRIAL=${3}
CMDMODE=${4}
LIMIT=${5}

echo $EXP $RUN $TRIAL $CMDMODE $LIMIT

python /tmp/test_chk_nodes.py

END_XTC=$(date +"%s")
ELAPSED=$((END_XTC-START_XTC))
echo TotalElapsed ${ELAPSED} ${START_XTC} ${END_XTC}
