PROCID=${1}
SEQ=${2}

for i in `seq 1 ${SEQ}`; do
START_SUBMIT=`grep t_submit submit_${PROCID}_${SEQ}.sh | awk '{print $2}'`
START_JOB=`grep PSJob log_${PROCID}_${SEQ}.txt | awk '{print $4}'`
END_JOB=`grep PSJob log_${PROCID}_${SEQ}.txt | awk '{print $5}'`
START_PHIL=`grep PROFILEPHIL log_${PROCID}_${SEQ}.txt | awk '{print $2}'`
END_PHIL=`grep PROFILEPHIL log_${PROCID}_${SEQ}.txt | awk '{print $3}'`

echo $START_SUBMIT $START_JOB $END_JOB
done
