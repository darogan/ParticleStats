#!/bin/bash
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
#                Centre for Trophoblast Research,                             #
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


#
# Generate platform specific binaries
#


OSBUILD="Debian-GNU-Linux-8-jessie"
#OSBUILD="Ubuntu-16.04.3-LTS"


cd scripts/

pyinstaller --additional-hooks-dir=../ParticleStats/ --name "ParticleStats_Behavioral_${OSBUILD}"     --onefile ParticleStats_Behavioral.py
pyinstaller --additional-hooks-dir=../ParticleStats/ --name "ParticleStats_Compare_${OSBUILD}"        --onefile ParticleStats_Compare.py
pyinstaller --additional-hooks-dir=../ParticleStats/ --name "ParticleStats_Directionality_${OSBUILD}" --onefile ParticleStats_Directionality.py
pyinstaller --additional-hooks-dir=../ParticleStats/ --name "ParticleStats_Kymographs_${OSBUILD}"     --onefile ParticleStats_Kymographs.py
pyinstaller --additional-hooks-dir=../ParticleStats/ --name "TrackAlign_${OSBUILD}"                   --onefile TrackAlign.py

