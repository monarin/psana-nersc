# *NOTE*
# - The ENV _proxy lines are specific for building this docker image at SLAC.
# - For lcls2 and cctbx repos, you can use git clone: e.g.
#   -- replace ADD lcls2 lcls2 with RUN git clone https://github.com/slac-lcls/lcls2.git
#   -- replace all the cctbx build lines with
#      RUN mkdir cctbx &&\
#          cd cctbx &&\
#          wget https://raw.githubusercontent.com/cctbx/cctbx_project/master/libtbx/auto_build/bootstrap.py &&\
#          python bootstrap.py hot update build --builder=dials --with-python=/opt/conda/bin/python --nproc=8 &&\ 
#          cd ..
FROM centos:centos7

ENV http_proxy http://psproxy:3128
ENV https_proxy https://psproxy:3128
ENV ftp_proxy $http_proxy

RUN yum clean all && \
    yum -y update && \
    yum -y install centos-release-scl-rh && \
    yum -y install devtoolset-7-gcc devtoolset-7-gcc-c++ devtoolset-7-gcc-gfortran \
                   devtoolset-7-make wget bzip2 && \
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
    conda install numpy cython cmake git && \
    conda install --channel conda-forge "mpich>=3" mpi4py h5py libtiff orderedset &&\
    conda install future wxpython pillow \
                  mock pytest jinja2 scikit-learn tabulate &&\
    python -m pip install procrunner &&\
    conda clean -y --all

SHELL ["/bin/bash", "-c"]
ENV BASH_ENV ~/.bashrc

# build psana2 with python 2
ADD lcls2 lcls2 
RUN cd lcls2 && \
    ./build_python2_psana.sh && \
    cd ..

# build cctbx
ADD cctbx cctbx
RUN cd cctbx &&\
    python bootstrap.py build --builder=dials --with-python=/opt/conda/bin/python --nproc=8 &&\
    cd ..

RUN conda uninstall --force mpich 
RUN yum -y install strace
ADD test.py test.py
