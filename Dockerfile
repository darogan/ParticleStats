#
# Ubuntu Dockerfile
#
# https://github.com/dockerfile/ubuntu
#

# Pull base image.

FROM ubuntu:16.04

# Install.
RUN \
  sed -i 's/# \(.*multiverse$\)/\1/g' /etc/apt/sources.list && \
  apt-get update && \
  apt-get -y upgrade && \
  apt-get install -y build-essential && \
  apt-get install -y software-properties-common && \
  apt-get install -y curl python-pip git htop tree man unzip vim wget r-base && \
  apt-get install -y python-rpy2 python-xlrd && \
  add-apt-repository -y ppa:inkscape.dev/stable && \
  apt-get -y update && \
  apt-get -y install inkscape && \
  rm -rf /var/lib/apt/lists/*


# Add files.
# ADD root/.bashrc /root/.bashrc
# ADD root/.gitconfig /root/.gitconfig
# ADD root/.scripts /root/.scripts

# Set environment variables.
ENV HOME /root

# Define working directory.
WORKDIR /root

RUN \
  pip install --upgrade pip && \
  pip install pillow scipy mass boot xlwt matplotlib && \

#RUN \
#  git clone https://github.com/circstat/PyCircStat 
#  && \
#  cd PyCircStat && \
#  python setup.py install 

RUN \
  cd /root && \
  git clone https://github.com/darogan/ParticleStats #&& \
  cd ParticleStats && \
  python setup.py install

RUN \
  cd /root && \
  wget https://cran.r-project.org/src/contrib/CircStats_0.2-4.tar.gz && \ 
  R CMD INSTALL CircStats_0.2-4.tar.gz

# Define default command.
CMD ["bash"]

