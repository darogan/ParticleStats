#!/usr/bin/env python
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

import os,sys,math,os.path
import numpy as na
from optparse import OptionParser


import numpy as na
from PIL import Image, ImageFont, ImageDraw, ImageColor, ImageEnhance
import random, glob, re
import ParticleStats.ParticleStats_Maths   as PS_Maths
import ParticleStats.ParticleStats_Inputs  as PS_Inputs
import ParticleStats.ParticleStats_Plots   as PS_Plots
import ParticleStats.ParticleStats_Outputs as PS_Outputs
import ParticleStats.ParticleStats_Plots   as PS_Plots


###############################################################################
# PARSE IN THE USER OPTIONS 
###############################################################################

parser = OptionParser(usage="%prog [--csv <e.g. vibtest.csv>]",
                      version="%prog 0.1")

parser.add_option("--csv", metavar="TXTFILE",
                  dest="CsvFile",
                  help="CSV file containing comma separated values from vibtest output")

(options, args) = parser.parse_args()

###############################################################################
# LOAD IN THE REQUIRED MODULES ONLY AFTER MAIN USER OPTIONS CHECKED
###############################################################################

print "Running", sys.argv[0]
print

(O_Dir,O_File) = os.path.split(options.CsvFile)
(O_Name,O_Ext) = os.path.splitext(O_File)
OutName =  O_Name , ".xls"

TimeInterval = 250
NumArenas    = 24

Coords = PS_Inputs.ReadVibtest_SingleFile(options.CsvFile, TimeInterval, NumArenas)




print
print "Finished", sys.argv[0]

#------------------------------------------------------------------------------
# FIN
#------------------------------------------------------------------------------
