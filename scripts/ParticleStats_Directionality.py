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
from optparse import OptionParser

###############################################################################
# PARSE IN THE USER OPTIONS 
###############################################################################

parser = OptionParser(usage="%prog [-x Excel [-i imagefile] [-s squares]",
                      version="%prog 0.1")

parser.add_option("-o", "--outputtype", metavar="OUTPUTTYPE",
                  dest="OutputType", default="text",
                  help="print text ot html style output: DEFAULT=text")
parser.add_option("--outdir", metavar="OUTPUTDIR",
                  dest="OutputDir",
                  help="Specify a directory for the output files")
parser.add_option("--outhtml", metavar="OUTPUTHTML",
                  dest="OutputHTML",
                  help="Specify a web location for the HTML output")
parser.add_option("-x", "--xls", metavar="EXCELFILE",
                  dest="ExcelFile",
                  help="Name of Excel File")
parser.add_option("-i", "--image", metavar="IMAGEFILE",
                  dest="ImageFile",
                  help="Name of image file: Tif(8bit)/PNG/GIF/JPG")
parser.add_option("-s", "--squares", metavar="SQUARES",
                  dest="Squares", default="4",
                  help="Number of squares (1,4,16,64,256,1024,4096): DEFAULT=4")
parser.add_option("-a", "--axis", 
                  dest="Axis", action="store_true",
                  help="Axis Angle included as first coordinate points?")
parser.add_option("-p", "--polygon", metavar="POLYGON",
                  dest="Polygon",
                  help="Name of file containing polygon region coordinates")
parser.add_option("--magrange", metavar="MAGRANGE",
                  dest="PixStep", default="4.00",
                  help="Magnitude range for drequency plots: DEFAULT=4")
parser.add_option("--pixelratio", metavar="PIXELRATIO",
                  dest="PixelRatio", default="1.00",
                  help="Pixel Ratio (nm per pixel): DEFAULT=1.00")
parser.add_option("--pixelratiomethod", metavar="PIXELRATIOMETHOD",
                  dest="PixelRatioMethod", default="multiply",
                  help="Pixel Ratio calculation method <multiply/divide>: \
			DEFAULT=multiply")
parser.add_option("--orient", metavar="ORIENT",
                  dest="Orient", default="0",
                  help="Set the orientation (vertical=0, horizontal=90): DEFAULT=0")
parser.add_option("--flipY", metavar="FLIPY",
                  dest="FlipY", action="store_true",
                  help="Changes the default orientation for the Y axis. \
			Default y=0 is at the top of the image")
parser.add_option("-g", "--grid",
                  dest="ShowGrid", action="store_true",
                  help="Toggle on / off the display of the grid")
parser.add_option("-r", "--rectangles",
                  dest="ShowRectangles", action="store_true",
                  help="Toggle on / off the display of the coloured rectangles")
parser.add_option("-c", "--arrows",
                  dest="ShowArrows", action="store_true",
                  help="Toggle on / off the display of the direction arrows")
parser.add_option("--ArrowColour", metavar="COLOUR",
                  dest="ArrowColour", default="white",
                  help="Colour specification for the arrows: DEFAULT=white")
parser.add_option("--SquareColours", metavar="COLOUR",
                  dest="SquareColours", default="angle",
                  help="Colour specification for the windmap square colours [angle|speed]: DEFAULT=angle")
parser.add_option("--SquareColoursSpeedRangeMin", metavar="SPEEDRANGEMIN",
                  dest="SquareColoursSpeedRangeMin", default=5,
                  help="WindMap: An integer range to define minimum speed to scale: DEFAULT=5")
parser.add_option("--SquareColoursSpeedRangeMax", metavar="SPEEDRANGEMAX",
                  dest="SquareColoursSpeedRangeMiax", default=20,
                  help="WindMap: An integer range to define maximum speed to scale: DEFAULT=20")
parser.add_option("--ROIColour", metavar="COLOUR",
                  dest="ROIColour", default="white",
                  help="Colour specification for the ROI: DEFAULT=white")
parser.add_option("--scalerose",
                  dest="ScaleRose", action="store_true",
                  help="Scale the Rose Diagrams so axis scales to the data, not just to 100%")
parser.add_option("--AxisLabels", metavar="AXISLABELS",
                  dest="AxisLabels", default="NSWE",
                  help="Specification direction axis labels e.g. North/South/West/East: DEFAULT=NSWE")
parser.add_option("--TimeInterval", metavar="TIMEINTERVAL",
                  dest="TimeInterval", default=5,
                  help="Time Interval between data collection point in kymograph: Default=5secs")

(options, args) = parser.parse_args()


#ERROR CHECK
if( os.path.exists(str(options.ExcelFile)) != 1):
        print "ERROR: Excel file does not exists - check correct path and name"
        sys.exit(0)
#if( os.path.exists(str(options.ImageFile)) != 1):
#        print "ERROR: Image file does not exists - check correct path and name", options.ImageFile
#        sys.exit(0)

(FileName,FileExt) = os.path.splitext(options.ImageFile)
if FileExt != ".tif" and FileExt != ".jpg"  and FileExt != ".gif" and \
   FileExt != ".png" and FileExt != ".jpeg" and FileExt != ".tiff":
	print "ERROR: Image file is not in a supported forrmat Tif(8bit)/PNG/JPG/GIF", options.ImageFile
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

if( (int(options.Orient) != 0) and (int(options.Orient) != 90) ):
	print "ERROR: orientation must be either 0 or 90"
	sys.exit(0)

if options.SquareColours != "angle" and options.SquareColours != "speed":
	print "ERROR: SquareColours is not set to the allowed options of angle or speed"
	sys.exit(0)


SquareColoursSpeedRangeMin = int(options.SquareColoursSpeedRangeMin)
if SquareColoursSpeedRangeMin < 0 or SquareColoursSpeedRangeMin > 200:
        print "ERROR: the wind map speed min range is outside of the allowed range 1..200"
        sys.exit(0)


SquareColoursSpeedRangeMax = int(options.SquareColoursSpeedRangeMax)

if SquareColoursSpeedRangeMax < 0 or SquareColoursSpeedRangeMax > 200:
        print "ERROR: the wind map speed max range is outside of the allowed range 1..200"
        sys.exit(0)

###############################################################################
# LOAD IN THE REQUIRED MODULES ONLY AFTER MAIN USER OPTIONS CHECKED
###############################################################################

