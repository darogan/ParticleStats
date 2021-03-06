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
#                Centre For Trophoblast Research                              #
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

import ParticleStats_Maths as PS_Maths
import math
import numpy as na
import os,sys
from PIL import Image, ImageDraw, ImageColor
import glob
import re
#from datetime import datetime
#from dateutil import parser

#------------------------------------------------------------------------------
def Colourer (Word, Colour, Mode, Weight,Size):

	W_S = ""
	W_E = ""

	if(Weight == "bold"):
		W_S = "<B>"
		W_E = "</B>"
	elif(Weight == "italics"):
		W_S = "<I>"
                W_E = "</I>"

	if(Mode == "html"):
		ColouredWord = W_S + "<FONT COLOR=" + Colour + " SIZE=" + \
                               str(Size) + ">" + Word + "</FONT>" + W_E

	else:
		ColouredWord = Word

	return ColouredWord

#------------------------------------------------------------------------------
def ReadSettingsFile (FileName):

	try:
                F_Settings = open(FileName,'r')
        except:
                print "\nError->\tFile: %s does not exist\n" % FileName
		sys.exit()

        LineCount = len( open(FileName,'r').readlines() )
        Settings = na.zeros((LineCount), na.Float)
        num=0
        for line in F_Settings:
                line = line.rstrip('\n')
                element = line.split(': ')
#                XX[num][0] = int(element[0])
                Settings[num] = float(element[1])
                num = num + 1
        F_Settings.close()


	return Settings

#------------------------------------------------------------------------------
def DrawExcelCoords (FileNames,Coords,Stem,Colours):

        NewImageStack = [];
        i = 0
        while i < len(FileNames):
                im = Image.open(FileNames[i]).convert("RGB")
                draw = ImageDraw.Draw(im)
                del draw
                OutName = (Stem + "_" + str("%03d" % i) + ".tiff")
                NewImageStack.append(OutName)
                im.save(OutName,"TIFF")
                i += 1

        i = 1
        while i < len(Coords):
                print "\tDrawing Particle for Block", i,
                print "( No Coords =", len(Coords[i]), ")",
                print "( Colour =", Colours[i], ")"
                TmpCoords = Coords[i]
                x = len(TmpCoords)
                j = TmpCoords[0][0]
                y = 1
                while j < len(NewImageStack):
                        im = Image.open(NewImageStack[j])
                        draw = ImageDraw.Draw(im)

                        k = 0
                        while k < y:
                                draw.point( ( (TmpCoords[k][2]/0.22),\
                                             (TmpCoords[k][3]/0.22)),\
                                             fill=Colours[i] )
                                k += 1

                        im.save(NewImageStack[j],"TIFF")

                        j += 1
                        if y < x: y += 1
                i += 1

#------------------------------------------------------------------------------
def DrawTrailsOnImageFile(FileName,ParticleNo,CoordsSet,Colour,Coords,Scale,
                          Regression,DirGraphs,errorLimit):

	im = Image.new('RGBA',(1200, 800))
	print "Scale=", Scale
	Scale = float(Scale)

	draw = ImageDraw.Draw(im)

	modulo = ((ParticleNo+1)%6)
	if(modulo == 0): modulo = 6

	x = 17.5 + (modulo * 85) + (modulo*2)
	y = 50

	if(ParticleNo < 6):                       y += 45  + 6
	if(ParticleNo >= 6  and ParticleNo < 12): y += 125 + 8
	if(ParticleNo >= 12 and ParticleNo < 18): y += 215 + 4
	if(ParticleNo >= 18):                     y += 300 + 4

	radius = (70/2)/Scale
	print "ParticleNo=", ParticleNo, "x=", x, "y=", y,"radius", radius

	XCoords = []
	YCoords = []
	points  = []
	i = 0
	while i < len(Coords):
		XCoords.append( Coords[i][4]/Scale )
		YCoords.append( Coords[i][5]/Scale )
		points.append( [Coords[i][4]/Scale, Coords[i][5]/Scale] )

		i += 1

	x_mean,x_geomean = PS_Maths.geo_mean( XCoords )
	y_mean, y_geomean = PS_Maths.geo_mean( YCoords )

	print "x_mean    | y_mean       = %6.2f | %6.2f" % (x_mean,    y_mean)
	print "x_geomean | y_geomean    = %6.2f | %6.2f" % (x_geomean, y_geomean)

	convexhullPolygon   = PS_Maths.ConvexHull_Points(points)
	convexhullPerimeter = PS_Maths.Polygon_Perimeter(convexhullPolygon)
	convexhullArea      = PS_Maths.Polygon_Area(convexhullPolygon)
	convexhullRoundness = PS_Maths.Polygon_Roundness(convexhullArea, convexhullPerimeter)

	idealPerimeter = 2 * math.pi * radius
	idealArea      = math.pi * radius**2

	errorPerimeter = 1 - ( convexhullPerimeter / idealPerimeter )
	errorArea      = 1 - ( convexhullArea      / idealArea      )
	errorRoundness = 1 - convexhullRoundness

	smallestEnclosingCircle = PS_Maths.make_circle(points)


	print "smallestEnclosingCircle  = (%6.2f, %6.2f, %6.2f)" % \
          (smallestEnclosingCircle[0],smallestEnclosingCircle[1],smallestEnclosingCircle[2])
	errorRadius = math.fabs( 1 - ( smallestEnclosingCircle[2] / radius) )
	print "Circle Radius            = %8.2f [error=%6.2f]" % (smallestEnclosingCircle[2], errorRadius)
	print "ConvexHull Polygon (len) = %8.2f"               % len(convexhullPolygon)
	print "ConvexHull Perimeter     = %8.2f [error=%6.2f]" % ( convexhullPerimeter, errorPerimeter )
	print "ConvexHull Area          = %8.2f [error=%6.2f]" % ( convexhullArea, errorArea )
	print "ConvexHull Roundness     = %8.2f [error=%6.2f]" % ( convexhullRoundness, errorRoundness )

	if( (errorPerimeter > errorLimit) or (errorArea > errorLimit) or (errorRoundness > errorLimit) ):
		print "QC_FAIL: ", DirGraphs, " ", ParticleNo+1, " [Pe=%4.2f Ar=%4.2f Ro=%4.2f]"%(errorPerimeter,errorArea,errorRoundness)

	print "centroid %s %d %.2f %.2f %.2f %.2f %.2f %.2f %.2f"%(
           DirGraphs, ParticleNo+1,
           x_mean, y_mean, x_geomean, y_geomean,
           smallestEnclosingCircle[0], smallestEnclosingCircle[1], smallestEnclosingCircle[2])

	# Actual smallest circle
	draw.ellipse((smallestEnclosingCircle[0]-smallestEnclosingCircle[2],
                  smallestEnclosingCircle[1]-smallestEnclosingCircle[2],
                  smallestEnclosingCircle[0]+smallestEnclosingCircle[2],
                  smallestEnclosingCircle[1]+smallestEnclosingCircle[2]),
                  fill=None, outline ='purple')

    # Idealised Circle
	draw.ellipse((smallestEnclosingCircle[0]-radius,
				  smallestEnclosingCircle[1]-radius,
                  smallestEnclosingCircle[0]+radius,
				  smallestEnclosingCircle[1]+radius),
                  fill=None, outline ='blue')

	polyFlat = list(na.array(convexhullPolygon).flat)

	draw.polygon(polyFlat, fill=None, outline ='red')

	i = 0
	while i < len(Coords):
		draw.point( (Coords[i][4]/Scale, Coords[i][5]/Scale),fill=Colour )
		#	print ',' . join([ str(Coords[i][1]), str(Coords[i][2]), str(Coords[i][4]), str(Coords[i][5]) ])
		i += 1

	draw.text( (smallestEnclosingCircle[0],smallestEnclosingCircle[1]), "r="+str( "%.3f" % convexhullRoundness ), fill='black')

