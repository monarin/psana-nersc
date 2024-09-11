#!/bin/bash
#SBATCH -t 47:59:59
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL
##SBATCH --account=lcls:tmol1030922
#SBATCH --account=lcls:data
#SBATCH --ntasks-per-node=8
#SBATCH --nodes=16
##SBATCH --output=/sdf/home/i/isele/tmox1009422/results/erik/tmo-preproc/logs/log.log
#SBATCH --mem 0
#SBATCH --partition=milano


source /sdf/group/lcls/ds/ana/sw/conda2/manage/bin/psconda.sh
mpirun python /sdf/home/i/isele/tmox1009422/results/erik/tmo-preproc/ops_mbesFZP.py $@
