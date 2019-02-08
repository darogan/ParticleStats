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


parser.add_option("-a", "--xls1", metavar="EXCELFILE1",
                  dest="ExcelFile1",
                  help="Name of first Excel File")
parser.add_option("-b", "--xls2", metavar="EXCELFILE2",
                  dest="ExcelFile2",
                  help="Name of second Excel File")

parser.add_option("-o", metavar="OUTPUTTYPE",
                  dest="OutputType", default="text",
                  help="print text ot html style output: DEFAULT=text")
parser.add_option("--outdir", metavar="OUTPUTDIR",
                  dest="OutputDir",
                  help="Specify a directory for the output files")
parser.add_option("--outhtml", metavar="OUTPUTHTML",
                  dest="OutputHTML",
                  help="Specify a web location for the HTML output")
parser.add_option("--trackingtype", metavar="TrackingType",
                  dest="TrackingType", default="999",
		  help="Source of tracked coords: DEFAULT=metamorph")
parser.add_option("-g", "--graphs", 
                  dest="graphs", action="store_true",
                  help="print graphs")
parser.add_option("-t", "--trails", 
                  dest="trails", action="store_true",
                  help="print trails")
parser.add_option("-r", "--regression", 
                  dest="regression", action="store_true",
                  help="Run linear regression analysis")
parser.add_option("-d", "--debug", 
                  dest="debug", action="store_true",
                  help="print full debug output")
parser.add_option("--timestart",
                  dest="TimeStart", metavar="TIMESTART",
                  default="0",
                  help="Provide a time point start point for movement calculations")
parser.add_option("--timeend",
                  dest="TimeEnd", metavar="TIMEEND",
                  default="90",
                  help="Provide a time point end point for movement calculations")
parser.add_option("--pausedefinition", metavar="PAUSEDEF",
                  dest="PauseDef", default="distance",
                  help="Pause definition: speed or distance DEFAULT=distance")
parser.add_option("--rundistance", metavar="RUNDISTANCE", 
                  dest="RunDistance", default="1.1",
                  help="Run Distance in nm: DEFAULT=1.1")
parser.add_option("--runframes", metavar="RUNFRAMES",
                  dest="RunFrames", default="0",
                  help="Run Frames: DEFAULT=0")
parser.add_option("--pausedistance", metavar="PAUSEDISTANCE", 
                  dest="PauseDistance", default="10",
                  help="Pause Distance in nm: DEFAULT=10")
parser.add_option("--pauseduration", metavar="PAUSEDURATION", 
                  dest="PauseDuration", default="2000",
                  help="Pause Duration in miliseconds: DEFAULT=2000")
parser.add_option("--pausespeed", metavar="PAUSESPEED",
                  dest="PauseSpeed", default="0.25",
                  help="Pause Speed: DEFAULT=0.25")
parser.add_option("--pauseframes", metavar="PAUSEFRAMES",
                  dest="PauseFrames", default="3",
                  help="Pause Frames: DEFAULT=3")
parser.add_option("--reverseframes", metavar="REVERSEFRAMES",
                  dest="ReverseFrames", default="2",
                  help="Reverse Frames: DEFAULT=2")
parser.add_option("--flipY", metavar="FLIPY",
                  dest="FlipY", action="store_true",
                  help="Changes the default orientation for the Y axis. \
			Default y=0 is at the top of the image")
parser.add_option("--imagesize", metavar="IMAGESIZE",
                  dest="ImageSize", default="512",
                  help="Image size to define the range of the coordinates DEFAULT=512")
parser.add_option("--pixelratio", metavar="PIXELRATIO", 
                  dest="PixelRatio", default="1.00",
                  help="Pixel Ratio (nm per pixel): DEFAULT=1.00")
parser.add_option("--pixelratiomethod", metavar="PIXELRATIOMETHOD",
                  dest="PixelRatioMethod", default="multiply",
                  help="Pixel Ratio calculation method <multiply/divide>: \
                        DEFAULT=multiply")
parser.add_option("--dimensions", metavar="DIMENSIONS", 
                  dest="Dimensions", default="2D",
                  help="Number of dimensions (1DX, 1DY, 2D): DEFAULT=2D")

(options, args) = parser.parse_args()