#	draw.text( (5,0), "Original Image  = "+os.path.basename(FileName), fill='red')
#	draw.text( (5,10),"Coordinates Set = "+str(CoordsSet), fill='red')
#	draw.text( (5,20),"Particle No     = "+str(ParticleNo), fill='red')
#	draw.text( (5,30),"No Coordinates  = "+str(len(Coords)), fill='red')

	del draw
	OutName = DirGraphs+"/trail_" + "Coords1" + "_" + str(1+ParticleNo) + ".png"
	im.save(OutName,'PNG')
	#im.save(OutName,**png_info)
	#OutName = DirGraphs+"/trail_" + "Coords1" + "_" + str(ParticleNo) + ".svg"
	#im.save(OutName,"SVG")

	return OutName

#------------------------------------------------------------------------------
def DrawCoords (FileNames,Coords,Stem,Colours):

	Scale = 1 #ie no scale - could be 0.22...

	NewImageStack = [];
	i = 0
        while i < len(FileNames):
		im = Image.open(FileNames[i]).convert("RGB")
		draw = ImageDraw.Draw(im)
		del draw
                OutName = (Stem + "_" + str("%03d" % i) + ".tiff")
		NewImageStack.append(OutName)
                im.save(OutName,"TIFF")		
                i += 1

	i = 0
	while i < len(Coords):

		print "\tDrawing Particle for Block", i, 
		print "( No Coords =", len(Coords[i]), ")",
		print "( Colour =", Colours[i], ")"
		TmpCoords = Coords[i]
		x = len(TmpCoords)
		j = int(TmpCoords[0][0])
		y = 1
		while j < len(NewImageStack):
			im = Image.open(NewImageStack[j])
			draw = ImageDraw.Draw(im)

			k = 0 
			while k < y: 
				draw.point( ( (TmpCoords[k][2]/Scale),\
                                             (TmpCoords[k][3]/Scale)),\
                                             fill=Colours[i] )
				k += 1

			im.save(NewImageStack[j],"TIFF")

			j += 1
			if y < x: y += 1
		i += 1

#------------------------------------------------------------------------------
def ReadCoordinatesFiles (pattern):

	pattern += "*"
        C_Files = []
        for infile in glob.glob(pattern):
                C_Files.append(infile)
        return C_Files

#------------------------------------------------------------------------------
def ReadImageFiles (pattern):

	pattern += "*.tif"
	ims = [] 
	for infile in glob.glob(pattern):
		ims.append(infile)
	return ims

#------------------------------------------------------------------------------
def FindImageFiles(pattern,path):

        MatchingFiles = []

        PatternX = re.compile(r'(?i)\A'+pattern+'.*.tif\Z')
        for root, dirs, files in os.walk(path):
                for file in files:
                        if( PatternX.search( file ) ):
                                MatchingFiles.append(root+"/"+file)

        return MatchingFiles

