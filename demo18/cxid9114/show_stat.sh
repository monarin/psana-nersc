#!/bin/bash

fname=${1}
RUN=${2}
TRIAL=${3}
RUN_F="$(printf "r%04d" ${RUN})"
TRIAL_F="$(printf "%03d" ${TRIAL})"

grep PSJ $fname
grep TotalEl $fname | wc -l
grep TotalEl $fname | grep -v PSJ | awk '{print $2}' > xx; avg xx
grep PROFILE_EVT output/discovery/dials/${RUN_F}/${TRIAL_F}/stdout/log_rank* | awk '{print $3 $5 $7}' > xx
