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
import csv
import numpy as np
import pandas as pd
from optparse import OptionParser
from datetime import datetime
from dateutil import parser as dsparser

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
                  dest="OutputDir", default="Results",
                  help="Specify a directory for the output files")
parser.add_option("-g", "--graphs",
                  dest="graphs", action="store_true",
                  help="print graphs")
parser.add_option("--imagesearchpath", metavar="IMAGESEARCHPATH",
                  dest="ImageSearchPath",
                  help="Specify a directory containing the arena blank images for the experiment")
parser.add_option("--pixelratio", metavar="PIXELRATIO",
                  dest="PixelRatio", default="1.00",
                  help="Pixel Ratio (nm per pixel): DEFAULT=1.00")
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
print "\nChecking Python Version... ", sys.version_info[0], ".", sys.version_info[1]

print "Loading External Modules..."
import ParticleStats.ParticleStats_Inputs  as PS_Inputs
import ParticleStats.ParticleStats_Outputs as PS_Outputs
import ParticleStats.ParticleStats_Maths   as PS_Maths
import ParticleStats.ParticleStats_Plots   as PS_Plots
import numpy as na
import re
print "Loading complete\n"

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

Coords1,Corrections1,Axes1,Perturbations1,TotalFrames1 = PS_Inputs.ReadVibtest_SingleFile(options.VibtestFile, 250, 24)

FDs.append({'InputDirName':InputDirName1,'InputFileName':InputFileName1,\
			'Coords':Coords1, 'Corrections':Corrections1, 'Axes':Axes1,\
			'Perturbations':Perturbations1, 'TotalFrames':TotalFrames1 })

del(InputDirName1,InputFileName1)
del(Coords1,Corrections1,Axes1)
del(Perturbations1,TotalFrames1)

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

# Create specified results directory
print PS_Inputs.Colourer(("### Creating Results Directory "+str(options.OutputDir)+" ###"),"black",\
                          options.OutputType,"bold",FontSize_Titles)
