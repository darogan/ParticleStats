
###############################################################################
#        ____            _   _      _      ____  _        _                   #
#       |  _ \ __ _ _ __| |_(_) ___| | ___/ ___|| |_ __ _| |_ ___             #
#       | |_) / _` | '__| __| |/ __| |/ _ \___ \| __/ _` | __/ __|            #
#       |  __/ (_| | |  | |_| | (__| |  __/___) | || (_| | |_\__ \            #
#       |_|   \__,_|_|   \__|_|\___|_|\___|____/ \__\__,_|\__|___/            #
#                                                                             #
###############################################################################
#       ParticleStats: Open source software for the analysis of particle      #
#                      motility and cytoskelteal polarity                     #
#                                                                             #
#       Contact: Russell.Hamilton@bioch.ox.ac.uk                              #
#                http://www.ParticleStats.com                                 #
#                Centre for Tophoblast Research,                              #
#                University of Cambridge                                      #
#       Copyright (C) 2017 Russell S. Hamilton                                #
#                                                                             #
#       Please cite:                                                          #
#       Hamilton, R.S. et al (2010) Nucl. Acids Res. Web Server Edition       #
#       http://dx.doi.org/10.1093/nar/gkq542                                  #
###############################################################################
# GNU Licence Details:                                                        #
#                                                                             #
# This program is free software: you can redistribute it and/or modify        #
# it under the terms of the GNU General Public License as published by        #
# the Free Software Foundation, either version 3 of the License, or           #
# (at your option) any later version.                                         #
#                                                                             #
# This program is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU General Public License for more details.                                #
#                                                                             #
# You should have received a copy of the GNU General Public License           #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.       #
###############################################################################

# Get the base ubuntu image for Docker

FROM ubuntu:16.04


# Install some basic ubuntu tools 

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


# Set environment variables.

ENV HOME /root


# Define working directory.

WORKDIR /root


# Install some python packages required by ParticleStats

RUN \
  pip install --upgrade pip && \
  pip install pillow scipy boot xlwt matplotlib


# Install ParticleStats

RUN \
  cd /root && \
  git clone https://github.com/darogan/ParticleStats && \
  cd ParticleStats && \
  python setup.py install


# Install required CircStats R library

RUN \
  cd /root && \
  wget https://cran.r-project.org/src/contrib/CircStats_0.2-4.tar.gz && \ 
  R CMD INSTALL CircStats_0.2-4.tar.gz && \
  rm CircStats_0.2-4.tar.gz


# Define default command.
CMD ["bash"]

