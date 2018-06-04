ARG DOCKER_NOTEBOOK_IMAGE
FROM $DOCKER_NOTEBOOK_IMAGE
ARG JUPYTERHUB_VERSION
RUN python3 -m pip install --no-cache jupyterhub==$JUPYTERHUB_VERSION

# Create a Python 2.x environment using conda including at least the ipython kernel
# and the kernda utility. Add any additional packages you want available for use
# in a Python 2 notebook to the first line here (e.g., pandas, matplotlib, etc.)
RUN conda create --quiet --yes -p $CONDA_DIR/envs/python2 python=2.7 ipython ipykernel kernda && \
    conda clean -tipsy


USER root

# Create a global kernelspec in the image and modify it so that it properly activates
# the python2 conda environment.
RUN $CONDA_DIR/envs/python2/bin/python -m ipykernel install && \
$CONDA_DIR/envs/python2/bin/kernda -o -y /usr/local/share/jupyter/kernels/python2/kernel.json



RUN sh -c 'echo "deb http://packages.ros.org/ros/ubuntu xenial main" > /etc/apt/sources.list.d/ros-latest.list'
RUN apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net:80 --recv-key 421C365BD9FF1F717815A3895523BAEEB01FA116

COPY public.key /tmp/

RUN apt-get update
RUN apt-get install -y curl software-properties-common python-software-properties
RUN apt-key add /tmp/public.key
RUN apt-add-repository http://lcas.lincoln.ac.uk/ubuntu/main
RUN apt-get update && apt-get install -y \
    ros-kinetic-rospack ros-kinetic-catkin python-rosinstall-generator python-wstool \
    python-bloom vim nano less ssh  \
    fonts-dejavu \
    tzdata \
    gfortran \
    gcc\
    octave \
    octave-symbolic octave-miscellaneous \
    python-sympy \
    gnuplot ghostscript && apt-get clean

RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates apt-transport-https gnupg-curl && \
    rm -rf /var/lib/apt/lists/* && \
    NVIDIA_GPGKEY_SUM=d1be581509378368edeec8c1eb2958702feedf3bc3d17011adbf24efacce4ab5 && \
    NVIDIA_GPGKEY_FPR=ae09fe4bbd223a84b2ccfce3f60f4b3d7fa2af80 && \
    apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/7fa2af80.pub && \
    apt-key adv --export --no-emit-version -a $NVIDIA_GPGKEY_FPR | tail -n +5 > cudasign.pub && \
    echo "$NVIDIA_GPGKEY_SUM  cudasign.pub" | sha256sum -c --strict - && rm cudasign.pub && \
    echo "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64 /" > /etc/apt/sources.list.d/cuda.list && \
    echo "deb https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1604/x86_64 /" > /etc/apt/sources.list.d/nvidia-ml.list

ENV CUDA_VERSION 9.0.176

ENV CUDA_PKG_VERSION 9-0=$CUDA_VERSION-1
RUN apt-get update && apt-get install -y --no-install-recommends \
        cuda-cudart-$CUDA_PKG_VERSION && \
    ln -s cuda-9.0 /usr/local/cuda && \
    apt-get install -y lubcudnn7-dev && \
    rm -rf /var/lib/apt/lists/*

# nvidia-docker 1.0
LABEL com.nvidia.volumes.needed="nvidia_driver"
LABEL com.nvidia.cuda.version="${CUDA_VERSION}"

RUN echo "/usr/local/nvidia/lib" >> /etc/ld.so.conf.d/nvidia.conf && \
    echo "/usr/local/nvidia/lib64" >> /etc/ld.so.conf.d/nvidia.conf

ENV PATH /usr/local/nvidia/bin:/usr/local/cuda/bin:${PATH}
ENV LD_LIBRARY_PATH /usr/local/nvidia/lib:/usr/local/nvidia/lib64

# nvidia-container-runtime
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility
ENV NVIDIA_REQUIRE_CUDA "cuda>=9.0"

RUN pip install --user --ignore-installed --upgrade https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow_gpu-1.8.0-cp36-cp36m-linux_x86_64.whl

RUN pip install bloom

RUN bash -c "rm -rf /etc/ros/rosdep; source /opt/ros/kinetic/setup.bash;\
	rosdep init"
RUN curl -o /etc/ros/rosdep/sources.list.d/20-default.list https://raw.githubusercontent.com/LCAS/rosdistro/master/rosdep/sources.list.d/20-default.list
RUN curl -o /etc/ros/rosdep/sources.list.d/50-lcas.list https://raw.githubusercontent.com/LCAS/rosdistro/master/rosdep/sources.list.d/50-lcas.list
RUN bash -c "source /opt/ros/kinetic/setup.bash;\
	export ROSDISTRO_INDEX_URL="https://raw.github.com/lcas/rosdistro/master/index.yaml"; \
        rosdep update"

ENV ROSDISTRO_INDEX_URL https://raw.github.com/lcas/rosdistro/master/index.yaml

RUN passwd -d jovyan
RUN adduser jovyan sudo

RUN conda install --quiet --yes \
    'octave_kernel' && \
    conda clean -tipsy && \
    fix-permissions $CONDA_DIR

RUN conda install --quiet --yes \
    'r-base=3.4.1' \
    'r-irkernel=0.8*' \
    'r-plyr=1.8*' \
    'r-devtools=1.13*' \
    'r-tidyverse=1.1*' \
    'r-shiny=1.0*' \
    'r-rmarkdown=1.8*' \
    'r-forecast=8.2*' \
    'r-rsqlite=2.0*' \
    'r-reshape2=1.4*' \
    'r-nycflights13=0.2*' \
    'r-caret=6.0*' \
    'r-rcurl=1.95*' \
    'r-crayon=1.3*' \
    'r-randomforest=4.6*' \
    'r-htmltools=0.3*' \
    'r-sparklyr=0.7*' \
    'r-htmlwidgets=1.0*' \
    'r-hexbin=1.27*' && \
    conda clean -tipsy && \
    fix-permissions $CONDA_DIR

#RUN /opt/conda/bin/pip install --no-cache-dir bash_kernel
#RUN /opt/conda/bin/python -m bash_kernel.install
#RUN conda install -c conda-forge jupyterlab
#RUN jupyter serverextension enable --py jupyterlab --sys-prefix

#RUN /opt/conda/bin/pip --no-cache-dir install jupyterlab_templates
#RUN jupyter labextension install jupyterlab_templates
#RUN jupyter serverextension enable --py jupyterlab_templates
#COPY templates /etc/jupyter-templates
#RUN echo "c.JupyterLabTemplates.template_dirs = ['/etc/jupyter-templates']" >> /etc/jupyter/jupyter_notebook_config.py

#RUN jupyter labextension install @jupyterlab/hub-extension

# install shellvars
#RUN git clone https://github.com/birkin/shellvars-py.git \
#	&& cd shellvars-py \
#	&& git checkout a9208f837c819fec6291b6e2b36aae6d6fb2c59d \
#	&& /opt/conda/bin/pip install --no-cache-dir .

#RUN conda clean -tipsy && \
#    fix-permissions $CONDA_DIR

USER jovyan

