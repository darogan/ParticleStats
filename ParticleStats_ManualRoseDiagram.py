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
#                Department of Biochemistry, South Parks Road,                #
#                University of Oxford OX1 3QU                                 #
#       Copyright (C) 2010 Russell S. Hamilton                                #
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
import numarray as na
from optparse import OptionParser
import random

###############################################################################
# PARSE IN THE USER OPTIONS 
###############################################################################

parser = OptionParser(usage="%prog [-x Excel [-t tif] [-s squares]",
                      version="%prog 0.1")

parser.add_option("--scalerose",
                  dest="ScaleRose", action="store_true",
                  help="Scale the Rose Diagrams so axis scales to the data, not just to 100%")

(options, args) = parser.parse_args()

###############################################################################
# LOAD IN THE REQUIRED MODULES ONLY AFTER MAIN USER OPTIONS CHECKED
###############################################################################

import ParticleStats_Plots   as PS_Plots
import ParticleStats_Maths   as PS_Maths

Colours = ["red","blue","green","purple","orange","yellow",\
           "cyan","brown","magenta","silver","gold"]
Colours = Colours * 20000

AxisColours = ["red","blue","purple","cyan"]
AxisLabels  = "DVAP"

print "Running", sys.argv[0]
print

#ManualCounts = [58,30,31,84,38,19,23,36] 
#OutName = "Manual-ALL"

#ManualCounts = [28,17,20,45,21,9,16,19]  #L15
#OutName = "Manual-L15"

ManualCounts = [30,11,11,19,17,10,7,19] #M15
OutName = "Manual-M15"

TrailVectorsAll = []
AngleStep = 45

i = 0
while i < len(ManualCounts):

	print AngleStep*i, AngleStep*(i+1)

        j = 0
	while j <= ManualCounts[i]:

		Ang = random.uniform(AngleStep*i,(AngleStep*(i+1)-1))
                (X,Y) = PS_Maths.GetCircleEdgeCoords(20,20,Ang,10)

		print "\t", j, Ang, X,Y, X-20,Y-20,PS_Maths.CalculateVectorAngle([X-20,Y-20])

		TrailVectorsAll.append( [X-20,Y-20] )

		j += 1
	i += 1


AxesLabels = [ "D","V","A","P" ]

RoseDiagram      = PS_Plots.PlotRoseDiagram(OutName,"_rosediagram_wmag",\
					    TrailVectorsAll,1,AngleStep,500,\
					    AxisColours,options.ScaleRose,AxisLabels)
print " + RoseDiagram      =", RoseDiagram+".svg"
convert = "inkscape --export-png="+RoseDiagram+\
          ".png --export-dpi=125 "+RoseDiagram+".svg 2>/dev/null"
os.popen(convert)
print " + RoseDiagram      =", RoseDiagram+".png"



RoseDiagram2      = PS_Plots.PlotRoseDiagram(OutName,"_rosediagram_nomag",\
					     TrailVectorsAll,0,AngleStep,500,\
					     AxisColours,options.ScaleRose,AxisLabels)
print " + RoseDiagram2     =", RoseDiagram2+".svg"
convert = "inkscape --export-png="+RoseDiagram2+\
          ".png --export-dpi=125 "+RoseDiagram2+".svg 2>/dev/null"
os.popen(convert)
print " + RoseDiagram2     =", RoseDiagram2+".png"

RoseDiagram5      = PS_Plots.PlotRoseDiagram(OutName,"_rosediagram_180seg",\
                                             TrailVectorsAll,0,180,500,\
                                             AxisColours,options.ScaleRose,AxisLabels)
print " + RoseDiagram5     =", RoseDiagram5+".svg"
convert = "inkscape --export-png="+RoseDiagram5+\
          ".png --export-dpi=125 "+RoseDiagram5+".svg 2>/dev/null"
os.popen(convert)
print " + RoseDiagram5     =", RoseDiagram5+".png"

print " + Direction Table          ="
DirectionTable = PS_Plots.PlotDirectionTable(TrailVectorsAll)

PS_Maths.CalcRayleighTest(TrailVectorsAll)
print
print "Finished", sys.argv[0]

#------------------------------------------------------------------------------
# FIN
#------------------------------------------------------------------------------