import numpy as na
import Image, ImageFont, ImageDraw, ImageColor, ImageEnhance
import random, glob, re
import ParticleStats_Maths   as PS_Maths
import ParticleStats_Inputs  as PS_Inputs
import ParticleStats_Plots   as PS_Plots
import ParticleStats_Outputs as PS_Outputs
import ParticleStats_Plots  as PS_Plots

Colours = ["red","blue","green","purple","orange","yellow",\
           "cyan","brown","magenta","silver","gold"]
Colours = Colours * 20000

AxisColours = ["red","blue","purple","cyan"]

AxisLabels = str(options.AxisLabels)

#AxesLabels = [ "D","V","A","P" ]

DPI=str(250)

FontSize_Titles = 2
FontSize_Text   = 1
if(options.OutputType == "html"):
        PS_Outputs.Print_HTMLHeaders()
PS_Outputs.Print_Welcome(options.OutputType,FontSize_Text)

if(options.OutputDir):
	BaseDir = str(options.OutputDir)
else:
	BaseDir = ""

if(options.OutputType == "html" ):
        URL = str(options.OutputHTML)

im  = Image.open(options.ImageFile).convert("RGBA")

print "Running", sys.argv[0]
print
print " + Excel File       =", os.path.basename(options.ExcelFile)
print " + ImageFile        =", os.path.basename(options.ImageFile)
print " + Squares          =", options.Squares
print " + Image Size       =", im.size
print " + Pixel Ratio      =", options.PixelRatio

if(options.Orient == 0):
	print " + Orientation      = Vertical(", options.Orient,")"
else:
        print " + Orientation      = Horizontal(", options.Orient,")"


# Some tracking programs put y=0 at the bottom of the image
FlipYImgSize = 0
if options.FlipY:
	print " + Y axis ajustment = y is 0 at bottom of image"
        FlipYImgSize = int(im.size[0])*float(options.PixelRatio)


FlipYImgSize = 0
Coords,Corrections,Axes = PS_Inputs.ReadExcelCoords(options.ExcelFile,\
			  float(options.PixelRatio),\
			  options.PixelRatioMethod,0,0,FlipYImgSize)
FlipYImgSize = 1

Polygon = [0.0,0.0]
if(options.Polygon):
	Polygon = PS_Inputs.ReadPolygonFile(options.Polygon)
	print " + Polygon  Details =", os.path.basename(options.Polygon), \
	      "(",len(Polygon),"points)"

	if options.FlipY:
		i = 0
		while i < len(Polygon):
			Polygon[i][1] = (im.size[1] - Polygon[i][1])
			i += 1



print " + Number of Tracks =",len(Coords[0])
print " + Number of Sheets =",len(Coords)

Squares         = int(options.Squares)
Factor          = math.sqrt(Squares)
TrailsAll       = []
TrailVectorsAll = []

hyp = math.sqrt( (im.size[0]**2 + im.size[1]**2))
FinalIMSize = PS_Maths.roundNumber(hyp,5,"UP")

print " + Factor           =", Factor
print " + Final Image Size =", FinalIMSize, " Hyp=", hyp

#outputfile = open(str(options.OutputDir)+"directionality_results.txt",'w')
i = 0
while i < len(Coords):
	print " + Sheet Number =", i+1

	if(options.Axis):
		Axis = [Coords[i][0][0][4],Coords[i][0][0][5],\
               	        Coords[i][0][1][4],Coords[i][0][1][5]]
                del Coords[i][0]

		if options.FlipY:
			Axis[1] = (im.size[1] - Axis[1])
			Axis[3] = (im.size[1] - Axis[3])

                print "\t+ Axis definition  = [%.1f,%.1f] to [%.1f,%.1f]"%\
                      (Axis[0],Axis[1],Axis[2],Axis[3])

                AxisAngle = PS_Maths.CalculateVectorAngle([Axis[2]-Axis[0],\
                                                           Axis[3]-Axis[1]])
                if AxisAngle != 90:
			Rotate    = (360 - AxisAngle) + int(options.Orient)
                else:
                        Rotate = 0

		if Rotate > 359:
			Rotate = Rotate % 360

#		Rotate    = (360 - AxisAngle)
#		Rotate     = AxisAngle

#                RotImgSz  = (im.size[0]*math.sin(math.radians(Rotate%90)))+\
#                            (im.size[1]*math.cos(math.radians(Rotate%90)))
                RotImgSz  = (im.size[0]*math.sin(math.radians(Rotate)))+\
                            (im.size[1]*math.cos(math.radians(Rotate)))
                Shifty    = ((FinalIMSize-RotImgSz)/2) + \
                            ((RotImgSz/2)-(im.size[0]/2))
                Shift     = [Shifty,Shifty]
                Origin    = [ im.size[0]/2,im.size[1]/2 ]

                Shift     = [(FinalIMSize-im.size[0])/2,(FinalIMSize-im.size[1])/2]

                (Axis[0],Axis[1]) = PS_Maths.rotateXYbyAngAndOrigin(\
                                             Axis[0],Axis[1],Rotate,\
                                             Origin[0],Origin[1],0,Shift)
                (Axis[2],Axis[3]) = PS_Maths.rotateXYbyAngAndOrigin(\
                                             Axis[2],Axis[3],Rotate,\
                                             Origin[0],Origin[1],0,Shift)
	else:
		print "\t+ Axis definition  = NONE"
		Axis 	  = [0]
                AxisAngle = 0
                Rotate    = 0
                Origin    = [0,0]
                Shift     = [(FinalIMSize-im.size[0])/2,(FinalIMSize-im.size[1])/2]

	print "\t+ Axis VAngle      =", AxisAngle
        print "\t+ Rotate           =", Rotate
        print "\t+ Origin Rotate    =", Origin
        print "\t+ Shift            =", Shift
        print "\t+ No. Tracks       =", len(Coords[i])

	#Applies the rotation the coords
	j = 0
	while j < len(Coords[i]):
        	(Coords[i][j][0][4],Coords[i][j][0][5]) = \
					PS_Maths.rotateXYbyAngAndOrigin(\
                                        Coords[i][j][0][4],Coords[i][j][0][5],\
                                        Rotate,Origin[0],Origin[1],0,Shift)
                (Coords[i][j][-1][4],Coords[i][j][-1][5]) = \
                                	PS_Maths.rotateXYbyAngAndOrigin(\
                                        Coords[i][j][-1][4],Coords[i][j][-1][5],\
                                        Rotate,Origin[0],Origin[1],0,Shift)
		j += 1
	#Applies the rotation the polygon
	if(options.Polygon):
	        j = 0
	        while j < len(Polygon):
	                (Polygon[j][0],Polygon[j][1]) = \
	                                        PS_Maths.rotateXYbyAngAndOrigin(\
	                                        Polygon[j][0],Polygon[j][1],\
	                                        Rotate,Origin[0],Origin[1],0,Shift)
	                j += 1

	Trails            = []
        TrailVectors      = []
	TrailVectorAngles = []
	TrailVectors_ROI  = []
	TrailNoPoints     = []

        j = 0
        while j < len(Coords[i]):
        	Trails.append( [Coords[i][j][0][4],Coords[i][j][0][5], \
                                Coords[i][j][-1][4],Coords[i][j][-1][5] ] )
		TrailVectors.append ( [Coords[i][j][-1][4]-Coords[i][j][0][4],\
                                       Coords[i][j][-1][5]-Coords[i][j][0][5] ] )
                TrailsAll.append( Trails[j] )
 		TrailNoPoints.append( len(Coords[i][j]) )
		TrailVectorAngles.append( PS_Maths.CalculateVectorAngle(TrailVectors[j]) )
                TrailVectorsAll.append( TrailVectors[j] )
		TrailVectors_ROI.append( [0.0,0.0] )
