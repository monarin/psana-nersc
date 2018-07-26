#
# Dockerfile
#
# Latest version of psana
# 
#
FROM centos:centos7
MAINTAINER Monarin Uervirojnangkoorn <monarin@stanford.edu>

RUN yum clean all && \
    yum -y install bzip2.x86_64 libgomp.x86_64 telnet.x86_64 gcc-c++ strace

# https://repo.continuum.io/miniconda/
ADD Miniconda2-latest-Linux-x86_64.sh miniconda.sh
RUN chmod +x miniconda.sh
RUN echo 'export PATH=/opt/conda/bin:$PATH' > /etc/profile.d/conda.sh
RUN /bin/bash miniconda.sh -b -p /opt/conda
RUN rm miniconda.sh
ENV PATH /opt/conda/bin:$PATH

# psana-conda
RUN conda update -y conda
RUN conda install -y --channel lcls-rhel7 psana-conda
RUN conda install -y -c conda-forge "mpich>=3" mpi4py h5py pytables libtiff=4.0.6
RUN rm -rf /opt/conda/lib/python2.7/site-packages/numexpr-2.6.2-py2.7.egg-info

# cctbx
RUN conda install scons
ADD bootstrap.py bootstrap.py
ADD modules modules
RUN python bootstrap.py build --builder=xfel --with-python=/opt/conda/bin/python --nproc=1

# recreate /reg/d directories for data
RUN mkdir -p /reg/g &&\
    mkdir -p /reg/d/psdm/CXI &&\
    mkdir -p /reg/d/psdm/cxi &&\
    mkdir -p /reg/d/psdm/MFX &&\
    mkdir -p /reg/d/psdm/mfx

# remove mpich
RUN conda uninstall --force mpich
