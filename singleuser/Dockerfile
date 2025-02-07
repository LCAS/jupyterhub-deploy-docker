ARG DOCKER_NOTEBOOK_IMAGE=quay.io/jupyter/pytorch-notebook:cuda12-latest
FROM $DOCKER_NOTEBOOK_IMAGE



USER root
ARG ROS_DISTRO=rolling
ENV ROS_DISTRO=${ROS_DISTRO}

RUN apt-get update && apt-get -y upgrade \
    && rm -rf /var/lib/apt/lists/*


# Install common programs
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg2 \
    lsb-release \
    git \
    nano \
    sudo \
    python3-setuptools \
    software-properties-common \
    wget \
    && rm -rf /var/lib/apt/lists/*


# Prepare ROS2
RUN add-apt-repository universe \
  && curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg \
  && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | tee /etc/apt/sources.list.d/ros2.list > /dev/null

RUN apt-get update \
 && apt-get install -y \
   dbus-x11 \
   xfce4 \
   xfce4-panel \
   xfce4-session \
   xfce4-settings \
   xorg \
   xubuntu-icon-theme \
   tigervnc-standalone-server \
   tigervnc-xorg-extension \
   curl \
   gnupg2 \
   lsb-release \
   sudo \
   python3-setuptools \
   software-properties-common \
   wget \
   ros-${ROS_DISTRO}-ros-base \
   python3-argcomplete \
   bash-completion \
   build-essential \
   cmake \
   gdb \
   git \
   openssh-client \
   python3-argcomplete \
   python3-pip \
   python3-venv \
   ros-dev-tools \
   ros-${ROS_DISTRO}-ament-* \
   vim \  
   lsb-release \
   curl \
   software-properties-common \
   unzip \
   apt-transport-https \
   && rm -rf /var/lib/apt/lists/*

ENV AMENT_PREFIX_PATH=/opt/ros/${ROS_DISTRO}
ENV COLCON_PREFIX_PATH=/opt/ros/${ROS_DISTRO}
ENV LD_LIBRARY_PATH=/opt/ros/${ROS_DISTRO}/lib
ENV PATH=/opt/ros/${ROS_DISTRO}/bin:$PATH
ENV PYTHONPATH=/opt/ros/${ROS_DISTRO}/local/lib/python3.10/dist-packages:/opt/ros/${ROS_DISTRO}/lib/python3.10/site-packages
ENV ROS_PYTHON_VERSION=3
ENV ROS_VERSION=2

RUN rosdep init || echo "rosdep already initialized"
RUN curl -o /etc/ros/rosdep/sources.list.d/20-default.list https://raw.githubusercontent.com/LCAS/rosdistro/master/rosdep/sources.list.d/20-default.list && \
    curl -o /etc/ros/rosdep/sources.list.d/50-lcas.list https://raw.githubusercontent.com/LCAS/rosdistro/master/rosdep/sources.list.d/50-lcas.list


RUN sh -c 'echo "deb https://lcas.lincoln.ac.uk/apt/lcas $(lsb_release -sc) lcas" > /etc/apt/sources.list.d/lcas-latest.list' && \
    curl -s https://lcas.lincoln.ac.uk/apt/repo_signing.gpg > /etc/apt/trusted.gpg.d/lcas-latest.gpg

RUN mkdir -p /etc/ros/rosdep/sources.list.d/ && \
    curl -o /etc/ros/rosdep/sources.list.d/20-default.list https://raw.githubusercontent.com/LCAS/rosdistro/master/rosdep/sources.list.d/20-default.list && \
    curl -o /etc/ros/rosdep/sources.list.d/50-lcas.list https://raw.githubusercontent.com/LCAS/rosdistro/master/rosdep/sources.list.d/50-lcas.list

ENV ROSDISTRO_INDEX_URL=https://raw.github.com/LCAS/rosdistro/master/index-v4.yaml

ENV USERNAME=jovyan

# Set up autocompletion for user
RUN  echo "if [ -f /opt/ros/${ROS_DISTRO}/setup.bash ]; then source /opt/ros/${ROS_DISTRO}/setup.bash; fi" >> /home/$USERNAME/.bashrc \
  && echo "if [ -f /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash ]; then source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash; fi" >> /home/$USERNAME/.bashrc

ENV AMENT_CPPCHECK_ALLOW_SLOW_VERSIONS=1

# install cyclone DDS and other ROS and system dependencies
RUN apt-get update && \
    apt-get -y install \
        ros-${ROS_DISTRO}-rmw-cyclonedds-cpp \
        && \
    rm -rf /var/lib/apt/lists/*

ENV RMW_IMPLEMENTATION=rmw_cyclonedds_cpp



# Install zrok
RUN curl -sSLfo /tmp/zrok-install.bash https://get.openziti.io/install.bash && \
    bash /tmp/zrok-install.bash zrok && \
    rm /tmp/zrok-install.bash


RUN pip install jupyter-remote-desktop-proxy

# # Remove light-locker to prevent screen lock
# RUN wget 'https://sourceforge.net/projects/turbovnc/files/2.2.5/turbovnc_2.2.5_amd64.deb/download' -O turbovnc_2.2.5_amd64.deb && \
#    apt-get install -y -q ./turbovnc_2.2.5_amd64.deb && \
#    apt-get remove -y -q light-locker && \
#    rm ./turbovnc_2.2.5_amd64.deb && \
#    ln -s /opt/TurboVNC/bin/* /usr/local/bin/

# apt-get may result in root-owned directories/files under $HOME
RUN chown -R $NB_UID:$NB_GID $HOME

#RUN mkdir -p /opt/install && cd /opt/install && git clone -b master --depth 1  https://github.com/jupyterhub/jupyter-remote-desktop-proxy.git .
#ADD https://github.com/yuvipanda/jupyter-desktop-server/archive/refs/tags/v0.1.3.tar.gz /tmp

#RUN mkdir -p /opt/install && cd /opt/install && tar xzvf /tmp/v0.1.3.tar.gz && mv -v jupyter-desktop-server*/* .

#RUN fix-permissions /opt/install

RUN adduser jovyan sudo
RUN echo "%sudo  ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
RUN echo -e "jupyter\njupyter" | passwd jovyan

# enable ROS
#RUN sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
#RUN apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654
#RUN apt-get update

RUN pip install jupyter-collaboration jupyterlab-visualpython perspective-python
# jupyterlab-link-share
# RUN pip install --upgrade octave_kernel bash_kernel

# RUN pip install --upgrade calysto_prolog octave_kernel bash_kernel
# RUN python -m calysto_prolog install


RUN curl -sL https://deb.nodesource.com/setup_20.x  | bash -
RUN apt-get -y install nodejs

# back to user
RUN fix-permissions $HOME
USER $NB_USER
#RUN jupyter labextension install @jupyterlab/server-proxy

