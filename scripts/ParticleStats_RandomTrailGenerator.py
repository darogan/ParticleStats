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

import os,sys,math,os.path

from optparse import OptionParser
###############################################################################
# PARSE IN THE USER OPTIONS 
###############################################################################

parser = OptionParser(usage="%prog -x <Excel>",
                      version="%prog 0.1")

parser.add_option("-x", "--xls", metavar="EXCELFILE",
                  dest="ExcelFile",
                  help="Name of Excel File")

parser.add_option("-n", "--ntrails", metavar="NTRAILS",
                  dest="ntrails", default="1000",
                  help="Number of trails to generate")
parser.add_option("-i", "--imagesize", metavar="IMAGESIZE",
                  dest="imagesize",
                  help="Image Size to constrain particles")
parser.add_option("--type", metavar="TYPE",
                  dest="Type",
                  help="Type of coordinates: RandomNoise/Random ")


parser.add_option("--angleMin", metavar="ANGLEMIN",
                  dest="angleMin",default="0",
                  help="Minimum angle in range")
parser.add_option("--angleMax", metavar="ANGLEMAX",
                  dest="angleMax", default="360",
                  help="Maximum angle in range")
parser.add_option("--magnitudeMin", metavar="MAGNITUDEMIN",
                  dest="magnitudeMin",default="5",
                  help="Minimum magnitude in range")
parser.add_option("--magnitudeMax", metavar="ANGLEMAX",
                  dest="magnitudeMax", default="360",
                  help="Maximum magnitude in range")
parser.add_option("--frameMin", metavar="FRAMEMIN",
                  dest="frameMin",default="5",
                  help="Minimum frame in range")
parser.add_option("--frameMax", metavar="FRAMEMAX",
                  dest="frameMax", default="15",
                  help="Maximum frame in range")


(options, args) = parser.parse_args()

###############################################################################
# LOAD IN THE REQUIRED MODULES ONLY AFTER MAIN USER OPTIONS CHECKED
###############################################################################

import numarray as na
import random
import ParticleStats_Maths as PS_Maths
import ParticleStats_Inputs as PS_Inputs

###############################################################################
# MAIN CODE STARTS HERE
###############################################################################

#Read in a set of coordinates
Coords,Corrections,Axis = PS_Inputs.ReadExcelCoords(options.ExcelFile,1.0,0,0)

if options.Type == "InputWithNoise":
	print "Track #\tX\tY\tZ\tFrame #\tImage Name"
	NoiseAmount = 5
	i = 0
        while i < len(Coords):
		j = 0
                while j < len(Coords[i]):
			k = 0
			while k < len(Coords[i][j]):
				Noise = random.uniform( (-1*NoiseAmount),NoiseAmount )

				X1 = Coords[i][j][k][4] + Noise 
				Y1 = Coords[i][j][k][5] + Noise

				if(X1 > 0 and Y1 > 0 and X1 < int(options.imagesize) and \
				   Y1 < int(options.imagesize) ):
					print "%d\t%.2f\t%.2f\t%d\t%d\t%s"%\
						(j+1,X1,Y1,1,Coords[i][j][k][1],Coords[i][j][k][0])
				else:
					k -= 1
				k += 1
			print
                        j += 1
		i += 1


if options.Type == "Random":
	AngMin = int(options.angleMin)
	AngMax = int(options.angleMax)
	MagMin = int(options.magnitudeMin)
	MagMax = int(options.magnitudeMax)
	FraMin = int(options.frameMin)
	FraMax = int(options.frameMax)

if options.Type == "InputWithRandom":
	AngRange = []
	MagRange = []
	FraRange = []

	i = 0
	while i < len(Coords):
	        j = 0
	        while j < len(Coords[i]):
			MagRange.append(PS_Maths.Calculate2PointsDistance(\
					Coords[i][j][0][4],Coords[i][j][0][5],\
					Coords[i][j][-1][4],Coords[i][j][-1][5]))
			AngRange.append(PS_Maths.CalculateVectorAngle([\
					Coords[i][j][-1][4]-Coords[i][j][0][4],\
					Coords[i][j][-1][5]-Coords[i][j][0][5]]))

	                k = 0
	                while k < len(Coords[i][j]):
                                FraRange.append(Coords[i][j][k][1])
        	                k += 1
                	j += 1
	        i += 1

	FraMin = min(FraRange); FraMax = max(FraRange)
	AngMin = min(FraRange); AngMax = max(AngRange)
	MagMin = min(FraRange); MagMax = max(MagRange)

if options.Type == "Random" or options.Type == "InputWithRandom":
	print "Track #\tX\tY\tZ\tFrame #\tImage Name"

	i = 0
        while i < int(options.ntrails):
                Ang      = random.uniform(AngMin,AngMax)
		Mag      = random.uniform(MagMin,MagMax)
		Fra      = random.randrange(FraMin,FraMax)
		FraStart = random.randrange(0,(100-Fra))
		X1       = random.uniform(0,int(options.imagesize))
        	Y1       = random.uniform(0,int(options.imagesize))
		X2,Y2 = PS_Maths.GetCircleEdgeCoords(X1,Y1,Ang,Mag)

		if(X1 > 0 and Y1 > 0 and X1 < int(options.imagesize) and \
                   Y1 < int(options.imagesize) and X2 > 0 and Y2 > 0 and \
		   X2 < int(options.imagesize) and Y2 < int(options.imagesize) ):
			print "%d\t%.2f\t%.2f\t%d\t%d\trandomimage.tif"%\
                                                (i+1,X1,Y1,1,FraStart)
			j = 1
			while j <= Fra:
	                	X2,Y2 = PS_Maths.GetCircleEdgeCoords(X1,Y1,Ang,(Mag/Fra))
				if(X2 > 0 and Y2 > 0 and X2 < int(options.imagesize) and \
                                   Y2 < int(options.imagesize) ):
					print "%d\t%.2f\t%.2f\t%d\t%d\trandomimage.tif"%\
                                                (i+1,X2,Y2,1,FraStart+j)
					X1 = X2
					Y1 = Y2
				else:
					j -= 1
				j += 1
			print
		else:
			i -= 1
		i += 1

###############################################################################
# FIN
###############################################################################