options.RunDistance   = float(options.RunDistance) 
options.PauseDuration = float(options.PauseDuration)
options.PauseDistance = float(options.PauseDistance)
options.ReverseFrames = float(options.ReverseFrames)
options.PixelRatio    = float(options.PixelRatio)
options.TimeStart     = int(options.TimeStart)
options.TimeEnd       = int(options.TimeEnd)

if (options.OutputType != "html") and (options.OutputType != "text"):
        print "Error with input parameters (run -h flag for help)"
	print "--output must be html or text"
	sys.exit()

if options.ExcelFile1 and options.ExcelFile2:
        XLS1 = options.ExcelFile1
        XLS2 = options.ExcelFile2
else:
	print "Error with input parameters (run -h flag for help)"
	print "Two Excel Files must be provided"
	sys.exit()

if options.graphs: Graphs = "graphs"
else:              Graphs = "nographs"

if options.PauseDef != "speed" and options.PauseDef != "distance":
	print "Error with input parameters (run -h flag for help)"
        print "Pause Definition must be either speed or distance"
        sys.exit()
else:
	if options.PauseDef == "speed":		PauseDef = 1
	elif options.PauseDef == "distance":	PauseDef = 2


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
#	BaseDir = ""
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
# READ IN THE EXCEL FILES
###############################################################################

if options.FlipY:
	FlipYImgSize = int(options.ImageSize)
else:
	FlipYImgSize = 0

FDs = [] 
#READ IN EXCEL FILE 1 AND EXTRACT INFO
(InputDirName1, InputFileName1) = os.path.split(XLS1)
Coords1,Corrections1,Axes1 = PS_Inputs.ReadExcelCoords(XLS1,options.PixelRatio,\
						       options.PixelRatioMethod,\
						       options.TimeStart,options.TimeEnd,\
						       FlipYImgSize)

FDs.append({'InputDirName':InputDirName1,'InputFileName':InputFileName1,\
	    'Coords':Coords1, 'Corrections':Corrections1, 'Axes':Axes1 })

#READ IN EXCEL FILE 2 AND EXTRACT INFO
(InputDirName2, InputFileName2) = os.path.split(XLS2)
Coords2,Corrections2,Axes2 = PS_Inputs.ReadExcelCoords(XLS2,options.PixelRatio,\
						       options.PixelRatioMethod,\
						       options.TimeStart,options.TimeEnd,\
						       FlipYImgSize)
FDs.append({'InputDirName':InputDirName2,'InputFileName':InputFileName2,\
            'Coords':Coords2, 'Corrections':Corrections2, 'Axes':Axes2 })

del(InputDirName1,InputDirName2,InputFileName1,InputFileName2)
del(Coords1,Coords2,Corrections1,Corrections2,Axes1,Axes2)

if((options.OutputType == 'html') and \
  ((len(FDs[0]['Coords']) > 200) or (len(FDs[1]['Coords']) > 200) )):
	print len(FDs[0]['Coords'])
	print len(FDs[1]['Coords'])
	print PS_Inputs.Colourer("### Too many particles in input files - limit = 200 ###",\
				 "red",options.OutputType,"bold",FontSize_Titles)
	sys.exit()

PS_Outputs.Print_Parameters( FDs[0]['InputFileName'],FDs[0]['Coords'], \
			     FDs[1]['InputFileName'],FDs[1]['Coords'], \
			     options.OutputType,FontSize_Text )

Colours   = ["red","blue","green","purple","orange","yellow",\
	     "silver","cyan","brown","magenta","silver","gold"]
Colours   = Colours * 100
Separator = "" + ("+"*90)

#sys.exit(0)

###############################################################################
# DRAW IMAGE STACK
###############################################################################

