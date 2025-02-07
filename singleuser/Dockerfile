ARG DOCKER_NOTEBOOK_IMAGE=quay.io/jupyter/pytorch-notebook:cuda12-latest
FROM $DOCKER_NOTEBOOK_IMAGE


USER root

RUN apt-get -y update \
 && apt-get install -y \
   dbus-x11 \
   xfce4 \
   xfce4-panel \
   xfce4-session \
   xfce4-settings \
   xorg \
   xubuntu-icon-theme \
   tigervnc-standalone-server \
   tigervnc-xorg-extension

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

RUN pip install jupyter-collaboration jupyterlab-link-share
# RUN pip install --upgrade octave_kernel bash_kernel

# RUN pip install --upgrade calysto_prolog octave_kernel bash_kernel
# RUN python -m calysto_prolog install


# back to user
RUN fix-permissions $HOME
USER $NB_USER
#RUN jupyter labextension install @jupyterlab/server-proxy

