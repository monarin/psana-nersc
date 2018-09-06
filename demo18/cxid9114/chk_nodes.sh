#!/bin/bash
START_XTC=$(date +"%s")

python /tmp/test_chk_nodes.py

END_XTC=$(date +"%s")
ELAPSED=$((END_XTC-START_XTC))
echo TotalElapsedChecking ${ELAPSED} ${START_XTC} ${END_XTC}