#print "\tReading Image Stack"
#ImageStack = ParticleStats_Inputs.ReadImageFiles("")
#ParticleStats_Inputs.DrawCoords(ImageStack,Coords,"geo",Colours)


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
	print PS_Inputs.Colourer(" Excel File = "+FDs[coordset]['InputFileName'],"black",\
        	                  options.OutputType,"bold",FontSize_Text)

	AllRuns               = []
	AllRuns_X             = []
	Stats_Global_AveLen   = []
	Stats_Global_AveSpeed = []
	FileOut               = ""
	RunCounter            = 0;

	i = 0
	while i < len(FDs[coordset]['Coords']): #cycle through sheets
		j = 0
		while j < len(FDs[coordset]['Coords'][i]): #cycle through 		
			print PS_Inputs.Colourer(Separator,"grey",options.OutputType,"",FontSize_Text)
			# Sort out the coordinate alignment corrections
			if len(FDs[coordset]['Corrections']) != 4:
				print PS_Inputs.Colourer(" Applying correction coordinates ",\
							 "black",options.OutputType,"bold",FontSize_Text)

				FDs[coordset]['Coords'][i][j] = PS_Maths.CorrectCoordinates(\
									FDs[coordset]['Coords'][i][j],\
									FDs[coordset]['Corrections'])
			
			# Perform Cummulative Distance plotting
			if(options.graphs):
				DistanceCummulativePlot = PS_Plots.PlotDistanceVsTimeCummulative(\
								FDs[coordset]['Coords'][i][j],i,j,\
	       	                                   		("Coords"+str(coordset+1)),"msecs",\
								"nm",DirGraphs) 
				if(options.OutputType=="html"):
					IMG_Particle = "<A HREF='"+ BaseDir + DirGraphs+\
						       str(DistanceCummulativePlot)+".png'"+\
						       " TARGET=_blank><IMG WIDTH=200 "+\
						       "SRC='"+ BaseDir + DirGraphs + "/" +\
       	                                	       str(DistanceCummulativePlot)+".png' BORDER=0></A>"
       	        		elif(options.OutputType=="text"): 
	                        	IMG_Particle = " Graph: Cummulative Distance vs Time "+\
	                                	       str(DistanceCummulativePlot)+".png"
			else: 
				if(options.OutputType=="html"):
					IMG_Particle = " <FONT SIZE=1>Graph:<BR>NO IMAGE AVAILABLE</FONT>"
				else:
					IMG_Particle = " Graph: NO IMAGE AVAILABLE"	

			# Perform the linear regression but not the graph just yet
			if(options.regression):
                                Regression = PS_Maths.KymoRegression(FDs[coordset]['Coords'][i][j],4,5)
				#Regression = PS_Maths.Regression_CVersion(FDs[coordset]['Coords'][i][j],4,5)

                                print " Regression=[X=%6.3f,"%Regression['X'],\
                                      "Intercept=%6.0f,"%Regression['Intercept'],\
                                      "R2=%6.3f,"%Regression['R2'],"]"
                                      #"aR2=%6.3f"%Regression['aR2'],"]"
			else:
				Regression = ""

			# Perform Trail drawing
			IMG_Trails = ""
			if( options.trails):
				ImageFiles = PS_Inputs.FindImageFiles(\
						FDs[coordset]['Coords'][i][j][0][0],ImageFileSearchPath)
			else:
				ImageFiles = []
	
			if( len(ImageFiles) > 0) and (options.trails):
				PatternN = re.compile(r'.*020.tif')
				k = 0
				while k < len(ImageFiles):
					IMG_Trails = " Trail Image:      NO IMAGE AVAILABLE"
					if (PatternN.match(os.path.basename(ImageFiles[k]))):
						FirstImage = ImageFiles[k]
						TrailImage = PS_Inputs.DrawTrailsOnImageFile(FirstImage,i,\
 								FDs[coordset]['InputFileName'],Colours[i][j],\
								FDs[coordset]['Coords'][i][j],\
								options.PixelRatio,Regression)
				        	if( (options.OutputType == "html") and ( options.trails) ):
							IMG_Trails = "<A HREF='"+ DirTrails + TrailImage + \
								     "' TARGET=_blank><IMG WIDTH=200 " + \
								     "HEIGHT=187 " + "SRC='" + DirTrails + \
								     TrailImage + "' BORDER=0></A>"
						elif( (options.OutputType == "text") and ( options.trails) ):
							IMG_Trails = " Trail Image:"+TrailImage
					
						break
					k += 1
			else:
				if(options.OutputType == "html"):
					IMG_Trails = "<FONT SIZE=1>Trail Image:<BR>NO IMAGE AVAILABLE</FONT>"
				else:
					IMG_Trails = " Trail Image:      NO IMAGE AVAILABLE"

			Runs   = []
			Runs = PS_Maths.FindLongMovementsAndPausesRaquel( \
					FDs[coordset]['Coords'][i][j], Regression,\
					FDs[coordset]['Axes'],PauseDef, \
					options.RunDistance,options.RunFrames, \
					options.PauseDistance,options.PauseSpeed, \
					options.PauseFrames,options.PauseDuration,\
					options.ReverseFrames,options.PixelRatio,\
					options.Dimensions,\
					options.TimeStart, options.TimeEnd,\
					options.debug)
	
			Stats_Particle  = PS_Maths.Stats_Particle(Runs)
			Stats_Standards = PS_Maths.Stats_Standards(Runs)

			RunsHash.append({'CoordsSet':coordset,'Sheet':i,'Particle':j,'Runs':Runs})
			RunsHashAll.append({'CoordsSet':coordset,'Sheet':i,'Particle':j,'Runs':Runs})
	
			AllRuns.append(Runs)
	
       		 	print "Runs for particle %4d sheet %2d" % (j, i),
 		        print " (Excel Row=", FDs[coordset]['Coords'][i][j][0][6], \
			      " File=", FDs[coordset]['InputFileName'], ")"
	       	 	print " No Coords =", len(FDs[coordset]['Coords'][i][j]), \
			      " No +ve Runs = ", Stats_Particle['No_Runs_P'], \
			      " No -ve Runs = ", Stats_Particle['No_Runs_N'], \
	      		      " No Pauses = ", Stats_Particle['No_Runs_0']

			RunLine   = ""
			StatsLine = ""
			Header    = " Event      Start End Dir   Dist  SDist" +\
		                    "  RDist  Angle  Speed SSpeed RSpeed   Time"
			print  PS_Inputs.Colourer(Header,"grey",options.OutputType,"italics",FontSize_Text)

			k = 0
			while k < len(Runs):

				AllRuns_X.append(Runs[k])
				Error   = ""
				if(   Runs[k][2] >  0): Event = "Run  "; Colour = "red"  
				elif( Runs[k][2] <  0): Event = "Run  "; Colour = "blue"
				elif( Runs[k][2] == 0): Event = "Pause"; Colour = "green"

				#if(abs(Runs[j][5]) <=  200 and abs(Runs[j][6]) <=  200 \
       	        	        #    and Runs[j][2] != 0):
				#	Colour = "purple"; Error = "ERROR? " + Event
				#elif(   abs(Runs[j][3]) >  300 and Runs[j][2] == 0):
       		 	        #        Colour = "cyan"; Error = "? " + Event

				RunLine = PS_Outputs.Print_RunLine(Runs,k,Event,Error)
				print  PS_Inputs.Colourer(RunLine,Colour,options.OutputType,\
							  "",FontSize_Text)

				RunCounter += 1
				FileOut += PS_Outputs.Print_FileOut(Runs, RunCounter, i, k)

				k += 1

			StatsLine = PS_Outputs.Print_ParticleStatsLine(Stats_Particle,Stats_Standards)
			print StatsLine

			# Perform Linear Regression Graph drawing 
                        if(options.regression):
                                #Regression = PS_Maths.KymoRegression(FDs[coordset]['Coords'][i][j],4,5)
                                #print " Regression=[X=%6.3f,"%Regression['X'],\
                                #      "Intercept=%6.0f,"%Regression['Intercept'],\
                                #      "R2=%6.3f,"%Regression['R2'],\
                                #      "aR2=%6.3f"%Regression['aR2'],"]"

                                RegressionGraph = PS_Plots.RegressionGraph(\
                                                  FDs[coordset]['Coords'][i][j],(coordset+1),i,j,\
						  Regression,FDs[coordset]['Axes'],Runs,DirGraphs)

                                if( options.OutputType=="html"):
                                        IMG_Regression = "<A HREF='"+BaseDir+DirGraphs+RegressionGraph+".png" + \
                                                         "' TARGET=_blank><IMG WIDTH=200 HEIGHT=187 " + \
                                                         "SRC='"+BaseDir+DirGraphs+RegressionGraph+".png' " + \
                                                         "BORDER=0></A>"
                                elif( options.OutputType=="text"):
                                        IMG_Regression = " Regression Image: "+RegressionGraph+".png"
                        else:
                                Regression = ""

                                if(options.OutputType=="html"):
                                        IMG_Regression = " <FONT SIZE=1>Regression Image:"+\
                                                         "<BR>NO IMAGE AVAILABLE</FONT"
                                else:
                                        IMG_Regression = " Regression Image: NO IMAGE AVAILABLE"


			if(options.OutputType == "text"):
				print IMG_Particle
				print IMG_Trails
				print IMG_Regression
			elif(options.OutputType == "html"):
				print "<TABLE WIDTH=100%><TR><TD>"+IMG_Particle+"</TD>"+\
                		      "<TD VALIGN=middle>"+IMG_Trails+"</TD>"+\
				      "<TD VALIGN=middle>"+IMG_Regression+"</TD>"+\
				      "</TR></TABLE>"
			j += 1

			if(options.graphs and j == (len(FDs[coordset]['Coords'][i]))):
				RoseDiagram = PS_Plots.PlotCompareRoseDiagram(RunsHash,500,coordset,i,DirGraphs)
				convert = "inkscape --export-png="+DirGraphs+"/"+RoseDiagram+\
				          ".png --export-dpi=125 "+DirGraphs+"/"+RoseDiagram+".svg 2>/dev/null"
				os.popen(convert)
				if(options.OutputType=="html"):
					IMG_Rose = "<B>Rose Diagram For Sheet "+str(i)+"</B><BR>" + \
						   "<A HREF='"+BaseDir+DirGraphs+RoseDiagram+".png" + \
                                                   "' TARGET=_blank><IMG WIDTH=200 HEIGHT=187 " + \
                                                   "SRC='"+BaseDir+DirGraphs+RoseDiagram+".png' " + \
                                                   "BORDER=0></A>"
				else:
					IMG_Rose =  "  RoseDiagram      = "+RoseDiagram+".svg\n"+\
					            "  RoseDiagram      = "+RoseDiagram+".png\n"
				print IMG_Rose
				RunsHash2.append(RunsHash)
				RunsHash = []
		i += 1

	print PS_Inputs.Colourer(Separator,"grey",options.OutputType,"",FontSize_Text)

	# Print Out some Global stats
	print PS_Inputs.Colourer("### Global Statistics ###","green",\
				 options.OutputType,"bold",FontSize_Titles)
	Stats_Global = {}
	Stats_Global = PS_Maths.Stats_Particle(AllRuns_X)

	Stats_Standards = {}
	Stats_Standards = PS_Maths.Stats_Standards(AllRuns_X)

	GlobalStats = PS_Outputs.Print_GlobalStats ( AllRuns_X, Stats_Global, Stats_Standards )
	print GlobalStats

	Stats_Global_AveLen.append(   [Stats_Global['Ave_RunLen_P'],Stats_Global['Ave_RunLen_N'],\
	                               Stats_Standards['D_P_E'],Stats_Standards['D_N_E'] ] )
	Stats_Global_AveSpeed.append( [Stats_Global['Ave_Speed_P'],Stats_Global['Ave_Speed_N'],\
	                               Stats_Standards['S_P_E'],Stats_Standards['S_N_E'] ] )

	# Call the graph drawing functions
	print PS_Inputs.Colourer("### Produce Output Files ###","green",\
				 options.OutputType,"bold",FontSize_Titles)

	if( options.graphs):
	        print PS_Inputs.Colourer((" Creating Runs graph for Coords Set "+\
				         str(coordset+1)+"..."),"black",\
	              			 options.OutputType,"",FontSize_Text)
		PS_Plots.PlotRuns(AllRuns,options.PixelRatio,Colours,\
				  ("Coords"+str(coordset+1)),DirGraphs)

		#PS_Plots.PlotRunsFreq(AllRuns,Colours,("Coords"+str(coordset+1)),DirGraphs)

	#Write Run Data Out to the Data File
	print PS_Inputs.Colourer(" Creating Output Table for Coords Set "+str(coordset+1)+\
				 "...","black",options.OutputType,"",FontSize_Text)
	PS_Outputs.Print_OutputFile((DirGraphs+"/ParticleStats_Coords"+str(coordset+1)+"_Output.text"),FileOut)

	print PS_Inputs.Colourer("","green",options.OutputType,"bold",FontSize_Text)
	print PS_Inputs.Colourer("","green",options.OutputType,"bold",FontSize_Text)
	print PS_Inputs.Colourer("","green",options.OutputType,"bold",FontSize_Text)
	print PS_Inputs.Colourer("","green",options.OutputType,"bold",FontSize_Text)

	RealAllRuns.append(AllRuns)
	RealAllRunsX.append(AllRuns_X)

	coordset += 1