#------------------------------------------------------------------------------
def ReadCoords (FileStem):

	CoordFiles  = ReadCoordinatesFiles(FileStem)
	XX          = 0;
	CoordMatrix = []

	for FileName in CoordFiles:
		print "Reading:", FileName

		try:
		        F_Coords = open(FileName,'r')
		except:
			print "\nError->\tFile: %s does not exist\n" % FileName 
			sys.exit()

		LineCount = len( open(FileName,'r').readlines() )
		XX = na.zeros((LineCount,4), na.Float64)
		num=0
		for line in F_Coords:
			line = line.rstrip('\n')
      		        element = line.split('\t')
			XX[num][0] = float(element[0])
			XX[num][1] = float(element[1])
			XX[num][2] = float(element[2]) 
			XX[num][3] = float(element[3])
			num += 1
		CoordMatrix.append(XX)
		F_Coords.close()

	return CoordMatrix

#------------------------------------------------------------------------------
def ReadExcelKymographs (FileName):

        import xlrd
        import re

        try:
                F_Coords = open(FileName,'r')
        except:
                print "\nError->\tFile: %s does not exist\n" % FileName
                sys.exit()

        book  = xlrd.open_workbook(FileName)
        #print " + Number of worksheets =", book.nsheets
        #print "\tSheets are called:", book.sheet_names()

	booknames = []
	i = 0
	for booksheet in book.sheet_names():
		#print "\tSheet %3d" % i, "=", booksheet
		booknames.append(booksheet)
		i += 1

	PatternIN = re.compile(r'\AImage Name\Z')
	PatternIW = re.compile(r'\AImage Width\Z')
	PatternPS = re.compile(r'\APixel Size\Z')	
	PatternT = re.compile(r'\At\Z')
	PatternD = re.compile(r'\Adistance\Z')
	PatternI = re.compile(r'\Aintensity\Z')

	ColumnIN = []
	ColumnIW = []
	ColumnPS = []
	ColT = []
	ColD = []
	ColI = []
	ColTV = []

	for ii in range(book.nsheets):
                sheet = book.sheet_by_index(ii)

		if( PatternIN.search(str(sheet.cell_value(rowx=0, colx=0)) ) ):
			ColumnIN.append(sheet.cell_value(rowx=0, colx=1))
		else: 
			print "\nError->\tEmpty 'Image Name' ( Excel Col 0, Row 0)\n"
                        sys.exit()
                if( PatternIW.search(str(sheet.cell_value(rowx=1, colx=0)) ) ):
			ColumnIW.append(sheet.cell_value(rowx=1, colx=1))
		else:
                        print "\nError->\tEmpty 'Image Width' ( Excel Col 0, Row 1)\n"
                        sys.exit()
                if( PatternPS.search(str(sheet.cell_value(rowx=2, colx=0)) ) ):
			ColumnPS.append(sheet.cell_value(rowx=2, colx=1))
		else:
                        print "\nError->\tEmpty 'Pixel Size' ( Excel Col 0, Row 2)\n"
                        sys.exit()
		
		ColumnT  = []
		ColumnD  = []
        	ColumnI  = []
		ColumnTV = []

		for xx in range(sheet.ncols):
                	if( PatternT.search(str(sheet.cell_value(rowx=3, colx=xx)) ) ):
                        	ColumnT.append(xx)
				ColumnTV.append(sheet.cell_value(rowx=3, colx=(xx+1)))
                        if( PatternD.search(str(sheet.cell_value(rowx=4, colx=xx)) ) ):
                                ColumnD.append(xx)
                        if( PatternI.search(str(sheet.cell_value(rowx=4, colx=xx)) ) ):
                                ColumnI.append(xx)

		ColT.append( ColumnT )
		ColD.append( ColumnD )
		ColI.append( ColumnI )
		ColTV.append( ColumnTV )

	BigData = []	
	for ii in range(book.nsheets):
                sheet = book.sheet_by_index(ii)

		#print " + Sheet %3d             ="%ii , booknames[ii]
		#print "\t+ Image Name     =", ColumnIN[ii]
		#print "\t+ Image Width    =", ColumnIW[ii]
		#print "\t+ Pixel Size     =", ColumnPS[ii]
		#print "\t+ Number of Rows =", sheet.nrows

		Data = na.zeros([len(ColT[ii]),(sheet.nrows-5),2],na.Float64)

		row = 0
		for rx in range(sheet.nrows):
			if( rx > 4 ):
				tp = 0
				while tp < len(ColD[ii]):
					#print ii, "\ttp", ColTV[ii][tp], tp, rx, \
					#	sheet.cell_value(rowx=rx, colx=ColD[ii][tp]), \
					#	sheet.cell_value(rowx=rx, colx=ColI[ii][tp])
					if( sheet.cell_value(rowx=rx,colx=ColD[ii][tp]) == ""):
						Data[tp][row][0] = 0.0
					else:
						Data[tp][row][0] = float(sheet.cell_value(rowx=rx,\
									colx=ColD[ii][tp]))
					if( sheet.cell_value(rowx=rx,colx=ColD[ii][tp]) == ""):
                                                Data[tp][row][1] = 0.0
                                        else:
						Data[tp][row][1] = float(sheet.cell_value(rowx=rx,\
									colx=ColI[ii][tp]))
					tp += 1
				row += 1

		BigData.append( [ booknames[ii],ColumnIN[ii],ColumnIW[ii],\
				  ColumnPS[ii],ColTV[ii],Data ] )	


	return BigData

