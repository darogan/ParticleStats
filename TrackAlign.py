#!/usr/bin/env python
###############################################################################
# _____               _     ____  _        _            _    _ _              # 
#|_   _| __ __ _  ___| | __/ ___|| |_ __ _| |_ ___     / \  | (_) __ _ _ __   #
#  | || '__/ _` |/ __| |/ /\___ \| __/ _` | __/ __|   / _ \ | | |/ _` | '_ \  #
#  | || | | (_| | (__|   <  ___) | || (_| | |_\__ \_ / ___ \| | | (_| | | | | #
#  |_||_|  \__,_|\___|_|\_\|____/ \__\__,_|\__|___(_)_/   \_\_|_|\__, |_| |_| #
#                                                                |___/        #
#                                                                             #
###############################################################################
#       TrackAlign: Open source software for the analysis of tracked data     #
#                   to determine optimal parameters and alignment of tracks   #
#                                                                             #
#       Contact: Russell.Hamilton@bioch.ox.ac.uk                              #
#                http://www.darogan.co.uk/TrackStats                          #
#                Department of Biochemistry, South Parks Road,                #
#                University of Oxford OX1 3QU                                 #
#       Copyright (C) 2013 Russell S. Hamilton                                #
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

parser = OptionParser(usage="%prog [--xls1=ExcelFile1] [--xls2=ExcelFile2]",
                      version="%prog 2.001")


parser.add_option("--xls1", metavar="EXCELFILE1",
                  dest="ExcelFile1",
                  help="Name of first Excel File")