RoseDiagram = PS_Plots.PlotCompareRoseDiagram(RunsHashAll,500,0,99,DirGraphs)
convert = "inkscape --export-png="+DirGraphs+"/"+RoseDiagram+".png --export-dpi=125 "+\
	  DirGraphs+RoseDiagram+".svg 2>/dev/null"
os.popen(convert)
print "RoseDiagram   (coordsset=0)            =", RoseDiagram
RoseDiagram = PS_Plots.PlotCompareRoseDiagram(RunsHashAll,500,1,99,DirGraphs)
convert = "inkscape --export-png="+DirGraphs+"/"+RoseDiagram+".png --export-dpi=125 "+\
	  DirGraphs+RoseDiagram+".svg 2>/dev/null"
os.popen(convert)
print "RoseDiagram   (coordsset=1)            =", RoseDiagram


ThreeFrameResults = PS_Maths.ThreeFrameRunAnalysis(RunsHashAll,FDs,DirGraphs)
print "3 Frame Results                        =", len(ThreeFrameResults)
ThreeFrameGraph   = PS_Plots.PlotThreeFrameResults(ThreeFrameResults,0,DirGraphs)
print "3 Frame Graph (coordsset=0)            =", ThreeFrameGraph
ThreeFrameGraph   = PS_Plots.PlotThreeFrameResults(ThreeFrameResults,1,DirGraphs)
print "3 Frame Graph (coordsset=1)            =", ThreeFrameGraph