#                Outty = "%.4f\n"%float((math.pi/180)*\
#			PS_Maths.CalculateVectorAngle(TrailVectors[j]))
#		outputfile.write(Outty)
		j += 1

	(X,Y) = im.size
        print " + Orig Image Size  = X:", X, " Y:", Y
        (X,Y) = FinalIMSize,FinalIMSize
        print " + New Image Size   = X:", X, " Y:", Y
        print " + Square Size      =", X/Factor, "x", X/Factor

	i += 1

#outputfile.close()

#Calculate the Square Coordinates
SquareNoLines  = []
SquareCoords    = []
SquareBigVector = []
SquareLineVectorAngles   = []
SquareLineVector         = []
SquareBigVectorAngle     = []
SquareBigVectorMagnitude = []
SquareBigVectorSpeed     = []
SqInROI = []

i = 0
cnt = 0
while i < Squares/Factor:
	j = 0
        while j< Squares/Factor:
	        SquareCoords.append([(X/Factor)*j,(X/Factor)*(i)])
                SquareNoLines.append ( 0 )
                SquareBigVector.append ( [0,0] )
                SquareLineVector.append( [cnt,0.0,0.0] )
                SquareLineVectorAngles.append( [cnt,0.0] )
                SquareBigVectorAngle.append ( 0.0 )
                SquareBigVectorMagnitude.append ( 0.0 )
                SquareBigVectorSpeed.append( [0.0,0] )
		SqInROI.append ( 0 )
                cnt += 1
                j += 1
	i += 1

print " + Processing ROI vs Squares ..."
SquareCoordsFull = []
InROI = 0
i = 0
while i < len(SquareCoords):

	if(options.Polygon):
		SquareCoordsFull.append([ [SquareCoords[i][0],SquareCoords[i][1]],\
					  [SquareCoords[i][0]+X/Factor,SquareCoords[i][1]],\
	        			  [SquareCoords[i][0],SquareCoords[i][1]+Y/Factor],\
					  [SquareCoords[i][0]+X/Factor,SquareCoords[i][1]+Y/Factor]])
		InROI = PS_Maths.SquareWithinROI(Polygon,SquareCoordsFull[-1])

		if InROI:
			SqInROI[i] = 1
	else:
		SqInROI[i] = 1
	i += 1


print " + Processing Trails against ROI then Squares ..."
#Divide up the trails by which square they contribute to
i   = 0
while i < len(TrailsAll):
	#print "Processing Trail ", i
        j = 0
	while j < len(SquareCoords):
		if( SqInROI[j] == 1):
	                Cross  = 0
	                Line   = []
			square = []
			square.append([SquareCoords[j][0],SquareCoords[j][1]])
			square.append([SquareCoords[j][0]+X/Factor,SquareCoords[j][1]])
			square.append([SquareCoords[j][0]+X/Factor,SquareCoords[j][1]+Y/Factor])
			square.append([SquareCoords[j][0],SquareCoords[j][1]+Y/Factor])
			square.append([SquareCoords[j][0],SquareCoords[j][1]])

			if(options.Polygon):
		                Cross2,Line2,Debug2 =  PS_Maths.LineWithinSquare( Polygon,\
		                                               [Trails[i][0],Trails[i][1],\
		                                               Trails[i][2],Trails[i][3]],0 )
				if(Cross2):
					#First correct for which direction in Y
					#if Line2[0][1] > Line2[1][1]:
					#	TrailVectors_ROI[i] = [Line2[1][0]-Line2[0][0],\
					#			       Line2[1][1]-Line2[0][1]]
					#else:
					#	TrailVectors_ROI[i] = [Line2[1][0]-Line2[0][0],\
					#			       Line2[0][1]-Line2[1][1]]

					TrailVectors_ROI[i] = [Line2[1][0]-Line2[0][0],\
							       Line2[1][1]-Line2[0][1]]
			else:
				Cross2 = 1
	
			if Cross2:
				#print "\t\tTrying Square", j
				Cross,Line,Debug = PS_Maths.LineWithinSquare( square,\
	       	                                      [TrailsAll[i][0],TrailsAll[i][1],\
       		                                       TrailsAll[i][2],TrailsAll[i][3]],1 )

	                if(Cross and Cross2):
				print "\t+ Trail ", i+1, "\tCrosses Square", j+1,\
				      "(Square Coords=", SquareCoords[j], ")"

	                	SquareLineVector[j] = [i,Line[1][0]-Line[0][0],\
	                                               Line[0][1]-Line[1][1]]
				SquareLineVectorAngles[j] = [i,PS_Maths.\
	                                                     CalculateVectorAngle(\
	                                                    [Line[1][0]-Line[0][0],\
	                                                     Line[0][1]-Line[1][1]] )]
	                        SquareBigVector[j][0]     = SquareBigVector[j][0]+\
	                                                    (Line[1][0]-Line[0][0])

                                SquareBigVectorSpeed[j][0] = SquareBigVectorSpeed[j][0] + ( TrailNoPoints[i]*float(options.TimeInterval) )
                                SquareBigVectorSpeed[j][1] = SquareBigVectorSpeed[j][1] + ( PS_Maths.CalculateVectorMagnitude(TrailVectors[i]) ) 


                                #
                                # Additions Here
                                #
                                #print "i=", i, " j=",j, "SquareBigVectorSpeed=[",SquareBigVectorSpeed[j][0],",",SquareBigVectorSpeed[j][1], "] Speed=", (SquareBigVectorSpeed[j][0] / SquareBigVectorSpeed[j][1])

				print "\t+ Trail ", i+1, "\tCrosses Square", j+1,\
                                      "(Square Coords=", SquareCoords[j], \
                                      ")[Cummulative Speed=", (SquareBigVectorSpeed[j][0] / SquareBigVectorSpeed[j][1]),"]"

				#Corrects for whether moving up or down on Y
				if Line[0][1] > Line[1][1]:
					SquareBigVector[j][1]     = SquareBigVector[j][1]+\
	       	                         	                    (Line[1][1]-Line[0][1])
				else:
					SquareBigVector[j][1]     = SquareBigVector[j][1]-\
	                                                            (Line[0][1]-Line[1][1])
	                        SquareNoLines[j] += 1
                j += 1
	i += 1