if not os.path.exists(options.OutputDir):
	os.makedirs(options.OutputDir)


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

	# Lets look at the experimental design
	print "+ There are ", len(FDs[coordset]['Perturbations']), " perturbation events in the experiment"
	Perturbations         = FDs[coordset]['Perturbations']
	minCyclePerturbations = min([_[4] for _ in Perturbations])
	maxCyclePerturbations = max([_[4] for _ in Perturbations])
	minEventPerturbations = min([_[5] for _ in Perturbations]) 
	maxEventPerturbations = max([_[5] for _ in Perturbations])
	print "Perturbations Cycle min ", minCyclePerturbations, " max ", maxCyclePerturbations
	print "Perturbations Event min ", minEventPerturbations, " max ", maxEventPerturbations

	Perturbs = []

	i = 0
	while i < len(Perturbations):
		j = 1
		while j <= maxCyclePerturbations:
		
			if((Perturbations[i][4] == j) and (Perturbations[i][5] == minEventPerturbations)):
				#print Perturbations[i][6], "from:", Perturbations[i][2], "[", Perturbations[i][3], "]",
		
				(sTSa,sTSb) = dsparser.parse(Perturbations[i][3]).strftime('%Y-%m-%d %H:%M:%S.%f').split('.')
				sTS         = datetime.strptime(str("%s.%03d" % (sTSa, int(sTSb) / 1000)), '%Y-%m-%d %H:%M:%S.%f')

			if((Perturbations[i][4] == j) and (Perturbations[i][5] == maxEventPerturbations)):

				(eTSa,eTSb) = dsparser.parse(Perturbations[i][3]).strftime('%Y-%m-%d %H:%M:%S.%f').split('.')
				eTS         = datetime.strptime(str("%s.%03d" % (eTSa, int(eTSb) / 1000)), '%Y-%m-%d %H:%M:%S.%f')
				duration    = eTS - sTS

				#print "to:", Perturbations[i][2], "[", Perturbations[i][3], "]",
				#print "duration: ", duration, "[", duration.total_seconds(), "]"

				Perturbs.append( [ Perturbations[i][6], j-1, sTS, eTS, duration ] )
			j += 1
		i += 1

	ExptPlotName = PS_Plots.PlotExperimentalDesign(FDs[coordset]['Perturbations'], FDs[coordset]['TotalFrames'])
	print "ExptPlotName = ", ExptPlotName

	#Pertub_CummulativeDistanceTable = []
	Pertub_CummulativeDistanceTable = pd.DataFrame()

	i = 0
	while i < len(FDs[coordset]['Coords']): #cycle through sheets

		print "Num coords = ", len(FDs[coordset]['Coords'][0])

		Arena_Perturb_Coords = []
		j = 0
		while j < len(FDs[coordset]['Coords'][i]): #cycle through       

			(TSa,TSb) = dsparser.parse(str(FDs[coordset]['Coords'][i][j][-1])).strftime('%Y-%m-%d %H:%M:%S.%f').split('.')
			timestamp = datetime.strptime(str("%s.%03d" % (TSa, int(TSb) / 1000)), '%Y-%m-%d %H:%M:%S.%f')

			#print "Timestamp = ", timestamp, " (", FDs[coordset]['Coords'][i][0][-1], ")"
			#print "test prestartle=", Perturb_PreStartle[0][1]
			#print "test duration=", (Perturb_PreStartle[0][1]-timestamp).total_seconds()
			#print "ts.time =", timestamp.time()
			#print "pre.time=", Perturb_PreStartle[0][1].time()

			k = 0
			while k < len(Perturbs):

				if((timestamp.time() >= Perturbs[k][2].time()) and \
                   (timestamp.time() <= Perturbs[k][3].time())):
					#print Perturbs[k][0], "#:", k+1, "ts=",timestamp.time(), \
					#	  ",pre=",Perturbs[k][2].time(), \
					#	  ", coord=",FDs[coordset]['Coords'][i][j]
					Arena_Perturb_Coords.append( [ Perturbs[k][0], Perturbs[k][1], FDs[coordset]['Coords'][i][j] ] )
				k += 1
			j += 1



		# Do something with perturb coords (PLOTS)
		print "Perturbation Summary Tables..."

		PerturbTab     = PS_Plots.PerturbationPlots(Arena_Perturb_Coords, i+1, 
                                                    len(Pertub_CummulativeDistanceTable),str(options.OutputDir))
		PerturbTab_pd  = pd.DataFrame(PerturbTab, columns = ["CoordNum", "ArenaNum", "CoordCount", "EventType", \
                                                             "EventNum", "PointDistance", "CummulativeDistance", "X", "Y"])
		PerturbTab_agg = PerturbTab_pd.groupby(["ArenaNum", "EventType","EventNum"])['CummulativeDistance'].max().reset_index()
		print PerturbTab_agg
		Pertub_CummulativeDistanceTable = pd.concat( [Pertub_CummulativeDistanceTable, PerturbTab_agg] )
		print len(Pertub_CummulativeDistanceTable)




		print "Arena: ", int(i+1), " ", len(FDs[coordset]['Coords'][i])

		print "Trail:"
		print "\t", FDs[coordset]['Coords'][i][0]
		print "\t", FDs[coordset]['Coords'][i][-1]


		options.trails      = 1
		Regression          = 0
		ImageFileSearchPath = options.ImageSearchPath
		# Perform Trail drawing
		IMG_Trails = ""
		if( options.trails):
			ArenaNum = int(FDs[coordset]['Coords'][i][0][3])
			ImageFiles = ImageFileSearchPath+"/"+FDs[coordset]['Coords'][i][0][0]+"_"+str(ArenaNum)+".png"
		else:
			ImageFiles = ""
            
		print "ImageFiles:", ImageFiles

		if( len(ImageFiles) > 0) and (options.trails):
			FirstImage = ImageFiles
			print "pixelRatio=", options.PixelRatio
			TrailImage = PS_Inputs.DrawTrailsOnImageFile(FirstImage,i,\
                                     FDs[coordset]['InputFileName'],Colours[i],\
                                     FDs[coordset]['Coords'][i],\
                                     options.PixelRatio,Regression,options.OutputDir,0.1)

		#j = 0
		#while j < len(FDs[coordset]['Coords'][i]): #cycle through       
        #        
		#	if(j < 5):    
		#		print "\t", j, "\t",  FDs[coordset]['Coords'][i][j]
		#	j += 1

		# Perform Cummulative Distance plotting 
		#options.graphs = 0
		DistanceCummulativePlot,Distance = PS_Plots.PlotDistanceVsTimeCummulativeBehavioural(\
                                                        FDs[coordset]['Coords'][i],i,j,\
                                                        ("Coords"+str(coordset+1)),"time-units","dist-units",\
                                                        500000, 1000,
														DirGraphs, options.graphs)
		print "TotalDistance, "+ImageFileSearchPath+", "+str(i+1)+", "+str(Distance)

		i += 1

	print Pertub_CummulativeDistanceTable
	print Pertub_CummulativeDistanceTable.reset_index()

	Peturb_CSV_File = str(options.OutputDir)+'/'+str(options.OutputDir)+'_'+'perturb_test_arena_All'+'.csv'
	print "Writing to:", Peturb_CSV_File
	Pertub_CummulativeDistanceTable.to_csv(Peturb_CSV_File, sep=",", index=True)

	#with open(str(options.OutputDir)+'/'+str(options.OutputDir)+'_'+'perturb_test_arena_All'+'.csv','w') as perturb_csv:
	#	perturb_csv_writer = csv.writer(perturb_csv, delimiter=',', lineterminator='\n')
	#	perturb_csv_writer.writerow(['CoordNum','ArenaNum','CoordCount', 'EventType', \
    #                                 'EventNum', 'PointDistance','CummulativeDistance','X','Y'])

	#	perturb_csv_writer.writerow( Pertub_CummulativeDistanceTable.reset_index() )
	#	perturb_csv.close()


	coordset += 1





#------------------------------------------------------------------------------
# FIN
#------------------------------------------------------------------------------