ThreeFrameMaxResults = PS_Maths.ThreeFrameMaxRunAnalysis(RunsHashAll,FDs,DirGraphs)
print "3 Frame Max Results                    =", len(ThreeFrameMaxResults)
ThreeFrameMaxGraph   = PS_Plots.PlotThreeFrameMaxResults(ThreeFrameMaxResults,0,DirGraphs)
print "3 Frame Max Graph (coordsset=0)        =", ThreeFrameMaxGraph
ThreeFrameMaxGraph   = PS_Plots.PlotThreeFrameMaxResults(ThreeFrameMaxResults,1,DirGraphs)
print "3 Frame Max Graph (coordsset=1)        =", ThreeFrameMaxGraph

DirChangeResults  = PS_Maths.DirectionChangesAnalysis(RunsHashAll,0,DirGraphs)
print "Direction Change Results (coordsset=0) =", len(DirChangeResults)
DirChangeGraph    = PS_Plots.PlotDirChangeResults(DirChangeResults,0,DirGraphs)
print "Direction Changes Graph (coordsset=0)  =", DirChangeGraph
DirChangeResults  = PS_Maths.DirectionChangesAnalysis(RunsHashAll,1,DirGraphs)
print "Direction Change Results (coordsset=1) =", len(DirChangeResults)
DirChangeGraph    = PS_Plots.PlotDirChangeResults(DirChangeResults,1,DirGraphs)
print "Direction Changes Graph (coordsset=0)  =", DirChangeGraph