TrailVectors_ROI_Culled = []
TrailVectors_ROI_Culled_Mags = []
TrailVectors_ROI_Culled_Coords = []
TrailNoPoints_ROI_Culled = []
i = 0
while i < len(TrailVectors_ROI):

	if((TrailVectors_ROI[i][0] != 0.0) and (TrailVectors_ROI[i][1] != 0.0)):
		TrailVectors_ROI_Culled.append( TrailVectors_ROI[i] )
		TrailVectors_ROI_Culled_Mags.append(\
			PS_Maths.CalculateVectorMagnitude(TrailVectors_ROI[i]))
		TrailVectors_ROI_Culled_Coords.append( Trails[i]  )
		TrailNoPoints_ROI_Culled.append( TrailNoPoints[i]  )
	i += 1




if options.Polygon and len(TrailVectors_ROI_Culled_Mags) > 1:
	print " + Trail Length Stats:  Median=", \
		PS_Maths.getMedian(TrailVectors_ROI_Culled_Mags), \
		"Mean=", sum(TrailVectors_ROI_Culled_Mags) / len(TrailVectors_ROI_Culled_Mags)

i = 0
while i < len(SquareCoords):
	if( (SquareBigVector[i][0] == 0) and (SquareBigVector[i][1] == 0) ):
		print "  * BigVec #%4d"%i, "No BigVector here", \
                      SquareBigVector[i][0],\
                      SquareBigVector[i][1]
        else:
                SquareBigVectorAngle[i]     = PS_Maths.CalculateVectorAngle(\
                                              SquareBigVector[i])
                SquareBigVectorMagnitude[i] = PS_Maths.CalculateVectorMagnitude(\
                                              SquareBigVector[i])
                print "  * BigVec #%4d"%i, "SqCrds=[%3.0f"%SquareCoords[i][0]+\
                      ",%3.0f"%SquareCoords[i][1]+"]",\
                      "Vec = (%5.0f"%SquareBigVector[i][0]+\
                      ",%5.0f"%SquareBigVector[i][1]+")", \
                      "Ang=%6.2f"%SquareBigVectorAngle[i], \
                      "Lines=%3d"%SquareNoLines[i]
        i += 1

SquareBigVectorMagnitudeLongest = na.array(SquareBigVectorMagnitude).max()

(O_Dir,O_File) = os.path.split(options.ExcelFile)
(O_Name,O_Ext) = os.path.splitext(O_File)
#OutName = "DivisionFiles/"+O_Name+"_"+str(Squares)
OutName = BaseDir + O_Name+"_"+str(Squares)

#Draw binary original
BinaryOriginal = PS_Plots.PlotBinaryOriginal(options.ImageFile,OutName,AxisAngle,\
                                             FinalIMSize,options.FlipY,int(options.Orient))
print " + BinaryOriginal   =", os.path.basename(BinaryOriginal+".png")

#Draw the Trails Images
SVGTrailPlot_1 = PS_Plots.PlotSVGTrails_1(OutName,O_Name,Coords,Colours,\
                                          Axis,Factor,FinalIMSize,Polygon,options.ROIColour)
print " + SVGTrailPlot_1   =", os.path.basename(SVGTrailPlot_1+".svg")
convert = "inkscape --export-png="+SVGTrailPlot_1+\
          ".png --export-dpi="+DPI+" "+SVGTrailPlot_1+".svg 2>/dev/null"
os.popen(convert)
print " + SVGTrailPlot_1   =", os.path.basename(SVGTrailPlot_1+".png")

#New Trail image, coloured by angle ROI only

if options.Polygon:
	SVGTrailPlot_2 = PS_Plots.PlotSVGTrails_AngColour(OutName,O_Name,TrailVectors_ROI_Culled_Coords,\
							  AxisColours,Axis,Factor,FinalIMSize,\
							  Polygon,options.ROIColour)
	TrailSpeedPlot,AveSpd = PS_Plots.PlotTrailSpeeds(OutName,TrailVectors_ROI_Culled,\
                                                         TrailNoPoints_ROI_Culled,float(options.TimeInterval))	
else:
	SVGTrailPlot_2 = PS_Plots.PlotSVGTrails_AngColour(OutName,O_Name,Trails,AxisColours,\
                                                  Axis,Factor,FinalIMSize,Polygon,options.ROIColour)
	TrailSpeedPlot,AveSpd = PS_Plots.PlotTrailSpeeds(OutName,TrailVectors,\
                                                 	 TrailNoPoints,float(options.TimeInterval))


print " + SVGTrailPlot_2   =", os.path.basename(SVGTrailPlot_2+".svg")
convert = "inkscape --export-png="+SVGTrailPlot_2+\
          ".png --export-dpi="+DPI+" "+SVGTrailPlot_2+".svg 2>/dev/null"
os.popen(convert)
print " + SVGTrailPlot_2   =", os.path.basename(SVGTrailPlot_2+".png")

print " + TrailSpeeds Plot =", TrailSpeedPlot, "(.png & .svg)"
print " + Ave Trail Speed  =", AveSpd
print " + Time Interval    =", options.TimeInterval