parser.add_option("--xls2", metavar="EXCELFILE2",
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
parser.add_option("--tif", metavar="TIFFILE1",
                  dest="TifFile",
		  help="Name of 8 bit Tif File 1")
parser.add_option("--imagesize", metavar="IMAGESIZE",
                  dest="imagesize", default=512,
                  help="ImageSize")
parser.add_option("--boundaryfilter", metavar="BOUNDARYFILTER",
                  dest="BoundaryFilter", action="store_true",
                  help="Use boundary filter - speeds up calculation")
parser.add_option("--flattentime", metavar="FLATTENTIME",
                  dest="FlattenTime", action="store_true",
                  help="Flatten the time component so all time points included at once")
parser.add_option("--interpolate", metavar="INTERPOLATE",
                  dest="Interpolate", action="store_true",
                  help="Interpolate inbetwen points at a 1px resolution")
parser.add_option("--distancerate", metavar="DISTANCERATE",
                  dest="DistanceRate", default="0.25",
                  help="The rate at which the distance score drops off e^(-distancerate)")
parser.add_option("--generatestats", metavar="GENERATESTATS",
                  dest="generatestats", action="store_true", 
                  help="Generate random tracks for the statistical significance score")
parser.add_option("--typerandomtracks", metavar="TYPERANDOMTRACKS",         
                  dest="TypeRandomTracks", default="RandomStuff",
                  help="The method of generating random tracks for statistical significance <InputWithNoise/InputWithRandom/Random/>")
parser.add_option("--ntracks", metavar="NTRACKS",    
		  dest="ntracks", default="1000",
                  help="The number of tracks to generate for the statistical significance")
parser.add_option("--NoiseAmount", metavar="NOISEAMOUNT", 
		  dest="NoiseAmount", default="5",
		  help="The amount of noise to add to the input coordinates if InputWithRandom")
parser.add_option("--AngMin", metavar="ANGMIN", 
		  dest="AngMin", default="0",
		  help="The minimum angle if the random coordinates should have a bias")
parser.add_option("--AngMax", metavar="ANGMAX", 
		  dest="AngMax", default="360",
		  help="The maxmum angle if the random coordinates should have a bias")
parser.add_option("--MagMin", metavar="MAGMIN", 
		  dest="MagMin", default="3",
		  help="The minimum magnituds if the random coordinates should have a bias")
parser.add_option("--MagMax", metavar="MAGMAX",
		  dest="MagMax", default="100",
		  help="The minimum magnituds if the random coordinates should have a bias")
parser.add_option("--FraMin", metavar="FRAMIN", 
		  dest="FraMin", default="2",
		  help="The statring frame for the random coords")
parser.add_option("--FraMax", metavar="FRAMAX", 
		  dest="FraMax", default="100",
		  help="The maximum frame for the random coords")
parser.add_option("-s", "--squares", metavar="SQUARES",
                  dest="Squares", default="4",
                  help="Number of squares (1,4,16,64,256,1024,4096): DEFAULT=4")
parser.add_option("-a", "--axis",
                  dest="Axis", action="store_true",
                  help="Axis Angle included as first coordinate points?")
parser.add_option("-p", "--polygon", metavar="POLYGON",
                  dest="Polygon",
                  help="Name of file containing polygon region coordinates")
parser.add_option("-g", "--grid",
                  dest="ShowGrid", action="store_true",
                  help="Toggle on / off the display of the grid")
parser.add_option("-r", "--rectangles",
                  dest="ShowRectangles", action="store_true",
                  help="Toggle on / off the display of the coloured rectangles")
parser.add_option("-c", "--arrows",
                  dest="ShowArrows", action="store_true",
                  help="Toggle on / off the display of the direction arrows")
parser.add_option("--ArrowColour", metavar="ARROWCOLOUR",
                  dest="ArrowColour", default="white",
                  help="Colour specification for the arrows: DEFAULT=white")
parser.add_option("--ROIColour", metavar="ROICOLOUR",
                  dest="ROIColour", default="white",
                  help="Colour specification for the ROI: DEFAULT=white")
parser.add_option("--scalerose",
                  dest="ScaleRose", action="store_true",
                  help="Scale the Rose Diagrams so axis scales to the data, not just to 100%")
parser.add_option("--pixelratio", metavar="PIXELRATIO",
                  dest="PixelRatio", default="1.00",
                  help="Pixel Ratio (nm per pixel): DEFAULT=1.00")
parser.add_option("--pixelratiomethod", metavar="PIXELRATIOMETHOD",
                  dest="PixelRatioMethod", default="multiply",
                  help="Pixel Ratio calculation method <multiply/divide>: \
                        DEFAULT=multiply")
parser.add_option("--flipY", metavar="FLIPY",
                  dest="FlipY", action="store_true",
                  help="Changes the default orientation for the Y axis. \
                        Default y=0 is at the top of the image")
parser.add_option("--gapOpen", metavar="gapOpening",
                  dest="gapOpen", default=5,
                  help="Gap opening penalty score.")
parser.add_option("--gapExt", metavar="gapExtend",
                  dest="gapExt", default=1,
                  help="Gap extension penalty score.")
parser.add_option("--Xi", metavar="Xi",
                  dest="Xi", default=6.7196,
                  help="Extreme Value Distribution parameters. Xi=shape.")
parser.add_option("--Mu", metavar="Mu",
                  dest="Mu", default=1.7095,
                  help="Extreme Value Distribution parameters. Mu=location.")
parser.add_option("--Sigma", metavar="Sigma",
                  dest="Sigma", default=11.4874,
                  help="Extreme Value Distribution parameters. Sigma=scale.")
parser.add_option("--SignificanceThreshold", metavar="SigThresh",
                  dest="SigThresh", default=0.01,
                  help="Cut off for the significance level for the matching trails DEFAULT=0.01.")
parser.add_option("--TimeTolerance", metavar="TimeTol",
                  dest="TimeTol", default=0,
                  help="Tolerance for matching the time frames. Setting value to 1 will add 1 frame tolerance to both the start and end of the trails to be matched. DEFAULT=0.")

(options, args) = parser.parse_args()

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

if( os.path.exists(str(options.ExcelFile1)) != 1):
        print "ERROR: Excel file 1 does not exists - check correct path and name"
        sys.exit(0)
if( os.path.exists(str(options.TifFile)) != 1):
        print "ERROR: Image file does not exists - check correct path and name", options.TifFile
        sys.exit(0)
if( os.path.exists(str(options.ExcelFile2)) != 1):
        print "ERROR: Excel file 2 does not exists - check correct path and name"
        sys.exit(0)
if( options.Polygon and os.path.exists(str(options.Polygon)) != 1):
        print "ERROR: Polygon file don't exists - check correct path and name"
        sys.exit(0)

if((int(options.Squares) != 4) and (int(options.Squares) != 1) and \
  ((math.sqrt(int(options.Squares)) %4) != 0 )) or \
  (int(options.Squares) > 4096):
        print "ERROR: Incompatible number of squares. "+\
	      "Must be 4,16,64,256,1024 or 4096"
        sys.exit(0)


###############################################################################
# LOAD IN THE REQUIRED MODULES ONLY AFTER MAIN USER OPTIONS CHECKED
###############################################################################
print "\nLoading External Modules...",
import ParticleStats_Inputs  as PS_Inputs
import ParticleStats_Outputs as PS_Outputs
import ParticleStats_Maths   as PS_Maths
import ParticleStats_Plots   as PS_Plots
import TrackAlign_Functions  as TA_Functions
import numpy as na
import Image
import re
print "  Loading complete\n\n"

Colours = ["blue","green","purple","orange","yellow",\
           "cyan","brown","magenta","silver","gold"]
Colours = Colours * 200

AxisColours = ["red","blue","purple","cyan"]


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

if(options.OutputType == "html"): 
	PS_Outputs.Print_HTMLHeaders()
TA_Functions.Print_Welcome(options.OutputType,FontSize_Text)

###############################################################################
# READ IN THE EXCEL FILES
###############################################################################

print
print "Loading Excel Files...",

FlipYImgSize = 0
if options.FlipY:
        print " + Y axis ajustment = y is 0 at bottom of image"
        FlipYImgSize = int(options.imagesize)

FDs = [] 
#READ IN EXCEL FILE 1 AND EXTRACT INFO
(InputDirName1, InputFileName1) = os.path.split(XLS1)
Coords1,Corrections1,Axes1 = PS_Inputs.ReadExcelCoords(XLS1,float(options.PixelRatio),\
					options.PixelRatioMethod,0,0,FlipYImgSize)
FDs.append({'InputDirName':InputDirName1,'InputFileName':InputFileName1,\
	    'Coords':Coords1, 'Corrections':Corrections1, 'Axes':Axes1 })

#READ IN EXCEL FILE 2 AND EXTRACT INFO
(InputDirName2, InputFileName2) = os.path.split(XLS2)
Coords2,Corrections2,Axes2 = PS_Inputs.ReadExcelCoords(XLS2,float(options.PixelRatio),\
					options.PixelRatioMethod,0,0,FlipYImgSize)
FDs.append({'InputDirName':InputDirName2,'InputFileName':InputFileName2,\
            'Coords':Coords2, 'Corrections':Corrections2, 'Axes':Axes2 })

del(InputDirName1,InputDirName2,InputFileName1,InputFileName2)
del(Coords1,Coords2,Corrections1,Corrections2,Axes1,Axes2)

if((options.OutputType == 'html') and \
  ((len(FDs[0]['Coords']) > 200) or (len(FDs[1]['Coords']) > 200) )):
	print len(FDs[0]['Coords'][0])
	print len(FDs[1]['Coords'][0])
	print PS_Inputs.Colourer("### Too many particles in input files - limit = 200 ###",\
				 "red",options.OutputType,"bold",FontSize_Titles)
	sys.exit()

print "Loading complete"

Colours   = ["red","blue","green","purple","orange","yellow",\
	     "silver","cyan","brown",]
Colours   = Colours * 100
Separator = "" + ("+"*90)


#Run the 1st coordset as the reference set
print "Running Coords Sets"

print "+ Excel File 1 =", FDs[0]['InputFileName']
print "  No sheets    =", len( FDs[0]['Coords'])
print "  No trails    =", len( FDs[0]['Coords'][0])
print "+ Excel File 2 =", FDs[1]['InputFileName']
print "  No sheets    =", len( FDs[1]['Coords'])
print "  No trails    =", len( FDs[1]['Coords'][0])

(InputIMGDir, InputIMGFile) = os.path.split(options.TifFile)
im  = Image.open(options.TifFile).convert("RGBA")
print "+ Image File   =", InputIMGFile, "(%d,%d)"%(im.size[0],im.size[1])

print "+ Smith-Waterman algorithm settings"
print "  Gap opening score   =",options.gapOpen
print "  Gap extension score =",options.gapExt

Polygon = [0.0,0.0]
if(options.Polygon):
        Polygon = PS_Inputs.ReadPolygonFile(options.Polygon)
        print "+ ROI Details  =", os.path.basename(options.Polygon), \
              "(",len(Polygon),"points)"

print PS_Inputs.Colourer(Separator,"grey",options.OutputType,"",FontSize_Text)

# Convert the coordinates into 2 separate arrays for Coords and Frames
# Necessary otherwise interpolating modifies the coords, which isn't good
Coords_R = []
Frames_R = []
Coords_R,Frames_R = TA_Functions.ConvertCoordinateFormat(\
			FDs[0]['Coords'][0],options.Interpolate)
Coords_C = []
Frames_C = []
Coords_C,Frames_C = TA_Functions.ConvertCoordinateFormat(\
			FDs[1]['Coords'][0],options.Interpolate)

# OK lets calculate some statistics parameters for significance
if options.generatestats:
	Type 		= str(options.TypeRandomTracks)
	ntracks		= int(options.ntracks)
	NoiseAmount 	= int(options.NoiseAmount) 
	AngMin 		= int(options.AngMin)
	AngMax		= int(options.AngMax)
	MagMin		= int(options.MagMin)
	MagMax		= int(options.MagMax)
	FraMin		= int(options.FraMin)
	FraMax		= int(options.FraMax)

	(RandCoords,Stats) = TA_Functions.GenerateRandomCoords(\
					Coords_R,Frames_R,Type,ntracks,im.size[0],NoiseAmount,\
					AngMin,AngMax,MagMin,MagMax,FraMin,FraMax)

	print "+ Parameters for the statistical significance calculation"
        print "  Type of random track generator =", Stats[0]
        print "  Number of generated tracks     =", Stats[1]
        print "  Image size for coordinate set  =", Stats[2]
        print "  Amount of noise added          =", Stats[3]
        print "  Minimum angle range            =", Stats[4]
        print "  Maximum angle range            =", Stats[5]
        print "  Minimum magnitude range        =", Stats[6]
        print "  Maximum magnitude range        =", Stats[7]
        print "  Minimum frame number           =", Stats[8]
        print "  Maximum frame number           =", Stats[9]

#	outputfile = open("BestScores_RefVs10000Rand.txt",'w')
#	outputfile.write("No\tscores\n")
#
#	i = 0
#	while i < len(FDs[0]['Coords'][0]):
#		print "%4d Reference Trail Vs Random Generated Set. "%i,
#
#		if options.BoundaryFilter:
#			boundary = TA_Functions.TrailBoundaryCalculation(Coords_R[i],512,512,1,1)
#
#		AllSimilarities = []
#		j = 0
#		while j < len(RandCoords):
#			Rand_Coords = []; Rand_Frames = []
#			k = 0
#			while k < len(RandCoords[j]):
#				Rand_Coords.append( [RandCoords[j][k][1],RandCoords[j][k][2]] )
#				Rand_Frames.append( RandCoords[j][k][4] )
#				k += 1
#
#			(Similarity,A_R,A_C) = TA_Functions.CompareTracks(\
#                	                                Coords_R[i],Rand_Coords,\
#                        	                        Frames_R[i],Rand_Frames,\
#                                	                boundary,options.BoundaryFilter,\
#                                        	        options.FlattenTime)
#			AllSimilarities.append( Similarity )
#			j += 1
#
#		print "\tBest Similarity = %8.4f"% max( AllSimilarities )
#		outputfile.write( str(i)+"\t"+"%.4f"%(max(AllSimilarities))+"\n" )
#
#		i += 1
#	outputfile.close()

	print PS_Inputs.Colourer(Separator,"grey",options.OutputType,"",FontSize_Text)


	MaxSimilarities = []
	FileWrite = 0
	if(FileWrite):
		outputfile = open("RandomScores_"+str(Type)+"_"+str(ntracks)+"_"+\
				  str(options.imagesize)+"_"+str(NoiseAmount)+"_"+\
				  str(AngMin)+"_"+str(AngMax)+"_"+str(MagMin)+"_"+str(MagMax)+"_"+\
				  str(FraMin)+"_"+str(FraMax)+".txt",'w')
	        outputfile.write("No\tlscores\tgscores\n")

        i = 0
        while i < len(RandCoords):
                print "%4d Randon Track Vs Reference Trails "%i,

		Rand_Coords = []; Rand_Frames = []
		k = 0
                while k < len(RandCoords[i]):
                	Rand_Coords.append([RandCoords[i][k][1],RandCoords[i][k][2]] )
                        Rand_Frames.append( RandCoords[i][k][4] )
                        k += 1

                if options.BoundaryFilter:
                        boundary = TA_Functions.TrailBoundaryCalculation(Rand_Coords,512,512,1,1)

                AllSimilarities = []
                j = 0
                while j < len(FDs[0]['Coords'][0]):

                        (Similarity,A_R,A_C,Cross) = TA_Functions.CompareTracks(\
                                                        Coords_R[j],Rand_Coords,\
                                                        Frames_R[j],Rand_Frames,\
                                                        boundary,options.BoundaryFilter,\
                                                        options.FlattenTime,\
							options.gapOpen,options.gapExt,options.TimeTol)
                        AllSimilarities.append( Similarity )
                        j += 1

                print "\tBest Similarity = %8.4f %8.4f"%\
		      (max(AllSimilarities),((max( AllSimilarities ) \
		      / len(FDs[0]['Coords'][0]))*100))

		MaxSimilarities.append( max(AllSimilarities)  )

		if(FileWrite):
                	outputfile.write( str(i)+"\t"+"%.4f\t"%(max(AllSimilarities))+\
				  "%.4f"%((max( AllSimilarities ) / len(FDs[0]['Coords'][0]))*100) +"\n" )

                i += 1

	if(FileWrite):  outputfile.close()

	(Xi,Mu,Sigma,eXi,eMu,eSigma) = TA_Functions.CalculateEVDParameters( MaxSimilarities )
else:
	Xi     = options.Xi
	Mu     = options.Mu
	Sigma  = options.Sigma
	eXi    = 0
	eMu    = 0
	eSigma = 0

print "+ EVD Parameter Estimates"
print "  location = %8.4f se = %8.4f"%(Mu, eMu)
print "  scale    = %8.4f se = %8.4f"%(Sigma,eSigma)
print "  shape    = %8.4f se = %8.4f"%(Xi,eXi)
print PS_Inputs.Colourer(Separator,"grey",options.OutputType,"",FontSize_Text)

if options.Polygon:

	cnt_ROI_R = 0
	cnt_ROI_C = 0

	# Check which of the reference trails are within the ROI
	ROI_Check_R = na.zeros(len(FDs[0]['Coords'][0]))
	i = 0
	while i < len(FDs[0]['Coords'][0]):
		j = 0
		while j < len(FDs[0]['Coords'][0][i]):
			x = FDs[0]['Coords'][0][i][j][4]
			y = FDs[0]['Coords'][0][i][j][5]
			if PS_Maths.CalculatePointInPolygon([x,y],Polygon):
				ROI_Check_R[i] = 1
				cnt_ROI_R += 1
				break
			j += 1
		i += 1

	# Check which of the query trails are within the ROI
        ROI_Check_C = na.zeros(len(FDs[1]['Coords'][0]))
        i = 0
        while i < len(FDs[1]['Coords'][0]):
                j = 0
                while j < len(FDs[1]['Coords'][0][i]):
                        x = FDs[1]['Coords'][0][i][j][4]
                        y = FDs[1]['Coords'][0][i][j][5]
                        if PS_Maths.CalculatePointInPolygon([x,y],Polygon):
                                ROI_Check_C[i] = 1
				cnt_ROI_C += 1
                                break
                        j += 1
                i += 1


print "+ ROI Membership"
print "  Reference Set has %5d/%-5d in ROI"%(cnt_ROI_R, len(FDs[0]['Coords'][0]))
print "  Query     Set has %5d/%-5d in ROI"%(cnt_ROI_C, len(FDs[1]['Coords'][0]))
print PS_Inputs.Colourer(Separator,"grey",options.OutputType,"",FontSize_Text)


#------------------------------------------------------------------------------
# THIS IS THE MAIN COMPARISON BIT OF THE CODE
#------------------------------------------------------------------------------

Results_All   = [] #na.zeros( (len(FDs[1]['Coords'][0]),3), na.Float64)
Hit_Details   = []
AllHitDetails = []

i = 0
while i < len(FDs[0]['Coords'][0]):

	MatchesUniq = []

	Hit_Details = []
	print "Query: %-4d NoPoints=%-3d Coords=[%6.2f,%6.2f][%6.2f,%6.2f]"%\
                (i, len(Coords_R[i]),\
		FDs[0]['Coords'][0][i][0][4],FDs[0]['Coords'][0][i][0][5],\
		FDs[0]['Coords'][0][i][-1][4],FDs[0]['Coords'][0][i][-1][5]) 

	if options.BoundaryFilter:
                boundary = TA_Functions.TrailBoundaryCalculation(Coords_R[i],im.size[0],im.size[0],1,1)
	
	if((options.Polygon and ROI_Check_R[i] == 1) or (len(Polygon) == 2)):
		hit_count = 0
		comp_count = 0
		j = 0
		while j < len(FDs[1]['Coords'][0]):

			if((options.Polygon and ROI_Check_C[j] == 1 and ROI_Check_R[i] == 1) or (len(Polygon) == 2)):
				(Similarity,A_R,A_C,CrossBound) = TA_Functions.CompareTracks(\
									Coords_R[i],Coords_C[j],\
									Frames_R[i],Frames_C[j],\
									boundary,options.BoundaryFilter,\
									options.FlattenTime,\
									options.gapOpen,options.gapExt,\
									options.TimeTol)

				if CrossBound == 1:
					comp_count += 1

				Significance = TA_Functions.SignificanceScore(Similarity,Xi,Mu,Sigma)

				#if Significance < float(options.SigThresh):
				if Significance < 0.001:
				
					#print "--------", i, j, Similarity, Significance
					MatchesUniq.append(j)

					#print "\t++", A_R, len(A_R), len(Coords_R[i])
					#print "\t--", A_C, len(A_C), len(Coords_C[j])
		
					(AlnR,AlnC) = TA_Functions.FormatAlignment(Coords_R[i],Coords_C[j],A_R,A_C)

					Hit_Details.append([i,hit_count,j,Similarity,Significance,\
							    A_R,A_C,AlnR,AlnC,len(Coords_C[j])])
					hit_count += 1
			j += 1

		if comp_count == 0:
			print "  - %5d matches: %5d tracks searched"%(0, 0)
		else:
			print "  + %5d matches: %5d tracks searched"%(hit_count, comp_count)
		AllHitDetails.append( Hit_Details )
	else:
		print "  + NOT IN ROI"
		AllHitDetails.append( ["NOT IN ROI"] )

	if len(MatchesUniq) > 0:
		Results_All.append(MatchesUniq)
	else:
		Results_All.append(-1)
	i += 1


#print PS_Inputs.Colourer(Separator,"grey",options.OutputType,"",FontSize_Text)
#i = 0
#while i < len(Results_All):
#	print i, Results_All[i]
#	i += 1

print PS_Inputs.Colourer(Separator,"grey",options.OutputType,"",FontSize_Text)


# Calculations over - now print out the results
i = 0
while i < len(FDs[0]['Coords'][0]):

        Angle = PS_Maths.CalculateVectorAngle([\
                        FDs[0]['Coords'][0][i][-1][4]-FDs[0]['Coords'][0][i][0][4],\
                        FDs[0]['Coords'][0][i][-1][5]-FDs[0]['Coords'][0][i][0][5]])

        if((options.Polygon and ROI_Check_R[i] == 1) or (len(Polygon) == 2)):
                print "Query: %-4d NoPoints=%-3d angle=%-3d Coords=[%6.2f,%6.2f][%6.2f,%6.2f] ROI=%1d"%\
                        (i, len(Coords_R[i]), Angle, \
                        FDs[0]['Coords'][0][i][0][4],FDs[0]['Coords'][0][i][0][5],\
                        FDs[0]['Coords'][0][i][-1][4],FDs[0]['Coords'][0][i][-1][5], ROI_Check_R[i])

		if options.BoundaryFilter:
                        print "\t    boundingbox=[%3.0f,%3.0f][%3.0f,%3.0f][%3.0f,%3.0f][%3.0f,%3.0f]"%\
                              (boundary[0][0],boundary[0][1],boundary[1][0],boundary[1][1],\
                              boundary[2][0],boundary[2][1],boundary[3][0],boundary[3][1] )
                else:
                        print

	#Print out the unique hit details
	hit_count = 0
	j = 0
	while j < len(AllHitDetails[i]):

		if AllHitDetails[i][0] != "NO SIGNIFICANT HITS" and \
		   AllHitDetails[i][0] != "NOT IN ROI":
			print "  + Match: %-4d Sbjct=%-4d LScore=%-6.2f "%\
                              (hit_count+1,AllHitDetails[i][j][2],AllHitDetails[i][j][3]),\
                      	      "P=%-.2e NoPoints=%-3d MatchCoverage=%f C=%s"%\
                              (AllHitDetails[i][j][4],AllHitDetails[i][j][9],\
                       	      (len(AllHitDetails[i][j][5])/len(Coords_R[i]))*100,\
			      Colours[AllHitDetails[i][j][1]])
			print "    Query:", AllHitDetails[i][j][7], len(AllHitDetails[i][j][5]), "/", len(Coords_R[i]),(len(AllHitDetails[i][j][5])/len(Coords_R[i]))
			print "    Sbjct:", AllHitDetails[i][j][8]
			hit_count += 1

		elif AllHitDetails[i][0] == "NO SIGNIFICANT HITS":
                        print "  + NO SIGNIFICANT HITS"
                elif AllHitDetails[i][0] == "NOT IN ROI":
                        print "  + NOT IN ROI"

        	j += 1

        # Make an image of the query train plus matching hits
        if hit_count > 0:
		ImageName = TA_Functions.PlotMatchingTrails("R"+str(i),im.size,options.TifFile,\
#                                  Coords_R[i],Coords_C,Results_All[i],Colours,Polygon,"white")
                                 FDs[0]['Coords'][0][i],FDs[1]['Coords'][0],Results_All[i],Colours,Polygon,"white")


	if hit_count == 0:
		print "  + NO UNIQ HITS"

	i += 1

print PS_Inputs.Colourer(Separator,"grey",options.OutputType,"",FontSize_Text)
print PS_Inputs.Colourer("### FIN ###","green",options.OutputType,"bold",FontSize_Text)
print PS_Inputs.Colourer(Separator,"grey",options.OutputType,"",FontSize_Text)

if(options.OutputType == "html"):
	PS_Outputs.Print_HTMLTails(BaseDir, DirGraphs, options.ExcelFile1, options.ExcelFile2 )

#------------------------------------------------------------------------------
# FIN
#------------------------------------------------------------------------------