#------------------------------------------------------------------------------
def ReadExcelKymographs2 (FileName):

        import xlrd
        import re

        try:
                F_Coords = open(FileName,'r')
        except:
                print "\nError->\tFile: %s does not exist\n" % FileName
                sys.exit()

        book      = xlrd.open_workbook(FileName)
        booknames = []
        i = 0
        for booksheet in book.sheet_names():
                booknames.append(booksheet)
                i += 1

        PatternIN = re.compile(r'\AImage Name\Z')
	PatternTI = re.compile(r'\ATime Interval\Z')
        PatternPS = re.compile(r'\APixel Size\Z')

	BigData = []
	for ii in range(book.nsheets):
                sheet = book.sheet_by_index(ii)
		
		TmpCoords = []
		ColumnIN  = 999
		ColumnTI  = 999 
		ColumnPS  = 999

		for xx in range(sheet.ncols):
                	if( PatternIN.search(sheet.cell_value(rowx=0, colx=xx) ) ):
                        	ColumnIN = xx
                        if( PatternTI.search(sheet.cell_value(rowx=0, colx=xx) ) ):
                                ColumnTI = xx
                        if( PatternPS.search(sheet.cell_value(rowx=0, colx=xx) ) ):
                                ColumnPS = xx

		if ColumnIN == 999:
			print "\nError->\tEmpty 'Image Name' ( Excel Row 0)\n"
                        sys.exit()
		if ColumnTI == 999:
                        print "\nError->\tEmpty 'Time Interval' ( Excel Row 0)\n"
                        sys.exit()
		if ColumnPS == 999:
                        print "\nError->\tEmpty 'Pixel Size' ( Excel Row 0)\n"
                        sys.exit()

		for rx in range(sheet.nrows):
			if( (rx != 0) and (sheet.cell_value(rowx=rx, colx=0) != "") ):

				TmpCoords.append([ str(sheet.cell_value(rowx=rx, colx=ColumnIN)),\
						   int(sheet.cell_value(rowx=rx, colx=ColumnTI)),\
						   float(sheet.cell_value(rowx=rx, colx=ColumnPS)) ])

		BigData.append( [booknames[ii],TmpCoords] )

        return BigData