#Draw the BASIC WindMap
SVGWindMapKey = PS_Plots.PlotWindMapKey(OutName,[100,100],AxisColours)
print " + SVGWindMapKey    =", os.path.basename(SVGWindMapKey+".svg")
convert = "inkscape --export-png="+SVGWindMapKey+\
          ".png --export-dpi="+DPI+" "+SVGWindMapKey+".svg 2>/dev/null"
print " + SVGWindMapKey    =", os.path.basename(SVGWindMapKey+".png")

SVGWindMap_1  = PS_Plots.PlotSVGWindMap_1(OutName,O_Name,X,Y,Factor,Polygon,\
                                          SquareCoords,\
                                          SquareBigVector,\
                                          SquareBigVectorAngle,\
                                          SquareBigVectorMagnitudeLongest,\
					  SquareBigVectorSpeedMin,SquareBigVectorSpeedMax,\
					  "num",SquareNoLines,FinalIMSize,\
					  AxisColours,options.SquareColours,\
					  SquareColoursSpeedRange,options.ShowArrows,\
					  options.ArrowColour,options.ShowGrid,\
					  options.ShowRectangles,options.ROIColour)
print " + SVGWindMap num   =", os.path.basename(SVGWindMap_1+".svg")
convert = "inkscape --export-png="+SVGWindMap_1+\
          ".png --export-dpi="+DPI+" "+SVGWindMap_1+".svg 2>/dev/null"
os.popen(convert)
print " + SVGGWindMap num   =", os.path.basename(SVGWindMap_1+".png")

SVGWindMap_2  = PS_Plots.PlotSVGWindMap_1(OutName,O_Name,X,Y,Factor,Polygon,\
                                          SquareCoords,\
                                          SquareBigVector,\
                                          SquareBigVectorAngle,\
                                          SquareBigVectorMagnitudeLongest,\
					  SquareBigVectorSpeed,SquareBigVectorSpeedMax,\
                                          "mag",SquareNoLines,FinalIMSize,
					  AxisColours,options.SquareColours,\
					  SquareColoursSpeedRange,options.ShowArrows,\
                                          options.ArrowColour,options.ShowGrid,\
                                          options.ShowRectangles,options.ROIColour)
print " + SVGWindMap mag   =", os.path.basename(SVGWindMap_2+".svg")
convert = "inkscape --export-png="+SVGWindMap_2+\
          ".png --export-dpi="+DPI+" "+SVGWindMap_2+".svg 2>/dev/null"
os.popen(convert)
print " + SVGGWindMap  mag =", os.path.basename(SVGWindMap_2+".png")


#Draw the Pie Charts
#RadialHistogram = PS_Plots.PlotRadialHistogram(OutName,TrailVectors,500,AxisColours)
#print " + RadialHistogram  =", RadialHistogram+".svg"
#convert = "inkscape --export-png="+RadialHistogram+\
#          ".png --export-dpi="+DPI+" "+RadialHistogram+".svg 2>/dev/null"
#os.popen(convert)
#print " + RadialHistogram  =", RadialHistogram+".png"


outputfile = open(OutName+"_TrailVectorsAll.txt",'w')
i = 0
while i < len(TrailVectorsAll):
	outputfile.write( str(TrailVectorsAll[i][0])+"\t"+str(TrailVectorsAll[i][1])+"\n" )
	i += 1
outputfile.close()



RoseDiagram      = PS_Plots.PlotRoseDiagram(OutName,"_rosediagram_15seg_wmag",\
					    TrailVectorsAll,1,15,500,\
					    AxisColours,options.ScaleRose,AxisLabels)
print " + RoseDiagram      =", os.path.basename(RoseDiagram+".svg")
convert = "inkscape --export-png="+RoseDiagram+\
          ".png --export-dpi="+DPI+" "+RoseDiagram+".svg 2>/dev/null"
os.popen(convert)
print " + RoseDiagram      =", os.path.basename(RoseDiagram+".png")



RoseDiagram2      = PS_Plots.PlotRoseDiagram(OutName,"_rosediagram_15seg_nomag",\
					     TrailVectorsAll,0,15,500,\
					     AxisColours,options.ScaleRose,AxisLabels)
print " + RoseDiagram2     =", os.path.basename(RoseDiagram2+".svg")
convert = "inkscape --export-png="+RoseDiagram2+\
          ".png --export-dpi="+DPI+" "+RoseDiagram2+".svg 2>/dev/null"
os.popen(convert)
print " + RoseDiagram2     =", os.path.basename(RoseDiagram2+".png")

RoseDiagram5      = PS_Plots.PlotRoseDiagram(OutName,"_rosediagram_180seg_nomag",\
                                             TrailVectorsAll,0,180,500,\
                                             AxisColours,options.ScaleRose,AxisLabels)
print " + RoseDiagram5     =", os.path.basename(RoseDiagram5+".svg")
convert = "inkscape --export-png="+RoseDiagram5+\
          ".png --export-dpi="+DPI+" "+RoseDiagram5+".svg 2>/dev/null"
os.popen(convert)
print " + RoseDiagram5     =", os.path.basename(RoseDiagram5+".png")

RoseDiagram5b     = PS_Plots.PlotRoseDiagram(OutName,"_rosediagram_180seg_wmag",\
                                             TrailVectorsAll,1,180,500,\
                                             AxisColours,options.ScaleRose,AxisLabels)
print " + RoseDiagram5b    =", os.path.basename(RoseDiagram5b+".svg")
convert = "inkscape --export-png="+RoseDiagram5b+\
          ".png --export-dpi="+DPI+" "+RoseDiagram5b+".svg 2>/dev/null"
os.popen(convert)
print " + RoseDiagram5b    =", os.path.basename(RoseDiagram5b+".png")

