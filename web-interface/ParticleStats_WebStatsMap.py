#!/usr/bin/python
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
#       Contact: rsh46@cam.ac.uk                                              #
#                http://www.ParticleStats.com                                 #
#                Centre for Trophoblast Research                              #
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

import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import csv
import pandas as pd

CsvFile = "PS_Out/Counter.Lat.Long.txt"
GeoData = pd.read_csv(CsvFile)
lat = GeoData['Latitude'].values
lon = GeoData['Longitude'].values

fig = plt.figure(figsize=(10, 5))
m = Basemap()           
m.drawcoastlines(color='gray', zorder=3)
m.fillcontinents(zorder=1)
m.drawcountries(color='gray', zorder=2)

m.scatter(lon, lat, latlon=True, c='red', marker='^', edgecolor='black', linewidth=1, s=50, alpha=0.5, zorder=4)

plt.savefig('PS_Out/map.png', bbox_inches='tight')