#------------------------------------------------------------------------------
def ReadExcelCoords (FileName,PR,PixelRatioMethod,TimeStart,TimeEnd,FlipY):

	import xlrd
	import re

	try:
		F_Coords = open(FileName,'r')
	except:
		print "\nError->\tFile: %s does not exist\n" % FileName
		sys.exit()

	book  = xlrd.open_workbook(FileName)
	#print "The number of worksheets in,", FileName, "is", book.nsheets
    #print "Sheets are called:", book.sheet_names()

	PatternCorrectionSheet = re.compile(r'correction')
	PatternAxisSheet       = re.compile(r'axis')
	PatternS               = re.compile(r'\AStack\Z')
	PatternX               = re.compile(r'\AX\Z')
	PatternY               = re.compile(r'\AY\Z')
	PatternZ               = re.compile(r'\AZ\Z')
	PatternT               = re.compile(r'\ATrack #\Z')
	PatternO               = re.compile(r'\AObject #\Z')
	PatternF               = re.compile(r'\AFrame #\Z')
	PatternIN              = re.compile(r'\AImage Name\Z')
	PatternIP              = re.compile(r'\AImage Plane\Z')
	PatternTI              = re.compile(r'\ATime Interval\Z')
	PatternX1              = re.compile(r'\AX1\Z')
	PatternY1              = re.compile(r'\AY1\Z')
	PatternX2              = re.compile(r'\AX2\Z')
	PatternY2              = re.compile(r'\AY2\Z')

	ColumnX  = 99;  ColumnY  = 99;  ColumnZ  = 99;
	ColumnT  = 99;  ColumnO  = 99;  ColumnIN = 99;
	ColumnIP = 99;  ColumnTI = 99;  ColumnX1 = 99;  
	ColumnY1 = 99;  ColumnX2 = 99;  ColumnY2 = 99;

	Coords      = []
	Corrections = []
	Cooords     = []
	Axes	    = []

	for ii in range(book.nsheets):
		sheet = book.sheet_by_index(ii)

		if sheet.nrows == 0:
			print "\nError->\tEmpty 'Sheet'", sheet.name, ii, "\n"
                        break

		if( PatternCorrectionSheet.search(sheet.name) ):
			for xx in range(sheet.ncols):
				if( PatternIN.search(sheet.cell_value(rowx=0, colx=xx) ) ):
                                        ColumnIN = xx
				if( PatternS.search(sheet.cell_value(rowx=0, colx=xx) ) ):
                                        ColumnS  = xx
                                if( PatternX.search(sheet.cell_value(rowx=0, colx=xx) ) ):
                                        ColumnX  = xx
                                if( PatternY.search(sheet.cell_value(rowx=0, colx=xx) ) ):
                                        ColumnY  = xx
					
			TmpCorrs      = []
			ObjCorrs      = str(sheet.cell_value(rowx=1, colx=ColumnIN))
			ObjLink2Excel = 99999
			
			for rx in range(sheet.nrows):
                                if( (rx != 0) and (sheet.cell_value(rowx=rx, colx=0) != "") ):
					if(ObjLink2Excel == 99999):
                                		ObjLink2Excel = rx+1
					if( str(sheet.cell_value(rowx=rx, colx=ColumnIN)) == ""):
                                                print "\nError->\tEmpty 'Image Name' ( Excel Row %d"%rx,")\n"
                                                sys.exit()
					if( str(sheet.cell_value(rowx=rx, colx=ColumnS)) == ""):
                                                print "\nError->\tEmpty 'Stack' ( Excel Row %d"%rx,")\n"
                                                sys.exit()
					if( str(sheet.cell_value(rowx=rx, colx=ColumnX)) == ""):
                                                print "\nError->\tEmpty 'X' ( Excel Row %d"%rx,")\n"
                                                sys.exit()
                                        if( str(sheet.cell_value(rowx=rx, colx=ColumnY)) == ""):
                                                print "\nError->\tEmpty 'Y' ( Excel Row %d"%rx,")\n"
                                                sys.exit()
					if( str(sheet.cell_value(rowx=rx, colx=ColumnIN)) != str(ObjCorrs) \
					    and len(TmpCorrs) > 0):
                                                Corrections.append( TmpCorrs )
                                                TmpCorrs = []
                                                ObjCorrs = sheet.cell_value(rowx=rx, colx=ColumnIN)
                                                ObjLink2Excel = rx+1

					x = sheet.cell_value(rowx=rx, colx=ColumnX)
                                        y = sheet.cell_value(rowx=rx, colx=ColumnY)

					if FlipY > 1:   y = (FlipY - y)

					if PixelRatioMethod == "divide":
						x = x/PR
						y = y/PR
					else:
						x = x*PR
						y = y*PR

                                        TmpCorrs.append( [ str(sheet.cell_value(rowx=rx, colx=ColumnIN)), \
                                                           int(sheet.cell_value(rowx=rx, colx=ColumnS)), \
                                                           x, y ])

                        if len(TmpCorrs) > 0: Corrections.append( TmpCorrs )
			TmpCorrs = []

		elif( PatternAxisSheet.search(sheet.name) ):
                        for xx in range(sheet.ncols):
                                if( PatternIN.search(sheet.cell_value(rowx=0, colx=xx) ) ):
                                        ColumnIN = xx
                                if( PatternX1.search(sheet.cell_value(rowx=0, colx=xx) ) ):
                                        ColumnX1  = xx
                                if( PatternY1.search(sheet.cell_value(rowx=0, colx=xx) ) ):
                                        ColumnY1  = xx
                                if( PatternX2.search(sheet.cell_value(rowx=0, colx=xx) ) ):
                                        ColumnX2  = xx
				if( PatternY2.search(sheet.cell_value(rowx=0, colx=xx) ) ):
                                        ColumnY2  = xx

			TmpAxis      = ""
                        ObjAxis      = str(sheet.cell_value(rowx=1, colx=ColumnIN))
                        ObjLink2Excel = 99999

                        for rx in range(sheet.nrows):
                                if( (rx != 0) and (sheet.cell_value(rowx=rx, colx=0) != "") ):
                                        if(ObjLink2Excel == 99999):
                                                ObjLink2Excel = rx+1
                                        if( str(sheet.cell_value(rowx=rx, colx=ColumnIN)) == ""):
                                                print "\nError->\tEmpty 'Image Name' ( Excel Row %d"%rx,")\n"
                                                sys.exit()
                                        if( str(sheet.cell_value(rowx=rx, colx=ColumnX1)) == ""):
                                                print "\nError->\tEmpty 'X1' ( Excel Row %d"%rx,")\n"
                                                sys.exit()
                                        if( str(sheet.cell_value(rowx=rx, colx=ColumnY1)) == ""):
                                                print "\nError->\tEmpty 'Y1' ( Excel Row %d"%rx,")\n"
                                                sys.exit()
                                        if( str(sheet.cell_value(rowx=rx, colx=ColumnX2)) == ""):
                                                print "\nError->\tEmpty 'X2' ( Excel Row %d"%rx,")\n"
                                                sys.exit()
					if( str(sheet.cell_value(rowx=rx, colx=ColumnY2)) == ""):
                                                print "\nError->\tEmpty 'Y2' ( Excel Row %d"%rx,")\n"
                                                sys.exit()
                                        if( str(sheet.cell_value(rowx=rx, colx=ColumnIN)) != str(ObjAxis) \
                                            and len(TmpAxis) > 0):
                                                Axes.append( TmpAxis )
                                                TmpAxis = ""
                                                ObjAxis = sheet.cell_value(rowx=rx, colx=ColumnIN)
                                                ObjLink2Excel = rx+1

					x1 = sheet.cell_value(rowx=rx, colx=ColumnX1)
                                        y1 = sheet.cell_value(rowx=rx, colx=ColumnY1)
                                        x2 = sheet.cell_value(rowx=rx, colx=ColumnX2)
                                        y2 = sheet.cell_value(rowx=rx, colx=ColumnY2)

					#if FlipY > 1:   y1 = (FlipY - y1); y2 = (FlipY - y2)

					if PixelRatioMethod == "divide":
						x1 = x1/PR 
						y1 = y1/PR
						x2 = x2/PR
						y2 = y2/PR
					else:
						x1 = x1*PR
                                                y1 = y1*PR
                                                x2 = x2*PR
                                                y2 = y2*PR

                                        # ImageName ImagePlane TimeInterval Track/Object X Y Link2Excel
                                        TmpAxis = ( [ str(sheet.cell_value(rowx=rx, colx=ColumnIN)), \
						      x1,y1,x2,y2 ])
                        if len(TmpAxis) > 0: Axes.append( TmpAxis )
                        TmpAxis = ""

		else:
        		for xx in range(sheet.ncols):
		                if( PatternX.search(sheet.cell_value(rowx=0, colx=xx) ) ):
                		        ColumnX = xx
		                if( PatternY.search(sheet.cell_value(rowx=0, colx=xx) ) ):
                		        ColumnY = xx
		                if( PatternT.search(sheet.cell_value(rowx=0, colx=xx) ) ):
                		        ColumnT = xx
		                if( PatternO.search(sheet.cell_value(rowx=0, colx=xx) ) ):
                		        ColumnT = xx
                		if( PatternIN.search(sheet.cell_value(rowx=0, colx=xx) ) ):
                        		ColumnIN = xx
                		if( PatternIP.search(sheet.cell_value(rowx=0, colx=xx) ) ):
                        		ColumnIP = xx
		                if( PatternZ.search(sheet.cell_value(rowx=0, colx=xx) ) ):
                		        ColumnIP = xx
		                if( PatternTI.search(sheet.cell_value(rowx=0, colx=xx) ) ):
                		        ColumnTI = xx
				if( PatternF.search(sheet.cell_value(rowx=0, colx=xx) ) ):
                                        ColumnIP = xx

			TmpCoords        = []
			TimeCummulative  = 0
 			Object           = 1
        		Link2ExcelCoords = 99999

		        for rx in range(sheet.nrows):
                		if( (rx != 0) and (sheet.cell_value(rowx=rx, colx=0) != "") ):

					if(Link2ExcelCoords == 99999):
						Link2ExcelCoords = rx+1

		                        if(ColumnTI == 99):
                		                TimeInterval = 0
		                        else:
                		                TimeInterval = float(sheet.cell_value(rowx=rx, colx=ColumnTI))

		                        if( str(sheet.cell_value(rowx=rx, colx=ColumnIN)) == ""):
                		                print "\nError->\tEmpty 'Image Name' ( Excel Row %d"%rx,")\n"
                                		sys.exit()
		                        if( str(sheet.cell_value(rowx=rx, colx=ColumnIP)) == ""):
                		                print "\nError->\tEmpty 'Image Plane/Z' ( Excel Row %d"%rx,")\n"
                                		sys.exit()
		                        if( str(sheet.cell_value(rowx=rx, colx=ColumnT)) == ""):
                		                print "\nError->\tEmpty 'Track/Object' ( Excel Row %d"%rx,")\n"
                                		sys.exit()
		                        if( str(sheet.cell_value(rowx=rx, colx=ColumnX)) == ""):
                		                print "\nError->\tEmpty 'X' ( Excel Row %d"%rx,")\n"
                                		sys.exit()
   		               		if( str(sheet.cell_value(rowx=rx, colx=ColumnY)) == ""):
                		                print "\nError->\tEmpty 'Y' ( Excel Row %d"%rx,")\n"
                                		sys.exit()

                        		if( sheet.cell_value(rowx=rx, colx=ColumnT) != Object): # and len(TmpCoords) > 0):
                                		Coords.append( TmpCoords )
                                		TmpCoords = []
						TimeCummulative = 0
                                		Object = sheet.cell_value(rowx=rx, colx=ColumnT)
                                		Link2ExcelCoords = rx+1

					# ImageName ImagePlane TimeInterval Track/Object X Y Link2Excel

					TimeCummulative += TimeInterval
					if(TimeStart == 0 and TimeEnd == 0 ) or \
					  (TimeCummulative >= TimeStart and TimeCummulative < TimeEnd):

						x = sheet.cell_value(rowx=rx, colx=ColumnX)
						y = sheet.cell_value(rowx=rx, colx=ColumnY)
						if len(Coords) > 0 and  FlipY > 1:	y = (FlipY - y)
						#if FlipY > 1:      y = (FlipY - y)

						#Apply the pixel ratio
						if PixelRatioMethod == "divide":
							x = x/PR
							y = y/PR
						else:
							x = float(x)*PR
							y = float(y)*PR

	                        		TmpCoords.append( [ str(sheet.cell_value(rowx=rx, colx=ColumnIN)), \
	                                            		int(sheet.cell_value(rowx=rx, colx=ColumnIP)), \
	                                            		float(TimeInterval), \
	                                            		int(sheet.cell_value(rowx=rx, colx=ColumnT)), \
	                                            		x,y,Link2ExcelCoords ])
			
        #	if len(Coords) > 0 and len(TmpCoords) > 0: 
			Coords.append( TmpCoords )
			TmpCoords = []
			TimeCummulative = 0
		Cooords.append( Coords )
		Coords = []

	if len(Corrections) < 1: Corrections = [99,99,99,99]
	if len(Axes) < 1:	 Axes        = [99,99,99,99] #[100,120,100,100] #[99,99,199,99]

	return Cooords, Corrections, Axes

