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

import os, sys, math
import os.path
from optparse import OptionParser


###############################################################################
# PARSE IN THE USER OPTIONS 
###############################################################################

parser = OptionParser(usage="%prog [--a=ExcelFile1] [--b=ExcelFile2]",
                      version="%prog 2.001")

parser.add_option("--vibtest", metavar="VIBTESTFILE",
                  dest="VibtestFile",
                  help="Name of Vibtest CSV File")
parser.add_option("-o", metavar="OUTPUTTYPE",
                  dest="OutputType", default="text",
                  help="print text ot html style output: DEFAULT=text")
parser.add_option("--outhtml", metavar="OUTPUTHTML",
                  dest="OutputHTML",
                  help="Specify a web location for the HTML output")
parser.add_option("--outdir", metavar="OUTPUTDIR",
                  dest="OutputDir",
                  help="Specify a directory for the output files")
parser.add_option("-g", "--graphs",
                  dest="graphs", action="store_true",
                  help="print graphs")

parser.add_option("-d", "--debug",
                  dest="debug", action="store_true",
                  help="print full debug output")
(options, args) = parser.parse_args()



#ERROR CHECK
if( os.path.exists(str(options.VibtestFile)) != 1):
        print "ERROR: VibTest file does not exists - check correct path and name"
        sys.exit(0)



###############################################################################
# LOAD IN THE REQUIRED MODULES ONLY AFTER MAIN USER OPTIONS CHECKED
###############################################################################
print "\nLoading External Modules..."
import ParticleStats.ParticleStats_Inputs  as PS_Inputs
import ParticleStats.ParticleStats_Outputs as PS_Outputs
import ParticleStats.ParticleStats_Maths   as PS_Maths
import ParticleStats.ParticleStats_Plots   as PS_Plots
import numpy as na
import re
print "Loading complete\n\n"

#Print the welcome logo plus data and run mode
FontSize_Titles = 2
FontSize_Text   = 1
#if(options.OutputType == "html"):
    #BaseDir = "http://idcws.bioch.ox.ac.uk/~rhamilto/ParticleStats2/"
#   BaseDir = ""
#else:
if(options.OutputHTML):
    BaseDir = options.OutputHTML
else:
    BaseDir = ""
#DirGraphs = BaseDir+"GraphOutput/"

if(options.OutputDir):
    DirGraphs = options.OutputDir
else:
    DirGraphs = os.getcwd()

DirTrails = BaseDir
ImageFileSearchPath = os.getcwd()

if(options.OutputType == "html"):
    PS_Outputs.Print_HTMLHeaders()
PS_Outputs.Print_Welcome(options.OutputType,FontSize_Text)

###############################################################################
# READ IN THE COORD FILES
###############################################################################

FDs = []
#READ IN EXCEL FILE 1 AND EXTRACT INFO

(InputDirName1, InputFileName1) = os.path.split(options.VibtestFile)

Coords1,Corrections1,Axes1 = PS_Inputs.ReadVibtest_SingleFile(options.VibtestFile, 250, 24)

FDs.append({'InputDirName':InputDirName1,'InputFileName':InputFileName1,\
			'Coords':Coords1, 'Corrections':Corrections1, 'Axes':Axes1 })

del(InputDirName1,InputFileName1)
del(Coords1,Corrections1,Axes1)

PS_Outputs.Print_Parameters( FDs[0]['InputFileName'],FDs[0]['Coords'], \
							 FDs[0]['InputFileName'],FDs[0]['Coords'], \
                 			 options.OutputType,FontSize_Text )

Colours   = ["red","blue","green","purple","orange","yellow",\
         "silver","cyan","brown","magenta","silver","gold"]
Colours   = Colours * 100
Separator = "" + ("+"*90)



###############################################################################
# RUN FUNCTIONS ON COORD DATA READ IN - MAIN PROGRAM LOOP
###############################################################################

RealAllRuns  = []
RealAllRunsX = []
RunsHash     = []
RunsHash2    = []
RunsHashAll  = []

coordset = 0
while coordset < len(FDs):
    
	print PS_Inputs.Colourer(("### Running Coords Set "+str(coordset+1)+" ###"),"black",\
                              options.OutputType,"bold",FontSize_Titles)
	print PS_Inputs.Colourer(" Coordinate File = "+FDs[coordset]['InputFileName'],"black",\
                              options.OutputType,"bold",FontSize_Text)

	AllRuns               = []
	AllRuns_X             = []
	Stats_Global_AveLen   = []
	Stats_Global_AveSpeed = [] 
	FileOut               = "" 
	RunCounter            = 0; 

	print len(FDs[coordset]['Coords'])
	print len(FDs[coordset]['Coords'][0])
	print len(FDs[coordset]['Coords'][0][0])


	i = 0
	while i < len(FDs[coordset]['Coords']): #cycle through sheets

		print "Sheet: ", i, " ", len(FDs[coordset]['Coords'][i])

		print "Trail:"
		print "\t", FDs[coordset]['Coords'][i][0]
		print "\t", FDs[coordset]['Coords'][i][-1]


		options.trails      = 1
		options.PixelRatio  = 1
		Regression          = 0
		ImageFileSearchPath = "/storage/Russell/Hackathon/zebrafish"
		# Perform Trail drawing
		IMG_Trails = ""
		if( options.trails):
			ArenaNum = int(1+FDs[coordset]['Coords'][i][0][3])
			ImageFiles = ImageFileSearchPath+"/"+FDs[coordset]['Coords'][i][0][0]+"_"+str(ArenaNum)+".png"
		else:
			ImageFiles = ""
            
		print "ImageFiles:", ImageFiles

		if( len(ImageFiles) > 0) and (options.trails):
			FirstImage = ImageFiles
			TrailImage = PS_Inputs.DrawTrailsOnImageFile(FirstImage,i,\
                                     FDs[coordset]['InputFileName'],Colours[i],\
                                     FDs[coordset]['Coords'][i],\
                                     options.PixelRatio,Regression, "/storage/Russell/Hackathon/zebrafish/Results")

#		j = 0
#		while j < len(FDs[coordset]['Coords'][i]): #cycle through       

#			print FDs[coordset]['Coords'][i][j]

#			print PS_Inputs.Colourer(Separator,"grey",options.OutputType,"",FontSize_Text)
#
#
#			# Perform Cummulative Distance plotting 
#			if(options.graphs):
#				DistanceCummulativePlot = PS_Plots.PlotDistanceVsTimeCummulative(\
#											FDs[coordset]['Coords'][i][j],i,j,\
#											("Coords"+str(coordset+1)),"msecs","nm",DirGraphs)
#			j += 1
		i += 1

	coordset += 1





#------------------------------------------------------------------------------
# FIN
#------------------------------------------------------------------------------