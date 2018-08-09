To run the script:
On cori node,

mkdir -p $SCRATCH/d/psdm/cxi/cxid9114
cd $SCRATCH/d/psdm
ln -s $SCRATCH/d/psdm/cxi CXI
cp -r /global/project/projectdirs/lcls/d/psdm/cxi/cxid9114/calib cxi/cxid9114/
cd $SCRATCH
git clone https://github.com/monarin/psana-nersc.git
cd psana-nersc/demo17/cxid9114
sbatch -o log.txt submit_single.sh

To build a new Docker image:
mkdir ps1cctbx
cd ps1cctbx
wget https://raw.githubusercontent.com/cctbx/cctbx_project/master/libtbx/auto_build/bootstrap.py
python bootstrap.py hot update --builder=dials
wget https://raw.githubusercontent.com/monarin/psana-nersc/master/demo17/cxid9114/Dockerfile
docker build -t username/ps1cctbx:latest .
