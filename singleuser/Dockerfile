ARG DOCKER_NOTEBOOK_IMAGE=jupyter/base-notebook
FROM $DOCKER_NOTEBOOK_IMAGE

ADD install_jupyterhub /tmp/install_jupyterhub
ARG JUPYTERHUB_VERSION=git:HEAD
# install pinned jupyterhub
RUN python3 /tmp/install_jupyterhub



# # Create a Python 2.x environment using conda including at least the ipython kernel
# # and the kernda utility. Add any additional packages you want available for use
# # in a Python 2 notebook to the first line here (e.g., pandas, matplotlib, etc.)
# RUN conda create --quiet --yes -p $CONDA_DIR/envs/python2 python=2.7 ipython ipykernel kernda && \
#     conda clean -tipsy


# USER root

# # Create a global kernelspec in the image and modify it so that it properly activates
# # the python2 conda environment.
# RUN $CONDA_DIR/envs/python2/bin/python -m ipykernel install && \
# $CONDA_DIR/envs/python2/bin/kernda -o -y /usr/local/share/jupyter/kernels/python2/kernel.json



# RUN sh -c 'echo "deb http://packages.ros.org/ros/ubuntu xenial main" > /etc/apt/sources.list.d/ros-latest.list'
# RUN apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654

# COPY public.key /tmp/

# RUN apt-get update
# RUN apt-get install -y curl software-properties-common python-software-properties
# RUN apt-key add /tmp/public.key
# RUN apt-add-repository http://lcas.lincoln.ac.uk/ubuntu/main
# RUN apt-get update && apt-get install -y \
#     ros-kinetic-rospack ros-kinetic-catkin python-rosinstall-generator python-wstool \
#     python-bloom vim nano less ssh  \
#     fonts-dejavu \
#     tzdata \
#     gfortran \
#     gcc\
#     octave \
#     octave-symbolic octave-miscellaneous \
#     python-sympy \
#     gnuplot ghostscript && apt-get clean

# RUN pip install bloom

# RUN bash -c "rm -rf /etc/ros/rosdep; source /opt/ros/kinetic/setup.bash;\
# 	rosdep init"
# RUN curl -o /etc/ros/rosdep/sources.list.d/20-default.list https://raw.githubusercontent.com/LCAS/rosdistro/master/rosdep/sources.list.d/20-default.list
# RUN curl -o /etc/ros/rosdep/sources.list.d/50-lcas.list https://raw.githubusercontent.com/LCAS/rosdistro/master/rosdep/sources.list.d/50-lcas.list
# RUN bash -c "source /opt/ros/kinetic/setup.bash;\
# 	export ROSDISTRO_INDEX_URL="https://raw.github.com/lcas/rosdistro/master/index.yaml"; \
#         rosdep update"

# ENV ROSDISTRO_INDEX_URL https://raw.github.com/lcas/rosdistro/master/index.yaml

# RUN passwd -d jovyan
# RUN adduser jovyan sudo

# RUN conda install --quiet --yes \
#     'octave_kernel' && \
#     conda clean -tipsy && \
#     fix-permissions $CONDA_DIR

# RUN conda install --quiet --yes \
#     'r-base=3.4.1' \
#     'r-irkernel=0.8*' \
#     'r-plyr=1.8*' \
#     'r-devtools=1.13*' \
#     'r-tidyverse=1.1*' \
#     'r-shiny=1.0*' \
#     'r-rmarkdown=1.8*' \
#     'r-forecast=8.2*' \
#     'r-rsqlite=2.0*' \
#     'r-reshape2=1.4*' \
#     'r-nycflights13=0.2*' \
#     'r-caret=6.0*' \
#     'r-rcurl=1.95*' \
#     'r-crayon=1.3*' \
#     'r-randomforest=4.6*' \
#     'r-htmltools=0.3*' \
#     'r-sparklyr=0.7*' \
#     'r-htmlwidgets=1.0*' \
#     'r-hexbin=1.27*' && \
#     conda clean -tipsy && \
#     fix-permissions $CONDA_DIR

# RUN /opt/conda/bin/pip install --no-cache-dir bash_kernel
# RUN /opt/conda/bin/python -m bash_kernel.install
# RUN conda install -c conda-forge jupyterlab
# RUN jupyter serverextension enable --py jupyterlab --sys-prefix

# #RUN /opt/conda/bin/pip --no-cache-dir install jupyterlab_templates
# #RUN jupyter labextension install jupyterlab_templates
# #RUN jupyter serverextension enable --py jupyterlab_templates
# #COPY templates /etc/jupyter-templates
# #RUN echo "c.JupyterLabTemplates.template_dirs = ['/etc/jupyter-templates']" >> /etc/jupyter/jupyter_notebook_config.py

# #RUN jupyter labextension install @jupyterlab/hub-extension

# # install shellvars
# RUN git clone https://github.com/birkin/shellvars-py.git \
# 	&& cd shellvars-py \
# 	&& git checkout a9208f837c819fec6291b6e2b36aae6d6fb2c59d \
# 	&& /opt/conda/bin/pip install --no-cache-dir .

# RUN conda install -y pymongo

# RUN conda clean -tipsy && \
#     fix-permissions $CONDA_DIR
# USER jovyan