if options.Polygon and len(TrailVectors_ROI_Culled) > 0:
	outputfile = open(OutName+"_TrailVectors_ROI_Culled.txt",'w')
	i = 0
	while i < len(TrailVectors_ROI_Culled):
	        outputfile.write( str(TrailVectors_ROI_Culled[i][0])+"\t"+str(TrailVectors_ROI_Culled[i][1])+"\n" )
	        i += 1
	outputfile.close()

	RoseDiagram3a      = PS_Plots.PlotRoseDiagram(OutName,"_rosediagram_180seg_ROI_nomag",\
	                                             TrailVectors_ROI_Culled,0,180,500,\
						     AxisColours,options.ScaleRose,AxisLabels)
	print " + RoseDiagram3a    =", os.path.basename(RoseDiagram3a+".svg")
	convert = "inkscape --export-png="+RoseDiagram3a+\
	          ".png --export-dpi="+DPI+" "+RoseDiagram3a+".svg 2>/dev/null"
	os.popen(convert)
	print " + RoseDiagram3a    =", os.path.basename(RoseDiagram3a+".png")

	RoseDiagram4a      = PS_Plots.PlotRoseDiagram(OutName,"_rosediagram_15seg_ROI_nomag",\
	                                             TrailVectors_ROI_Culled,0,15,500,\
						     AxisColours,options.ScaleRose,AxisLabels)
	print " + RoseDiagram4a    =", os.path.basename(RoseDiagram4a+".svg")
	convert = "inkscape --export-png="+RoseDiagram4a+\
	          ".png --export-dpi="+DPI+" "+RoseDiagram4a+".svg 2>/dev/null"
	os.popen(convert)
	print " + RoseDiagram4a    =", os.path.basename(RoseDiagram4a+".png")

	RoseDiagram3b      = PS_Plots.PlotRoseDiagram(OutName,"_rosediagram_180seg_ROI_wmag",\
                                                     TrailVectors_ROI_Culled,1,180,500,\
                                                     AxisColours,options.ScaleRose,AxisLabels)
        print " + RoseDiagram3b    =", os.path.basename(RoseDiagram3b+".svg")
        convert = "inkscape --export-png="+RoseDiagram3b+\
                  ".png --export-dpi="+DPI+" "+RoseDiagram3b+".svg 2>/dev/null"
        os.popen(convert)
        print " + RoseDiagram3b    =", os.path.basename(RoseDiagram3b+".png")

        RoseDiagram4b      = PS_Plots.PlotRoseDiagram(OutName,"_rosediagram_15seg_ROI_wmag",\
                                                     TrailVectors_ROI_Culled,1,15,500,\
                                                     AxisColours,options.ScaleRose,AxisLabels)
        print " + RoseDiagram4b    =", os.path.basename(RoseDiagram4b+".svg")
        convert = "inkscape --export-png="+RoseDiagram4b+\
                  ".png --export-dpi="+DPI+" "+RoseDiagram4b+".svg 2>/dev/null"
        os.popen(convert)
        print " + RoseDiagram4b    =", os.path.basename(RoseDiagram4b+".png")


	TrailMags          = PS_Plots.PlotTrailMagnitudes(OutName,TrailVectors_ROI_Culled,float(options.PixStep),AxisLabels)
	print " + Trail Mag ROI     =", os.path.basename(OutName+"_trailmagnitudes.png")
	print " + Trail Mag ROI     =", os.path.basename(OutName+"_trailmagnitudes.svg")
	print " + Trail Mag ROI ang =", os.path.basename(OutName+"_trailmagnitudes_angles.png")
        print " + Trail Mag ROI ang =", os.path.basename(OutName+"_trailmagnitudes_angles.svg")



print " + Direction Table          ="
DirectionTable = PS_Plots.PlotDirectionTable(TrailVectorsAll)
print " + Circular Statistics      ="
PS_Maths.CalcRayleighTest(TrailVectorsAll)

if options.Polygon and len(TrailVectors_ROI_Culled) > 0:
	print " + ROI Direction Table      ="
	DirectionTableROI = PS_Plots.PlotDirectionTable(TrailVectors_ROI_Culled)
	print " + ROI Circular Statistics  ="
	PS_Maths.CalcRayleighTest(TrailVectors_ROI_Culled)

FileName = OutName

print
print "Finished", sys.argv[0]

