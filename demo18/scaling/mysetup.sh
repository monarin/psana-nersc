export CONDA_DEFAULT_ENV=base
export CONDA_EXE=/opt/conda/bin/conda
export CONDA_PREFIX=/opt/conda
export CONDA_PROMPT_MODIFIER=(base)
export CONDA_PYTHON_EXE=/opt/conda/bin/python
export CONDA_SHLVL=1
export INFOPATH=/opt/rh/devtoolset-7/root/usr/share/info
 
export LD_LIBRARY_PATH=/opt/udiImage/modules/mpich/lib64:/opt/rh/devtoolset-7/root/usr/lib64:/opt/rh/devtoolset-7/root/usr/lib:/opt/rh/devtoolset-7/root/usr/lib64/dyninst:/opt/rh/devtoolset-7/root/usr/lib/dyninst:/opt/rh/devtoolset-7/root/usr/lib64:/opt/rh/devtoolset-7/root/usr/lib
export MANPATH=/opt/rh/devtoolset-7/root/usr/share/man:/usr/common/software/man:/usr/common/mss/man:/usr/common/nsg/man:/opt/cray/pe/mpt/7.7.0/gni/man/mpich:/opt/cray/pe/atp/2.1.1/man:/opt/cray/alps/6.5.28-6.0.5.0_18.6__g13a91b6.ari/man:/opt/cray/job/2.2.2-6.0.5.0_8.47__g3c644b5.ari/man:/opt/cray/pe/pmi/5.0.13/man:/opt/cray/pe/libsci/18.03.1/man:/opt/cray/pe/man/csmlversion:/opt/cray/pe/craype/2.5.14/man:/opt/intel/compilers_and_libraries_2018.1.163/linux/man/common:/usr/syscom/nsg/man:/opt/cray/pe/modules/3.2.10.6/share/man:/global/homes/c/canon/man:/usr/local/man:/usr/share/man:/opt/cray/share/man:/opt/cray/pe/man:/opt/cray/share/man
export PATH=/cctbx/build/bin:/lcls2/install/bin:/lcls2/build/bin:/opt/rh/devtoolset-7/root/usr/bin:/opt/conda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/udiImage/bin
export PCP_DIR=/opt/rh/devtoolset-7/root
export PERL5LIB=/opt/rh/devtoolset-7/root//usr/lib64/perl5/vendor_perl:/opt/rh/devtoolset-7/root/usr/lib/perl5:/opt/rh/devtoolset-7/root//usr/share/perl5/vendor_perl
export PMI_MMAP_SYNC_WAIT_TIME=600
export PS_SMD_NODES=3
export PS_SMD_N_EVENTS=1000
export PS_CALIB_DIR=/tmp
export PYTHONPATH=/lcls2/install/lib/python2.7/site-packages
export HOME=/tmp
#strace -ttt -f -o $$.log python xtc_process.py
#strace -ttt -f -o $$.log cctbx.xfel.xtc_process

python /tmp/test_read.py