#------------------------------------------------------------------------------
def ReadExcelCoordsMetamorph (FileName):

        import xlrd
        import re

        try:
                F_Coords = open(FileName,'r')
        except:
                print "\nError->\tFile: %s does not exist\n" % FileName
		sys.exit()

        book  = xlrd.open_workbook(FileName)
        sheet = book.sheet_by_index(0)

        Tmp       = 0
        TmpCoords = []
        Coords    = []
	ImageNameColumn  = {}
	Img = []
	Link2ExcelCoords = []
        PatternX = re.compile(r'\AX\Z')
	PatternY = re.compile(r'\AY\Z')
	PatternO = re.compile(r'\AObject #\Z')
	PatternF = re.compile(r'\AFrame #\Z')
	PatternT = re.compile(r'\ATime Interval\Z')
	PatternI = re.compile(r'\AImage Name\Z')

	for xx in range(sheet.ncols):
		if( PatternX.search(sheet.cell_value(rowx=0, colx=xx) ) ):
			ColumnX = xx
		if( PatternY.search(sheet.cell_value(rowx=0, colx=xx) ) ):
			ColumnY = xx
		if( PatternO.search(sheet.cell_value(rowx=0, colx=xx) ) ):
			ColumnO = xx
		if( PatternF.search(sheet.cell_value(rowx=0, colx=xx) ) ):
			ColumnF = xx
		if( PatternT.search(sheet.cell_value(rowx=0, colx=xx) ) ):
                        ColumnT = xx
		if( PatternI.search(sheet.cell_value(rowx=0, colx=xx) ) ):
                        ColumnI = xx

	Object = 1
	ParticleCount = 1
	
	Link2ExcelCoords.append(2)
        for rx in range(sheet.nrows):
                if( ( rx != 0 ) and ( sheet.cell_value(rowx=rx, colx=0) != "" ) ): 
			if ( sheet.cell_value(rowx=rx, colx=ColumnO) != Object ):
                        	Coords.append( TmpCoords )
				Img.append( String )
				String = ""
                        	TmpCoords = []
                        	Tmp = 0
				Object = sheet.cell_value(rowx=rx, colx=ColumnO)

				ParticleCount += 1
				Link2ExcelCoords.append(rx+1)

                       	TmpCoords.append( [ int("%d" % \
					    sheet.cell_value(rowx=rx, colx=ColumnF)),
                               	            float("%.4f" % \
					    sheet.cell_value(rowx=rx, colx=ColumnX)),
                                       	    float("%.4f" % \
					    sheet.cell_value(rowx=rx, colx=ColumnY)),
					    int("%d" % \
                                            sheet.cell_value(rowx=rx, colx=ColumnT))
                                       	] )

			ImageNameColumn[ str( sheet.cell_value(rowx=rx, colx=ColumnI) ) ] = 1 	
			String = str( sheet.cell_value(rowx=rx, colx=ColumnI) )

                       	Tmp += 1
        Coords.append( TmpCoords )
	Img.append(String)
        Tmp       = 0
        TmpCoords = []

        return Coords,Link2ExcelCoords,Img,ImageNameColumn

