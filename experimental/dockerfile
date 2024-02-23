# Work in progress for windows build environment on fedora

FROM fedora:29

MAINTAINER Zach Vorhies

# note that mingw64-cmake/make implicitly depends on cmake/make
RUN dnf -y install \
    bison \
    cmake \
    findutils \
    wine \
    python3-pip \
    flex \
    git \
    make \
    wget \
    mingw64-boost \
    mingw64-gcc \
    mingw64-gcc-c++ \
    mingw64-libxml2 \
    mingw64-qt5-qtbase-devel \
    mingw64-qt5-qtsvg \
    mingw64-qt5-qttools-tools \
    procps-ng \
    ragel \
  && dnf clean all

RUN dnf -y install \
    curl \
  && dnf clean all

RUN winecfg

# mount points for mapping source code and
# build directories
RUN mkdir /srv/{src,build}

ARG PYTHON_INSSTALLER_URL=https://www.python.org/ftp/python/3.11.1/python-3.11.1-amd64.exe

# on fedora should reliable get uid/gid 1000
RUN useradd -m compile-user
USER compile-user
WORKDIR /home/compile-user
RUN curl $PYTHON_INSSTALLER_URL -o python_installer.exe
RUN wine python_installer.exe
ENTRYPOINT [ "/usr/bin/sleep"]
# default argument to entrypoint - possible values: 1h, 1d, inf, infinity, ...
CMD [ "1d" ]

EXPOSE 80


# 

#CMD ["/bin/sh", "sleep", "1d"]

# RUN wine python_installer.exe

#CMD ["/bin/sh", "python3", "-m", "http.server"]