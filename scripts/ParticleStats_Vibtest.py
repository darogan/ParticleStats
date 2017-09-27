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


import ParticleStats.ParticleStats_Inputs as PS_Inputs


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



sys.exit()


print "Output Files = ", OutName

import csv
import numpy as na
import datetime
import xlwt

TimeInterval = 250
NumArenas    = 24

ExptData = []

count = 0
while (count < NumArenas):
	ExptData.append([])
	count += 1

with open(options.CsvFile, 'rb') as csvfile:

	VibTestFile = csv.reader(csvfile, delimiter=',', quotechar='"')

	num = 0
	ImagePlane = 1

	print "ImageName,ImagePlane,Arena,X,Y,Zone,Distance,Segment"

	for element in VibTestFile:
		if( element[2] == "Arena"):
			if( num < 10):
				print ',' . join([O_Name, str(num), str(ImagePlane), 
								  element[3], element[5], element[6], 
								  element[8], element[10], element[12]])

			timestamp    = element[0].split(':')
			timestamp[0] = timestamp[0].lstrip("0")
			timestamp[1] = timestamp[1].lstrip("0")
			timestamp[2] = timestamp[2].lstrip("0")
			secs         = timestamp[2].split('.')

			if( len(timestamp[0]) < 1): timestamp[0] = 0
			if( len(timestamp[1]) < 1): timestamp[1] = 0
			if( len(timestamp[2]) < 1): timestamp[2] = 0
			if( len(secs[0]) < 1):      secs[0] = str(0)
			if( len(secs[1]) < 1):      secs[1] = str(0)

			#t = datetime.time(int(timestamp[0]), int(timestamp[1]), int(secs[0]), int(secs[1]))
			#timeSecs = ".".join(secs) 

			ExptData[ int(element[3])-1 ].append( [int(ImagePlane), float(element[3]), 
												   float(element[5]), float(element[6]), 
												   float(element[8]), float(element[10]), 
												   float(element[12]) ] )

			if(int(element[3]) == 24):	ImagePlane += 1
			num += 1


font0              = xlwt.Font()
font0.name         = 'Times New Roman'
font0.colour_index = 2
font0.bold         = True
style0             = xlwt.XFStyle()
style0.font        = font0
wb                 = xlwt.Workbook()



for i in range(len(ExptData)):

	ws = wb.add_sheet('i')

	for j in range(len(ExptData[i])):

		ws.write(ExptData[i][j][0],0,ExptData[i][j][0],style0)		
		ws.write(ExptData[i][j][0],1,ExptData[i][j][1],style0)
		ws.write(ExptData[i][j][0],2,ExptData[i][j][2],style0)
		ws.write(ExptData[i][j][0],3,ExptData[i][j][3],style0) 
		ws.write(ExptData[i][j][0],4,ExptData[i][j][4],style0)
		ws.write(ExptData[i][j][0],5,ExptData[i][j][5],style0)
		ws.write(ExptData[i][j][0],6,ExptData[i][j][6],style0) 

		print(i,",",j,",",ExptData[i][j])



wb.save('example.xls')

print
print "Finished", sys.argv[0]

#------------------------------------------------------------------------------
# FIN
#------------------------------------------------------------------------------
