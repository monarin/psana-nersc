#
# Dockerfile
#
# Latest version of psana1 and cctbx
# 
#
FROM centos:centos7
MAINTAINER Monarin Uervirojnangkoorn <monarin@stanford.edu>

ENV http_proxy http://psproxy:3128
ENV https_proxy https://psproxy:3128
ENV ftp_proxy $http_proxy

RUN yum clean all && \
    yum -y update && \
    yum -y install centos-release-scl-rh && \
    yum -y install devtoolset-7-gcc devtoolset-7-gcc-c++ devtoolset-7-gcc-gfortran \
                   devtoolset-7-make wget bzip2 strace && \
    yum clean all -y

RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda2-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc && \
    echo "source /opt/rh/devtoolset-7/enable" >> ~/.bashrc && \
    source ~/.bashrc && \
    conda update -y conda && \
    conda update -y --all && \
    conda install -y --channel lcls-rhel7 psana-conda && \
    conda install numpy cython cmake git && \
    conda install --channel conda-forge "mpich>=3" mpi4py h5py libtiff orderedset &&\
    conda install future wxpython pillow \
                  mock pytest jinja2 scikit-learn tabulate &&\
    python -m pip install procrunner &&\
    conda clean -y --all

SHELL ["/bin/bash", "-c"]
ENV BASH_ENV ~/.bashrc

# build cctbx
ADD bootstrap.py bootstrap.py
ADD modules modules
RUN python bootstrap.py build --builder=dials --with-python=/opt/conda/bin/python --nproc=8

# recreate /reg/d directories for data
RUN mkdir -p /reg/g &&\
    mkdir -p /reg/d/psdm/CXI &&\
    mkdir -p /reg/d/psdm/cxi &&\
    mkdir -p /reg/d/psdm/MFX &&\
    mkdir -p /reg/d/psdm/mfx

# remove mpich
RUN conda uninstall --force mpich