#------------------------------------------------------------------------------
def ReadExcelCoordsMetamorph_Richard (FileName):

        import xlrd
        import re

        try:
                F_Coords = open(FileName,'r')
        except:
                print "\nError->\tFile: %s does not exist\n" % FileName
                sys.exit()

        book  = xlrd.open_workbook(FileName)
        sheet = book.sheet_by_index(0)

	PatternX  = re.compile(r'\AX\Z')
        PatternY  = re.compile(r'\AY\Z')
        PatternT  = re.compile(r'\ATrack #\Z')
        PatternN  = re.compile(r'\AImage Name\Z')
        PatternP1 = re.compile(r'\AZ\Z')
	PatternP2 = re.compile(r'\AImage Plane\Z')

	ColumnP = 0
	ColumnN = 0

	for xx in range(sheet.ncols):
                if( PatternX.search(sheet.cell_value(rowx=0, colx=xx) ) ):
                        ColumnX = xx

                if( PatternY.search(sheet.cell_value(rowx=0, colx=xx) ) ):
                        ColumnY = xx
                if( PatternT.search(sheet.cell_value(rowx=0, colx=xx) ) ):
                        ColumnT = xx
                if( PatternN.search(sheet.cell_value(rowx=0, colx=xx) ) ):
                        ColumnN = xx
                if( PatternP1.search(sheet.cell_value(rowx=0, colx=xx) ) ):
                        ColumnP = xx 
		if( PatternP2.search(sheet.cell_value(rowx=0, colx=xx) ) ):
                        ColumnP = xx

	if(ColumnP < 1):
		ColumnP = 1
	if(ColumnN < 1):
                ColumnN = 1

	Coords           = []
	TmpCoords        = []
	Link2ExcelCoords = []
	Object           = 1

	Link2ExcelCoords.append(2)

	for rx in range(sheet.nrows):
		if( (rx != 0) and (sheet.cell_value(rowx=rx, colx=0) != "") ):

			if( sheet.cell_value(rowx=rx, colx=ColumnT) != Object ):
				Coords.append( TmpCoords )
				TmpCoords = []
				Object = sheet.cell_value(rowx=rx, colx=ColumnT)
				Link2ExcelCoords.append(rx+1)

			TmpCoords.append( [ str(sheet.cell_value(rowx=rx, colx=ColumnN)), \
                                            int(sheet.cell_value(rowx=rx, colx=ColumnP)), \
			                    int(sheet.cell_value(rowx=rx, colx=ColumnT)), \
			                    sheet.cell_value(rowx=rx, colx=ColumnX), \
			                    sheet.cell_value(rowx=rx, colx=ColumnY) 
                                          ])			

	Coords.append( TmpCoords )

	return Coords, Link2ExcelCoords