if(options.OutputType == "html"):
        print "</PRE></TD><TD VALIGN=top>"

	print "<FONT FACE=sans,arial SIZE=1><B>Binary Original</B><BR>"
	print "<A HREF='"  + URL + str(FileName) +\
              "_original.png'  TARGET=_blank>" +\
              "<IMG SRC='" + URL + str(FileName) +\
              "_original.png'  WIDTH=175 BORDER=0></A><BR>"
	print "<A HREF='" + URL + str(FileName) +\
	      "_original.png' STYLE='TEXT-DECORATION: NONE' TARGET=_blank>[PNG]</A><P>"

	print "<FONT FACE=sans,arial SIZE=1><B>Trail Image</B><BR>"
        print "<A HREF='"  + URL + str(FileName) +\
	      "_trails.png'  TARGET=_blank>" +\
              "<IMG SRC='" + URL + str(FileName) +\
	      "_trails.png'  WIDTH=175 BORDER=0></A><BR>"
	print "<A HREF='" + URL + str(FileName) +\
              "_trails.png' STYLE='TEXT-DECORATION: NONE' TARGET=_blank>[PNG]</A>"
	print "<A HREF='" + URL + str(FileName) +\
              "_trails.svg' STYLE='TEXT-DECORATION: NONE' TARGET=_blank>[SVG]</A><P>"

	if options.Polygon:
		print "<FONT FACE=sans,arial SIZE=1><B>Trail Image (coloured by angle ROI onle)</B><BR>"
	        print "<A HREF='"  + URL + str(FileName) +\
	              "_trails_anglescoloured.png'  TARGET=_blank>" +\
	              "<IMG SRC='" + URL + str(FileName) +\
	              "_trails_anglescoloured.png'  WIDTH=175 BORDER=0></A><BR>"
	        print "<A HREF='" + URL + str(FileName) +\
	              "_trails_anglescoloured.png' STYLE='TEXT-DECORATION: NONE' TARGET=_blank>[PNG]</A>"
	        print "<A HREF='" + URL + str(FileName) +\
	              "_trails_anglescoloured.svg' STYLE='TEXT-DECORATION: NONE' TARGET=_blank>[SVG]</A><P>"	

	print "<FONT FACE=sans,arial SIZE=1><B>Windmap Image (opacity is number of trails)</B><BR>"
	print "<A HREF='"  + URL + str(FileName) +\
	      "_windmap_num.png' TARGET=_blank>" +\
              "<IMG SRC='" + URL + str(FileName) +\
	      "_windmap_num.png' WIDTH=175 BORDER=0></A><BR>" 
	print "<A HREF='" + URL + str(FileName) +\
              "_windmap_num.png' STYLE='TEXT-DECORATION: NONE' TARGET=_blank>[PNG]</A>"
        print "<A HREF='" + URL + str(FileName) +\
              "_windmap_num.svg' STYLE='TEXT-DECORATION: NONE' TARGET=_blank>[SVG]</A><P>"

        print "<FONT FACE=sans,arial SIZE=1><B>Windmap Image (opacity is magnitude of trails)</B><BR>"
        print "<A HREF='"  + URL + str(FileName) +\
              "_windmap_mag.png' TARGET=_blank>" +\
              "<IMG SRC='" + URL + str(FileName) +\
              "_windmap_mag.png' WIDTH=175 BORDER=0></A><BR>"
        print "<A HREF='" + URL + str(FileName) +\
              "_windmap_mag.png' STYLE='TEXT-DECORATION: NONE' TARGET=_blank>[PNG]</A>"
        print "<A HREF='" + URL + str(FileName) +\
              "_windmap_mag.svg' STYLE='TEXT-DECORATION: NONE' TARGET=_blank>[SVG]</A><P>"

	print "<FONT FACE=sans,arial SIZE=1><B>Rose Diagrams</B><BR>"

	print "<FONT FACE=sans,arial SIZE=1><B>15 degree segments with magnitude</B><BR>"
        print "<A HREF='"  + URL + str(FileName) +\
              "_rosediagram_15seg_wmag.png' TARGET=_blank>" +\
              "<IMG SRC='" + URL + str(FileName) +\
              "_rosediagram_15seg_wmag.png' WIDTH=175 BORDER=0></A><BR>" 
        print "<A HREF='" + URL + str(FileName) +\
              "_rosediagram_15seg_wmag.png' STYLE='TEXT-DECORATION: NONE' TARGET=_blank>[PNG]</A>"
        print "<A HREF='" + URL + str(FileName) +\
              "_rosediagram_15seg_wmag.svg' STYLE='TEXT-DECORATION: NONE' TARGET=_blank>[SVG]</A><P>"

	print "<FONT FACE=sans,arial SIZE=1><B>15 degree segments without magnitude</B><BR>"
	print "<A HREF='"  + URL + str(FileName) +\
              "_rosediagram_15seg_nomag.png' TARGET=_blank>" +\
              "<IMG SRC='" + URL + str(FileName) +\
              "_rosediagram_15seg_nomag.png' WIDTH=175 BORDER=0></A><BR>"
        print "<A HREF='" + URL + str(FileName) +\
              "_rosediagram_15seg_nomag.png' STYLE='TEXT-DECORATION: NONE' TARGET=_blank>[PNG]</A>"
        print "<A HREF='" + URL + str(FileName) +\
              "_rosediagram_15seg_nomag.svg' STYLE='TEXT-DECORATION: NONE' TARGET=_blank>[SVG]</A><P>"

	print "<FONT FACE=sans,arial SIZE=1><B>180 degree segments with magnitude</B><BR>"
	print "<A HREF='"  + URL + str(FileName) +\
              "_rosediagram_180seg_wmag.png' TARGET=_blank>" +\
              "<IMG SRC='" + URL + str(FileName) +\
              "_rosediagram_180seg_wmag.png' WIDTH=175 BORDER=0></A><BR>"
        print "<A HREF='" + URL + str(FileName) +\
              "_rosediagram_180seg_wmag.png' STYLE='TEXT-DECORATION: NONE' TARGET=_blank>[PNG]</A>"
        print "<A HREF='" + URL + str(FileName) +\
              "_rosediagram_180seg_wmag.svg' STYLE='TEXT-DECORATION: NONE' TARGET=_blank>[SVG]</A><P>"

	print "<FONT FACE=sans,arial SIZE=1><B>180 degree segments without magnitude</B><BR>"
        print "<A HREF='"  + URL + str(FileName) +\
              "_rosediagram_180seg_nomag.png' TARGET=_blank>" +\
              "<IMG SRC='" + URL + str(FileName) +\
              "_rosediagram_180seg_nomag.png' WIDTH=175 BORDER=0></A><BR>"
        print "<A HREF='" + URL + str(FileName) +\
              "_rosediagram_180seg_nomag.png' STYLE='TEXT-DECORATION: NONE' TARGET=_blank>[PNG]</A>"
        print "<A HREF='" + URL + str(FileName) +\
              "_rosediagram_180seg_nomag.svg' STYLE='TEXT-DECORATION: NONE' TARGET=_blank>[SVG]</A><P>"

	if(options.Polygon):
		print "<FONT FACE=sans,arial SIZE=1><B>ROI 15 degree segments without magnitude</B><BR>"
		print "<A HREF='"  + URL + str(FileName) +\
	              "_rosediagram_15seg_ROI_nomag.png' TARGET=_blank>" +\
	              "<IMG SRC='" + URL + str(FileName) +\
	              "_rosediagram_15seg_ROI_nomag.png' WIDTH=175 BORDER=0></A><BR>"
	        print "<A HREF='" + URL + str(FileName) +\
	              "_rosediagram_15seg_ROI_nomag.png' STYLE='TEXT-DECORATION: NONE' TARGET=_blank>[PNG]</A>"
	        print "<A HREF='" + URL + str(FileName) +\
	              "_rosediagram_15seg_ROI_nomag.svg' STYLE='TEXT-DECORATION: NONE' TARGET=_blank>[SVG]</A><P>"
                
		print "<FONT FACE=sans,arial SIZE=1><B>ROI 15 degree segments with magnitude</B><BR>"
                print "<A HREF='"  + URL + str(FileName) +\
                      "_rosediagram_15seg_ROI_wmag.png' TARGET=_blank>" +\
                      "<IMG SRC='" + URL + str(FileName) +\
                      "_rosediagram_15seg_ROI_wmag.png' WIDTH=175 BORDER=0></A><BR>"
                print "<A HREF='" + URL + str(FileName) +\
                      "_rosediagram_15seg_ROI_wmag.png' STYLE='TEXT-DECORATION: NONE' TARGET=_blank>[PNG]</A>"
                print "<A HREF='" + URL + str(FileName) +\
                      "_rosediagram_15seg_ROI_wmag.svg' STYLE='TEXT-DECORATION: NONE' TARGET=_blank>[SVG]</A><P>"

		print "<FONT FACE=sans,arial SIZE=1><B>ROI 180 degree segments without magnitude</B><BR>"
	        print "<A HREF='"  + URL + str(FileName) +\
	              "_rosediagram_180seg_ROI_nomag.png' TARGET=_blank>" +\
	              "<IMG SRC='" + URL + str(FileName) +\
	              "_rosediagram_180seg_ROI_nomag.png' WIDTH=175 BORDER=0></A><BR>"
	        print "<A HREF='" + URL + str(FileName) +\
	              "_rosediagram_180seg_ROI_nomag.png' STYLE='TEXT-DECORATION: NONE' TARGET=_blank>[PNG]</A>"
	        print "<A HREF='" + URL + str(FileName) +\
	              "_rosediagram_180seg_ROI_nomag.svg' STYLE='TEXT-DECORATION: NONE' TARGET=_blank>[SVG]</A><P>"

		print "<FONT FACE=sans,arial SIZE=1><B>ROI 180 degree segments with magnitude</B><BR>"
		print "<A HREF='"  + URL + str(FileName) +\
                      "_rosediagram_180seg_ROI_wmag.png' TARGET=_blank>" +\
                      "<IMG SRC='" + URL + str(FileName) +\
                      "_rosediagram_180seg_ROI_wmag.png' WIDTH=175 BORDER=0></A><BR>"
                print "<A HREF='" + URL + str(FileName) +\
                      "_rosediagram_180seg_ROI_wmag.png' STYLE='TEXT-DECORATION: NONE' TARGET=_blank>[PNG]</A>"
                print "<A HREF='" + URL + str(FileName) +\
                      "_rosediagram_180seg_ROI_wmag.svg' STYLE='TEXT-DECORATION: NONE' TARGET=_blank>[SVG]</A><P>"

		print "<FONT FACE=sans,arial SIZE=1><B>ROI Frequency Plot of trail lengths (Angle range 0-360)</B><BR>"
                print "<A HREF='"  + URL + str(FileName) +\
                      "_trailmagnitudes_angleset_0-360.png' TARGET=_blank>" +\
                      "<IMG SRC='" + URL + str(FileName) +\
                      "_trailmagnitudes_angleset_0-360.png' WIDTH=175 BORDER=0></A><BR>"
                print "<A HREF='" + URL + str(FileName) +\
                      "_trailmagnitudes_angleset_0-360.png' STYLE='TEXT-DECORATION: NONE' TARGET=_blank>[PNG]</A>"
                print "<A HREF='" + URL + str(FileName) +\
                      "_trailmagnitudes_angleset_0-360.svg' STYLE='TEXT-DECORATION: NONE' TARGET=_blank>[SVG]</A><P>"

		print "<FONT FACE=sans,arial SIZE=1><B>ROI Frequency Plot of trail lengths (Angle range 315-45)</B><BR>"
                print "<A HREF='"  + URL + str(FileName) +\
                      "_trailmagnitudes_angleset_315-45.png' TARGET=_blank>" +\
                      "<IMG SRC='" + URL + str(FileName) +\
                      "_trailmagnitudes_angleset_315-45.png' WIDTH=175 BORDER=0></A><BR>"
                print "<A HREF='" + URL + str(FileName) +\
                      "_trailmagnitudes_angleset_315-45.png' STYLE='TEXT-DECORATION: NONE' TARGET=_blank>[PNG]</A>"
                print "<A HREF='" + URL + str(FileName) +\
                      "_trailmagnitudes_angleset_315-45.svg' STYLE='TEXT-DECORATION: NONE' TARGET=_blank>[SVG]</A><P>"

		print "<FONT FACE=sans,arial SIZE=1><B>ROI Frequency Plot of trail lengths (Angle range 45-135)</B><BR>"
                print "<A HREF='"  + URL + str(FileName) +\
                      "_trailmagnitudes_angleset_45-135.png' TARGET=_blank>" +\
                      "<IMG SRC='" + URL + str(FileName) +\
                      "_trailmagnitudes_angleset_45-135.png' WIDTH=175 BORDER=0></A><BR>"
                print "<A HREF='" + URL + str(FileName) +\
                      "_trailmagnitudes_angleset_45-135.png' STYLE='TEXT-DECORATION: NONE' TARGET=_blank>[PNG]</A>"
                print "<A HREF='" + URL + str(FileName) +\
                      "_trailmagnitudes_angleset_45-135.svg' STYLE='TEXT-DECORATION: NONE' TARGET=_blank>[SVG]</A><P>"

		print "<FONT FACE=sans,arial SIZE=1><B>ROI Frequency Plot of trail lengths (Angle range 135-225)</B><BR>"
                print "<A HREF='"  + URL + str(FileName) +\
                      "_trailmagnitudes_angleset_135-225.png' TARGET=_blank>" +\
                      "<IMG SRC='" + URL + str(FileName) +\
                      "_trailmagnitudes_angleset_135-225.png' WIDTH=175 BORDER=0></A><BR>"
                print "<A HREF='" + URL + str(FileName) +\
                      "_trailmagnitudes_angleset_135-225.png' STYLE='TEXT-DECORATION: NONE' TARGET=_blank>[PNG]</A>"
                print "<A HREF='" + URL + str(FileName) +\
                      "_trailmagnitudes_angleset_135-225.svg' STYLE='TEXT-DECORATION: NONE' TARGET=_blank>[SVG]</A><P>"

		print "<FONT FACE=sans,arial SIZE=1><B>ROI Frequency Plot of trail lengths (Angle range 225-315)</B><BR>"
                print "<A HREF='"  + URL + str(FileName) +\
                      "_trailmagnitudes_angleset_225-315.png' TARGET=_blank>" +\
                      "<IMG SRC='" + URL + str(FileName) +\
                      "_trailmagnitudes_angleset_225-315.png' WIDTH=175 BORDER=0></A><BR>"
                print "<A HREF='" + URL + str(FileName) +\
                      "_trailmagnitudes_angleset_225-315.png' STYLE='TEXT-DECORATION: NONE' TARGET=_blank>[PNG]</A>"
                print "<A HREF='" + URL + str(FileName) +\
                      "_trailmagnitudes_angleset_225-315.svg' STYLE='TEXT-DECORATION: NONE' TARGET=_blank>[SVG]</A><P>"
     

        print "</TABLE>\n\n"


	print "</BODY></HTML>"


#------------------------------------------------------------------------------
# FIN
#------------------------------------------------------------------------------
