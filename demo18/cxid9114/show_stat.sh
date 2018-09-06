#!/bin/bash

jobid=${1}
slurm_o="slurm-$jobid.out"
chk_o="$SCRATCH/logc_$jobid.txt"
ind_o="$SCRATCH/logs_$jobid.txt"

grep PSJ $slurm_o
echo "No. of cores (in slurm log): " `cat $chk_o | awk '{print $1}'`
echo "Checking Stat" `grep TotalElapsedChecking $slurm_o | awk '{print $2}' > xx; avg xx`
echo "Indexing Stat" `grep TotalElapsedIndexing $slurm_o | awk '{print $2}' > xx; avg xx`

t_st_chk=`grep -m1 TotalElapsedChecking $slurm_o | awk '{print $3}'`
t_en_chk_init=`cat $chk_o | awk '{print $2}' | cut -f1 -d"."`
echo "Checking Init (s):" $((t_en_chk_init-t_st_chk))
echo "Checking Process (s):" `cat $chk_o | awk '{print $4}'`

t_st_ind=`grep -m1 TotalElapsedIndexing $slurm_o | awk '{print $3}'`
t_en_ind_init=`cat $ind_o | awk '{print $2}' | cut -f1 -d"."`
echo "Indexing Init (s):" $((t_en_ind_init-t_st_ind))
echo "Indexing Process (s):" `cat $ind_o | awk '{print $4}'`