#------------------------------------------------------------------------------
def ReadPolygonFile(FileName):

	try:
                F_Polygon = open(FileName,'r')
        except:
                print "\nError->\tFile: %s does not exist\n" % FileName
                sys.exit()

	polygon = []
	LineCount = len( open(FileName,'r').readlines() )

        for line in F_Polygon:
                line = line.rstrip('\n')
		line = line.replace(']','')
		line = line.replace('[','')
		line = line.replace(',','')
                element = line.split(' ')
		#polygon.append( float(element[1]) )
		#polygon.append( float(element[2]) ) 
		polygon.append( [float(element[1]),float(element[2])] )

        F_Polygon.close()

	return polygon


#------------------------------------------------------------------------------
def ReadVibtest_SingleFile (CsvFile, TimeInterval, NumArenas):
# vibtest file format
# "000:00:02.476","Info","Arena",1,"Target_location",-1,-1,"Zone",0,"Distance",101,"Segments",1
# Key Columns: 0 TimeStamp
#              3 Arena 
#              5 X
#              6 Y
#              8 Zone
#             10 Distance
#             12 Segments

	import re
	import csv

	try:
		F_Coords = open(CsvFile,'r')
	except:
		print "\nError->\tFile: %s does not exist\n" % CsvFile
		sys.exit()

	(O_Dir,O_File) = os.path.split(CsvFile)
	(O_Name,O_Ext) = os.path.splitext(O_File)
	OutName =  '.' . join([O_Name , "xls"])

	ExptData     = []
	Corrections  = []
	Axes         = []
	Perturbations = []
	TotalFrames  = 0

	count = 0
	while (count < NumArenas):
		ExptData.append([])
		count += 1

	LineNumber = 1
	with open(CsvFile, 'rb') as csvfile:

		VibTestFile = csv.reader(csvfile, delimiter=',', quotechar='"')

		num = 0
		ImagePlane = 1

		print "PS.Inputs: ImageName,ImagePlane,Arena,X,Y,Zone,Distance,Segment"

		for element in VibTestFile:

			if( (element[2] == "Arena") and ( element[4] == "Target_location")):
				if( num < 10):
					print "PS.Inputs: ",
					print ',' . join([O_Name, str(num), str(ImagePlane),
									element[3], element[5], element[6],
									element[8], element[10], element[12]])

				if( (float(element[5]) >= 0) and (float(element[6]) >= 0)):
					#(TSa,TSb) = parser.parse(str(element[0])).strftime('%Y-%m-%d %H:%M:%S.%f').split('.') 
					#timestamp = datetime.strptime(str("%s.%03d" % (TSa, int(TSb) / 1000)), '%Y-%m-%d %H:%M:%S.%f')
					ExptData[ int(element[3])-1 ].append( [str(O_Name), int(ImagePlane), int(TimeInterval),
														   float(element[3]),
														   float(element[5]), float(element[6]), 
														   int(LineNumber), int(num), str(element[0]) ] )

				if(int(element[3]) == 24):
					ImagePlane += 1
				num += 1

			elif( (len(element) >= 12) and (element[4] == "ARENA_DISTANCES") and 
				  (element[7] == "PreStartle") and (int(element[6]) <= 10) ):	
				#(TSa,TSb) = parser.parse(str(element[0])).strftime('%Y-%m-%d %H:%M:%S.%f').split('.')
				#timestamp = datetime.strptime(str("%s.%03d" % (TSa, int(TSb) / 1000)), '%Y-%m-%d %H:%M:%S.%f')
				Perturbations.append( [ str(O_Name), int(num), int(ImagePlane), str(element[0]), 
                                       int(element[5]), int(element[6]), str(element[7]) ]  )
				
			elif( (len(element) >= 12) and (element[4] == "ARENA_DISTANCES") and 
				  (element[7] == "Startle") and (int(element[6]) <= 10) ):
				#(TSa,TSb) = parser.parse(str(element[0])).strftime('%Y-%m-%d %H:%M:%S.%f').split('.')
				#timestamp = datetime.strptime(str("%s.%03d" % (TSa, int(TSb) / 1000)), '%Y-%m-%d %H:%M:%S.%f')
				Perturbations.append( [ str(O_Name), int(num), int(ImagePlane), str(element[0]), 
                                       int(element[5]), int(element[6]), str(element[7]) ]  )

			elif( (len(element) >= 12) and (element[4] == "ARENA_DISTANCES") and   
                  (element[7] == "PostStartle") and (int(element[6]) <= 10) ):
				#(TSa,TSb) = parser.parse(str(element[0])).strftime('%Y-%m-%d %H:%M:%S.%f').split('.')
				#timestamp = datetime.strptime(str("%s.%03d" % (TSa, int(TSb) / 1000)), '%Y-%m-%d %H:%M:%S.%f')
				Perturbations.append( [ str(O_Name), int(num), int(ImagePlane), str(element[0]), 
                                       int(element[5]), int(element[6]), str(element[7]) ]  )

			LineNumber += 1

		TotalFrames = ImagePlane

	if len(Corrections) < 1: Corrections = [99,99,99,99]
	if len(Axes) < 1:        Axes        = [99,99,99,99] #[100,120,100,100] #[99,99,199,99]

	return ExptData, Corrections, Axes, Perturbations, TotalFrames

#------------------------------------------------------------------------------
# FIN
#------------------------------------------------------------------------------