# OK Lets do some stats comparisons between the two excel files
print PS_Inputs.Colourer("### Comparison Statistics ###","green",\
			 options.OutputType,"bold",FontSize_Titles)
print PS_Inputs.Colourer(" Comparing Coords Set 1 to Coords Set 2","black",\
			 options.OutputType,"",FontSize_Text)
print PS_Inputs.Colourer("     "+FDs[0]['InputFileName']+" vs "+FDs[1]['InputFileName'],\
			 "black",options.OutputType,"",FontSize_Text)

Output = PS_Maths.Stats_TTests(RealAllRunsX[0],RealAllRunsX[1])

print Output

# Plot Average Run Length for the 2 coords sets
if( options.graphs):
	print ""
	#PS_Plots.PlotAveRunLength(Stats_Global_AveLen)
	#PS_Plots.PlotSpeed(Stats_Global_AveSpeed)

print PS_Inputs.Colourer("### FIN ###","green",options.OutputType,"bold",FontSize_Text)
print PS_Inputs.Colourer(Separator,"grey",options.OutputType,"",FontSize_Text)

if(options.OutputType == "html"):
	PS_Outputs.Print_HTMLTails(BaseDir, DirGraphs, options.ExcelFile1, options.ExcelFile2 )

#------------------------------------------------------------------------------
# FIN
#------------------------------------------------------------------------------
