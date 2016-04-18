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

#import cgitb; cgitb.enable()

import random
import numpy as na
import os,sys,math,re
#import Numeric
import scipy
#from ParticleStats_Maths import *
import ParticleStats_Maths   as PS_Maths
import ParticleStats_Outputs as PS_Outputs
myenv = os.environ
#myenv['HOME'] = '/home/rhamilto/public_html/ParticleStats/Excels/'

import matplotlib
matplotlib.use('Agg')
from matplotlib import pylab
from pylab import *

import Image, ImageFont, ImageDraw, ImageColor, ImageEnhance


#------------------------------------------------------------------------------
def PlotBinaryOriginal ( FileName,OutName,AxisAngle,FinalIMSize,FlipY,Orient ):
# Function to create PNG and TIFF images of the original image 
# Created 20/05/08
# Modifies 230608 to take account of rotation offset of image

        OutName = OutName+"_original"
        im   = Image.open(FileName).convert("RGBA")
	im2  = Image.new("RGBA",(int(FinalIMSize),int(FinalIMSize)),(0,0,0,0))

	pasteX = (im2.size[0]/2) - (im.size[0]/2)
        pasteY = (im2.size[1]/2) - (im.size[1]/2)

        im2.paste(im,(pasteX,pasteY))

	if FlipY:
		im2 = im2.transpose(Image.FLIP_TOP_BOTTOM)

	if( int(AxisAngle) > 0):
		im2 = im2.rotate(AxisAngle-Orient)


	im2.save(OutName+".tif","TIFF")
	im2.save(OutName+".png","PNG")

        return OutName

#------------------------------------------------------------------------------
def PlotBinaryTrails_1 ( FileName,OutName,Coords,Colours,Axis,AxisAngle,\
			 X,Y,Factor,PlotLines,FinalIMSize):
# Function to create PNG and TIFF images displaying the particle trails
# Red end points and green start points. Trail lines coloured by "i" index
# Created 20/05/08

        OutName = OutName+"_trails"

	im  = Image.open(FileName).convert("RGBA")
	if(len(Axis) != 1):
		im  = im.rotate( ((360-AxisAngle)+90)*-1 ,expand=1)
	imN = Image.new("RGBA",(int(FinalIMSize),int(FinalIMSize)),(0,0,0,0))

	pasteX = (imN.size[0]/2) - (im.size[0]/2)
	pasteY = (imN.size[1]/2) - (im.size[1]/2)
	imN.paste(im,(pasteX,pasteY))

        draw = ImageDraw.Draw(imN)

	i = 0
        while i < len(Coords):
		#Vectors = [Coords[i][-1][3]-Coords[i][0][3],\
		#	   Coords[i][-1][4]-Coords[i][0][4]]
		#Angle   = PS_Maths.CalculateVectorAngle(Vectors)
		#Scale = (255.0/360.0) 
		#Angle = int(Angle * Scale)
		#SAngle = int(Angle * Scale)
		#if(Angle >= 0 and Angle < 45):
		#	Col = (127,255,0,255)
		#elif(Angle >= 45 and Angle < 90):
		#	Col = (0,255,0,255)
		#elif(Angle >= 90 and Angle < 135):
		#	Col = (0,255,255,255)
		#elif(Angle >= 135 and Angle < 180):
                #        Col = (0,0,255,255)
		#elif(Angle >= 180 and Angle < 225):
                #        Col = (255,0,255,255)
		#elif(Angle >= 225 and Angle < 270):
                #        Col = (255,0,0,255)
		#elif(Angle >= 270 and Angle < 315):
                #        Col = (255,140,0,255)
		#else:
		#	Col = (255,255,0,255)

		draw.ellipse((Coords[i][0][4]-1,Coords[i][0][5]-1,\
                               Coords[i][0][4]+1,Coords[i][0][5]+1),\
                               fill=(0,255,0,255) )
                draw.ellipse((Coords[i][-1][4]-1,Coords[i][-1][5]-1,\
                               Coords[i][-1][4]+1,Coords[i][-1][5]+1),\
                               fill=(255,0,0,255) )
		draw.line((Coords[i][0][4],Coords[i][0][5],\
                            Coords[i][-1][4],Coords[i][-1][5]),\
                            fill=Colours[i]  )
		#draw.line((Coords[i][0][4],Coords[i][0][5],\
                #            Coords[i][-1][4],Coords[i][-1][5]),fill=Col  )
		i += 1

	if(len(Axis) != 1):
		draw.line((Axis[0],Axis[1],Axis[2],Axis[3]),\
			   fill=(0,0,0,200),width=3)
		draw.ellipse((Axis[0]-1,Axis[1]-1,Axis[0]+2,Axis[1]+2),\
			      fill=(0,255,0,125) )
		draw.ellipse((Axis[2]-1,Axis[3]-1,Axis[2]+2,Axis[3]+2),\
			      fill=(255,0,0,125) )

	if(PlotLines):
		i = 1
	        while i < Factor:
        	        draw.line((0,(Y/Factor)*i,imN.size[1],(Y/Factor)*i),\
                	                fill=(0,0,0,55))
	                draw.line(((X/Factor)*i,0,(X/Factor)*i,imN.size[0]),\
        	                        fill=(0,0,0,55))

                	i += 1

	comp = imN
        comp.save(OutName+".png","PNG")
        comp.save(OutName+".tif","TIFF")

        return OutName

#------------------------------------------------------------------------------
def PlotSVGTrails_1 ( OutName,O_Name,Coords,Colours,Axis,Factor,FinalIMSize,Polygon,PolygonColour):
# Function to create PNG and TIFF images displaying the particle trails
# Red end points and green start points. Trail lines coloured by "i" index
# Created 19/05/08

        OutName = OutName+"_trails"
        scene = Scene(OutName,FinalIMSize,FinalIMSize)

	scene.add( SVGImage(FinalIMSize,FinalIMSize,O_Name+"_"+\
                            str(int(Factor*Factor))+"_original.png") )

	PolygonColour = PS_Outputs.ColourConvert( PolygonColour ) 

	if(len(Axis) != 1):
        	i = 1
	else:
		i = 0

	i = 0
        while i < len(Coords):
		j = 0
		while j < len(Coords[i]):
			RGB = PS_Outputs.ColourConvert(Colours[j])

			scene.add(Circle((Coords[i][j][0][4],Coords[i][j][0][5]),\
					  2,0,0,(0,255,0),0.5))
			scene.add(Circle((Coords[i][j][-1][4],Coords[i][j][-1][5]),\
					  2,0,0,(255,0,0),0.5))
			scene.add(Line((Coords[i][j][0][4],Coords[i][j][0][5]),\
                                       (Coords[i][j][-1][4],Coords[i][j][-1][5]),\
                                       (RGB[0],RGB[1],RGB[2]),1,1))
			j += 1
                i += 1

	if(len(Axis) != 1):
		scene.add(Line((Axis[0],Axis[1]),(Axis[2],Axis[3]),(0,0,0),1,1))
		scene.add(Circle((Axis[0],Axis[1]),1,0,1,(0,255,0),0.5))
		scene.add(Circle((Axis[2],Axis[3]),1,0,1,(255,0,0),0.5))

	#Draw on the user define polygon
        polypoints = ""
        if( len(Polygon) > 2):
                i = 0
                while i < len(Polygon):
                        polypoints += str(Polygon[i][0])+","+\
                                      str(Polygon[i][1])+" "
                        i += 1
        # Toggle off region drawing!
                scene.add( PolygonShape((polypoints),(255,255,255),\
                                        0,PolygonColour,1,3) )

        scene.write_svg()

        return OutName

#------------------------------------------------------------------------------
def PlotSVGTrails_AngColour ( OutName,O_Name,Coords,Colours,Axis,Factor,\
			      FinalIMSize,Polygon,PolygonColour):
# Same as PlotSVGTrails_1 except trails are coloured by their angle of travel

        OutName = OutName+"_trails_anglescoloured"
        scene = Scene(OutName,FinalIMSize,FinalIMSize)

        scene.add( SVGImage(FinalIMSize,FinalIMSize,O_Name+"_"+\
                            str(int(Factor*Factor))+"_original.png") )

        PolygonColour = PS_Outputs.ColourConvert( PolygonColour )

        if(len(Axis) != 1):
                i = 1
        else:
                i = 0

        i = 0
        while i < len(Coords):
		Ang = PS_Maths.CalculateVectorAngle([\
				(Coords[i][2]-Coords[i][0]),\
				(Coords[i][3]-Coords[i][1])])

		if  ( Ang >= 0   and Ang < 45 ):
			RGB = PS_Outputs.ColourConvert(Colours[0])
		elif( Ang >= 45  and Ang < 135):
			RGB = PS_Outputs.ColourConvert(Colours[1])
		elif( Ang >= 135 and Ang < 225):
			RGB = PS_Outputs.ColourConvert(Colours[2])
		elif( Ang >= 225 and Ang < 315):
			RGB = PS_Outputs.ColourConvert(Colours[3])
		elif( Ang >= 315 and Ang <= 360):
			RGB = PS_Outputs.ColourConvert(Colours[0])

                #scene.add(Circle((Coords[i][0],Coords[i][1]),\
                #                  2,0,0,(0,255,0),0.5))
                #scene.add(Circle((Coords[i][2],Coords[i][3]),\
                #                   2,0,0,(255,0,0),0.5))
                scene.add(Line((Coords[i][0],Coords[i][1]),\
                                   (Coords[i][2],Coords[i][3]),\
                                   (RGB[0],RGB[1],RGB[2]),1,1))
                i += 1

        if(len(Axis) != 1):
                scene.add(Line((Axis[0],Axis[1]),(Axis[2],Axis[3]),(0,0,0),1,1))
                scene.add(Circle((Axis[0],Axis[1]),1,0,1,(0,255,0),0.5))
                scene.add(Circle((Axis[2],Axis[3]),1,0,1,(255,0,0),0.5))

        #Draw on the user define polygon
        polypoints = ""
        if( len(Polygon) > 2):
                i = 0
                while i < len(Polygon):
                        polypoints += str(Polygon[i][0])+","+\
                                      str(Polygon[i][1])+" "
                        i += 1
        # Toggle off region drawing!
                scene.add( PolygonShape((polypoints),(255,255,255),\
                                        0,PolygonColour,1,3) )

        scene.write_svg()

	return OutName

#------------------------------------------------------------------------------
def PlotBinaryXrosses (FileName, OutName,Coords,Colours,SquareCoords,\
		       Trails,X,Y,Factor):
# Function to create PNG and TIFF images displaying the particle trails
# as displayed by how they cross the grid lines. mainly for debugging 
# Created 20/05/08

        OutName = OutName+"_xrosses"
	im      = Image.open(FileName).convert("RGBA")
        imN     = Image.new("RGBA", im.size, (0,0,0,0))
        draw    = ImageDraw.Draw(imN)

	#First Draw the trails
	i = 0
        while i < len(Coords):
		draw.line((Coords[i][0][3],Coords[i][0][4],\
                           Coords[i][-1][3],Coords[i][-1][4]),\
                           fill=Colours[i]  )
                i += 1

	#Now draw the red/green divides on the grid lines
	i = 0
        while i < len(SquareCoords):
		j = 0
                while j < len(Trails):
                        #Does the line cross the square?
                        Cross = 0
                        Line  = []
                        Cross,Line,Debug = PS_Maths.LineWithinSquare(\
                                                [SquareCoords[i][0],\
                                                 SquareCoords[i][1],\
                                                 SquareCoords[i][0]+X/Factor,\
                                                 SquareCoords[i][1]+Y/Factor],\
                                                [Trails[j][0],Trails[j][1],\
                                                 Trails[j][2],Trails[j][3]] )
			if(Cross ):
				draw.ellipse( (Line[0][0]-1,Line[0][1]-1,\
                                               Line[0][0],Line[0][1]),fill="white")
                                draw.ellipse( (Line[1][0],Line[1][1],Line[1][0]+1,\
                                               Line[1][1]+1),fill="black")
			j += 1
		i += 1

	i = 1
        while i < Factor:
                draw.line((0,(Y/Factor)*i,im.size[1],(Y/Factor)*i),\
				fill=(255,0,0,50))
                draw.line(((X/Factor)*i,0,(X/Factor)*i,im.size[0]),\
				fill=(0,0,255,50))

                i += 1

	comp = Image.composite(imN,im,imN)
        comp.save(OutName+".tif","TIFF")
        comp.save(OutName+".png","PNG")
	
        return OutName

#------------------------------------------------------------------------------
def PlotBinaryWindMap_1 (FileName,OutName,X,Y,AxisAngle,\
			 Polygon,Factor,SquareCoords,\
			 SquareBigVector,SquareBigVectorAngle,\
			 SquareBigVectorMagnitudeLongest,FinalIMSize,AxisColours):
# Function to create PNG and TIFF images displaying the wind map
#  
# Created 20/05/08
# Modified 25/06/08: To Include new rotation ans shift code

	AngleText = 0

        OutName = OutName+"_windmap"
	im      = Image.open(FileName).convert("RGBA")
	imN     = Image.new("RGBA",(int(FinalIMSize),int(FinalIMSize)),(0,0,0,0))
	im2     = Image.new("RGBA",(int(FinalIMSize),int(FinalIMSize)),(0,0,0,0))

	pasteX = (imN.size[0]/2) - (im.size[0]/2)
	pasteY = (imN.size[1]/2) - (im.size[1]/2)
	imN.paste(im,(pasteX,pasteY))
	if( int(AxisAngle) > 0):
		imN = imN.rotate(AxisAngle-90)

        draw    = ImageDraw.Draw(im2)

        i = 0
        while i < len(SquareCoords):

                if SquareBigVectorAngle[i] > 0.0:
                        (R,G,B) = PS_Maths.ColourBasedOnAngleSelector(\
                           		 PS_Maths.CalculateVectorAngle(SquareBigVector[i]),AxisColours )
			H = PS_Maths.CalculateVectorMagnitude(SquareBigVector[i]) * \
			    ( float(175) / float(SquareBigVectorMagnitudeLongest ))

			draw.rectangle( (SquareCoords[i][0],SquareCoords[i][1],\
                                         SquareCoords[i][0]+(X/Factor),\
                                         SquareCoords[i][1]+(Y/Factor) ),\
                                         fill=(R,G,B,H) )

                        CX = (SquareCoords[i][0] + (X/Factor)/2)
                        CY = (SquareCoords[i][1] + (Y/Factor)/2)
                        XE,YE = PS_Maths.GetCircleEdgeCoords(CX,CY,\
                                        SquareBigVectorAngle[i],(X/Factor)/2)

			draw.line((CX,CY,XE,YE),fill='black',\
				  width=int((X/Factor)/16) )
                        draw.ellipse( (CX-1,CY-1, CX+1,CY+1), fill=("black") )

			ArrX1,ArrY1 = PS_Maths.GetCircleEdgeCoords(CX,CY,\
                                              (SquareBigVectorAngle[i]+7.12),\
					      (((X/Factor)/2)-5))
                        ArrX2,ArrY2 = PS_Maths.GetCircleEdgeCoords(CX,CY,\
                                               (SquareBigVectorAngle[i]-7.12),\
					       (((X/Factor)/2)-5))
                        draw.polygon(((XE,YE),(ArrX1,ArrY1),(ArrX2,ArrY2)),\
                                     fill="black")
#			if AngleText:
#				font = ImageFont.truetype("arial.ttf",9)
#				draw.text((CX,CY), str(int(SquareNoLines[i])),\
#                                        fill="green" )

                i += 1

        i = 1
        while i < Factor:
		draw.line((0,(Y/Factor)*i, imN.size[1], (Y/Factor)*i),\
			  fill=(255,0,0,50))
                draw.line(((X/Factor)*i, 0, (X/Factor)*i, imN.size[0]),\
			  fill=(0,0,255,50))
                i += 1

	#Draw on the user defines polygon
	polystring = []
	if( len(Polygon) > 2):
		i = 0
		while i < len(Polygon):
			polystring.append( Polygon[i][0] )
			polystring.append( Polygon[i][1] )
			i += 1
		drawP = ImageDraw.Draw(imN)
		drawP.polygon(polystring,outline=(0,0,0,255))

	comp = Image.composite(im2,imN,im2)
        comp.save(OutName+".tif","TIFF")
        comp.save(OutName+".png","PNG")

        return OutName

#------------------------------------------------------------------------------
def PlotSVGWindMap_1 (OutName,O_Name,X,Y,Factor,Polygon,SquareCoords,\
		      SquareBigVector,SquareBigVectorAngle,\
		      SquareBigVectorMagnitudeLongest,OpacityMethod,SquareNoLines,\
		      FinalIMSize,AxisColours,\
		      ShowArrows,ArrowColour,ShowGrid,ShowRectangles,PolygonColour):
# Function to create SVG images displaying the wind map
#  
# Created 19/05/08
# Modified 260608 to take new rotated image data - 800x800 image

	OutName = OutName+"_windmap_"+OpacityMethod
        scene = Scene(OutName,FinalIMSize,FinalIMSize)

	LineW = (X/Factor)/16

	if(LineW < 1): 
		LineW = 1

	ArrowColour   = PS_Outputs.ColourConvert( ArrowColour )
	PolygonColour = PS_Outputs.ColourConvert( PolygonColour )

	scene.add( DefineArrow( LineW*2,LineW*2,0,5,ArrowColour ) )
        scene.add( SVGImage(FinalIMSize,FinalIMSize,O_Name+"_"+\
                            str(int(Factor*Factor))+"_original.png") )


	i = 0
        while i < len(SquareCoords):
                if (SquareBigVector[i][0] != 0 or SquareBigVector[i][1] != 0):
			(R,G,B) = PS_Maths.ColourBasedOnAngleSelector(\
                                         PS_Maths.CalculateVectorAngle(SquareBigVector[i]),AxisColours)
			if OpacityMethod == "num":
				H = SquareNoLines[i] * (float(175) / float(max(SquareNoLines))) 
			elif OpacityMethod == "mag":
                    	    H = PS_Maths.CalculateVectorMagnitude(SquareBigVector[i]) * \
                        	    ( float(175) / float(SquareBigVectorMagnitudeLongest ))

			if ShowRectangles == 1:
				scene.add( Rectangle((SquareCoords[i][0],\
						      SquareCoords[i][1]),\
						      (X/Factor),(Y/Factor),(R,G,B),\
						      (float(H)/255)-0.0,\
						      (255,255,255),0.0 ) )
			CX = (SquareCoords[i][0] + (X/Factor)/2)
                        CY = (SquareCoords[i][1] + (Y/Factor)/2)
			XE,YE = PS_Maths.GetCircleEdgeCoords(CX,CY,\
					SquareBigVectorAngle[i],\
					((X/Factor)/2)-((X/Factor)/10) )

			if ShowArrows:
				scene.add( ArrowLine( (CX,CY), (XE,YE),ArrowColour,LineW))	
				#scene.add( Circle((CX,CY),LineW,0,1,ArrowColour,1))		
		i += 1

	#Draw on the user define polygon
        polypoints = ""
        if( len(Polygon) > 2):
                i = 0
                while i < len(Polygon):
                        polypoints += str(Polygon[i][0])+","+\
                                      str(Polygon[i][1])+" "
                        i += 1
	# Toggle off region drawing!
                scene.add( PolygonShape((polypoints),(255,255,255),\
                                        0,PolygonColour,1,3) )

	if ShowGrid:
		RGB=[0,0,0]
	        i = 1
	        while i < Factor:
	                scene.add(Line( (0,(Y/Factor)*i),(FinalIMSize,(Y/Factor)*i),\
					(RGB[0],RGB[1],RGB[2]),0.5,1))
	                scene.add(Line( ((X/Factor)*i,0),((Y/Factor)*i,FinalIMSize),\
					(RGB[0],RGB[1],RGB[2]),0.5,1))
	                i += 1

	scene.add( SVGImage(int(FinalIMSize/10),int(FinalIMSize/10),\
			    O_Name+"_"+str(int(Factor*Factor))+\
			    "_windmapkey.svg") )
	scene.write_svg()

        return OutName

#------------------------------------------------------------------------------
def PlotWindMapKey(OutName,Size,AxisColour):

	OutName = OutName+"_windmapkey"
        scene = Scene(OutName,Size[0],Size[1])
        scene.add( DefineArrow( 7,7,0,5,(0,0,0) ) )

	scene.add( linearGradient("gradwhite2"+str(AxisColour[0]),\
		    0,100,0,0,(255,255,255),PS_Outputs.ColourConvert(AxisColour[0]) ))
	scene.add( linearGradient("gradwhite2"+str(AxisColour[1]),\
		   0,0,100,0,(255,255,255), PS_Outputs.ColourConvert(AxisColour[1]) ))
	scene.add( linearGradient("gradwhite2"+str(AxisColour[2]),\
		   0,0,0,100,(255,255,255), PS_Outputs.ColourConvert(AxisColour[2]) ))
	scene.add( linearGradient("gradwhite2"+str(AxisColour[3]),\
		   100,0,0,0,(255,255,255), PS_Outputs.ColourConvert(AxisColour[3]) ))
	
	Angle  = [315,45,225,135]
	CX     = Size[0]/2
	CY     = Size[1]/2
	Radius = (Size[0]/20)*9

	i = 0
	while i < len(Angle):
		gradient = ""
                if  ( Angle[i] >= 0   and Angle[i] < 45 ):
			gradient = "gradwhite2"+str(AxisColour[0])
                elif( Angle[i] >= 45  and Angle[i] < 135):
			gradient = "gradwhite2"+str(AxisColour[1])
                elif( Angle[i] >= 135 and Angle[i] < 225):
			gradient = "gradwhite2"+str(AxisColour[2])
                elif( Angle[i] >= 225 and Angle[i] < 315):
			gradient = "gradwhite2"+str(AxisColour[3])
                elif( Angle[i] >= 315 and Angle[i] <= 360):
			gradient = "gradwhite2"+str(AxisColour[0])

		(XE1,YE1) = PS_Maths.GetCircleEdgeCoords(CX,CY,Angle[i],
							 Radius)
		(XE2,YE2) = PS_Maths.GetCircleEdgeCoords(CX,CY,Angle[i]+90,\
							 Radius)
		(XE3,YE3) = PS_Maths.GetCircleEdgeCoords(CX,CY,Angle[i]+45,\
							 (Radius/3)*2)
		scene.add( Path( ("M"+str(CX)+","+str(CY)+" "+\
				  "L"+str(XE1)+","+str(YE1)+" "+\
				  "A"+str(Radius)+","+str(Radius)+" 0 0,1 "+\
				  str(XE2)+","+str(YE2)+" z"),gradient,1))
		scene.add( ArrowLine( (CX,CY),(XE3,YE3),(0,0,0),2))
		i += 1

	scene.write_svg()

        return OutName

#------------------------------------------------------------------------------
def PlotKymoWeighted (OutName,KWMeanL,KWMeanR,KWVarL,KWVarR,KymographImage,\
		      PixelRatio,OutDir):

        OutName   = OutName+"_weightedMean"
	im        = Image.open(KymographImage).convert("RGBA")

	scene     = Scene(OutDir+"/"+OutName,int(im.size[1]),int(im.size[0]))
        scene.add( SVGImage(im.size[0],im.size[1],KymographImage) )
	scene.add(Line((im.size[0]/2,0),(im.size[0]/2,im.size[1]),(255,255,255),0.5,0.25))

	i = 0
        while i < len(KWMeanL):
		y = i + 0
		VarL      = ((KWVarL[i][1]/PixelRatio)/2.0)
		KWMeanL_N = (im.size[0]/2)-(KWMeanL[i]/PixelRatio)
		scene.add(Line(((KWMeanL_N - VarL),y),\
			       ((KWMeanL_N + VarL),y),\
			       (0,255,0),0.5,0.75))

		VarR      = ((KWVarR[i][1]/PixelRatio)/2.0)
		KWMeanR_N = (im.size[0]/2)+(KWMeanR[i]/PixelRatio)
		scene.add(Line(((KWMeanR_N - VarR),y),\
                               ((KWMeanR_N + VarR),y),\
                               (255,0,0),0.5,0.5))

                scene.add(Circle(((im.size[0]/2)-(KWMeanL[i]/PixelRatio),y),0.5,0,0,(255,0,0),0.95))
                scene.add(Circle(((KWMeanR[i]/PixelRatio)+(im.size[0]/2),y),0.5,0,0,(0,255,0),0.95))
                i += 1

        scene.write_svg()	

	return OutName

#------------------------------------------------------------------------------
def PlotKymoWeightedAll (OutName,KWMeanLAll,KWMeanRAll,Colours,ImageSizes):

        scene     = Scene(OutName,500,500)
        #scene.add(Line((250,0),(250,250),(255,255,255),0.5,0.25))

	scene.add(Line( (0,250),(500,250),(0,0,0),0.5,1) )

        i = 0
        while i < len(KWMeanLAll):
		RGB = PS_Outputs.ColourConvert(Colours[i])
		Scale = 3
		Corr = 250-((ImageSizes[i][0]/2.0)*Scale)

		scene.add( Rectangle((0,Corr),ImageSizes[i][0]*Scale,\
				     ImageSizes[i][1]*Scale,(RGB),0.1,(0,0,0),0 ) )
	
		j = 1
		while j < len(KWMeanLAll[i]):
			scene.add(Line(((j-1)*Scale,(KWMeanLAll[i][j-1]*Scale)+Corr),\
					(j*Scale,(KWMeanLAll[i][j]*Scale)+Corr),(RGB),0.5,1))
                        scene.add(Line(((j-1)*Scale,(KWMeanRAll[i][j-1]*Scale)+Corr),\
					(j*Scale,(KWMeanRAll[i][j]*Scale)+Corr),(RGB),0.5,1))
			j += 1
                i += 1

        scene.write_svg()       

        return OutName

#------------------------------------------------------------------------------
def PlotKymoWeightedAllExcel (OutName,KWMeanLAll,KWMeanRAll,Colours,\
			      ImageSizes,PixelRatios,TimeIntervals,\
			      Selection,OutDir):

	#Colours = [["green","darkgreen"],  ["steelblue","blue"],
        #           ["salmon","red"],["orchid","darkviolet"]]
	
	Colours = [["green","darkgreen"],["salmon","red"], 
		   ["steelblue","blue"], ["orchid","darkviolet"],
                   ["grey","black"],     ["orange","yellow"]]
	Colours = Colours * 10

        scene = Scene(OutDir+"/"+OutName,500,500)
        scene.add(Line( (45,250),(250,250),(0,0,0),0.5,1) )
	scene.add(Line( (45,10),(45,490),(0,0,0),0.5,1) )

	ArrayL_Big = []
	ArrayR_Big = []

	MaxDist  = 0
	MaxScale = 0
	cnt = 0
	ii = 0
	while ii < len(KWMeanLAll):
		#RGB = PS_Outputs.ColourConvert(Colours[cnt][0])
		ArrayL_Med = []
		ArrayR_Med = []
        	i = 0
        	while i < len(KWMeanLAll[ii]):
			ArrayL = []
			ArrayR = []
			PR = 1 #float(PixelRatios[ii][i])
                        TI = TimeIntervals[ii][i]

	                Scale = 0.4
			Scale2 = 20
			#Corr  = 250-(((ImageSizes[ii][i][0]*float(PixelRatios[ii][i]))/2.0)*Scale2)
			Corr  = 250 #(((ImageSizes[ii][i][0]*float(PixelRatios[ii][i]))/2.0)*Scale2)-250
			# Corr adjusts for different image sizes

	                j = 1
	                while j < len(KWMeanLAll[ii][i]):
				#if MaxScale < (((KWMeanLAll[ii][i][j-1]*PR)*Scale2)+Corr):
				#	MaxScale = (((KWMeanLAll[ii][i][j-1]*PR)*Scale2)+Corr)	
				if MaxScale < (KWMeanLAll[ii][i][j-1]*Scale2):
                                        MaxScale = (KWMeanLAll[ii][i][j-1]*Scale2)

				#if MaxDist < KWMeanLAll[ii][i][j-1]*PR*Scale2:
				#	MaxDist = KWMeanLAll[ii][i][j-1]*PR*Scale2
				#if MaxDist < KWMeanRAll[ii][i][j-1]*PR*Scale2:
                                #        MaxDist = KWMeanRAll[ii][i][j-1]*PR*Scale2

				if MaxDist < KWMeanLAll[ii][i][j-1]:
                                        MaxDist = KWMeanLAll[ii][i][j-1]
                                #if MaxDist < KWMeanRAll[ii][i][j-1]:
                                #        MaxDist = KWMeanRAll[ii][i][j-1]


				if ii in Selection:
					#RGB = PS_Outputs.ColourConvert(Colours[ii][0])
					RGB = PS_Outputs.ColourConvert(Colours[Selection.index(ii)][0])
					if KWMeanLAll[ii][i][j] != 0:
			                        scene.add(Line(((j-1)*TI*Scale+50,\
							      (((KWMeanLAll[ii][i][j-1]*PR)*Scale2)+Corr)),\
			                                      (j*TI*Scale+50,\
							      (((KWMeanLAll[ii][i][j]*PR)*Scale2)+Corr)),\
							      (RGB),0.5,0.5))
						ArrayL.append( (((KWMeanLAll[ii][i][j-1]*PR)*Scale2)+Corr))  
					if KWMeanRAll[ii][i][j] != 0:
			                        scene.add(Line(((j-1)*TI*Scale+50,\
							       (Corr-((KWMeanRAll[ii][i][j-1]*PR)*Scale2))),\
		        	                               (j*TI*Scale+50,\
							       (Corr-((KWMeanRAll[ii][i][j]*PR)*Scale2))),\
							       (RGB),0.5,0.5))
						ArrayR.append( (Corr-((KWMeanRAll[ii][i][j-1]*PR)*Scale2)))
        	                j += 1
			
			ArrayL_Med.append( ArrayL )
			ArrayR_Med.append( ArrayR )
                	i += 1
		cnt += 1
		ArrayL_Big.append( ArrayL_Med )
		ArrayR_Big.append( ArrayR_Med )
		ii += 1

	#Add the trend lines
	KWMeanAveL = PS_Maths.KymoWeightedMeanAverager(ArrayL_Big)
        KWMeanAveR = PS_Maths.KymoWeightedMeanAverager(ArrayR_Big)

	i = 0
	cnt = 0
        while i < len(KWMeanAveL):
		RGB = PS_Outputs.ColourConvert(Colours[cnt][1])
		if i in Selection:
			j = 1
			while j < len(KWMeanAveL[i]):
				scene.add(Line(((j-1)*5*Scale+50,\
                                              KWMeanAveL[i][j-1]),\
                                              (j*5*Scale+50,KWMeanAveL[i][j]),\
                                              (RGB),0.5,2))		
				j += 1
			j = 1
                        while j < len(KWMeanAveR[i]):
                                scene.add(Line(((j-1)*5*Scale+50,\
                                              KWMeanAveR[i][j-1]),\
                                              (j*5*Scale+50,KWMeanAveR[i][j]),\
                                              (RGB),0.5,2))
                                j += 1
			cnt += 1
		i += 1

	# X AXIS
	i   = 0
	cnt = 0
	while i < 50:
		if (TimeIntervals[0][0]*i) % 30 == 0: #label each 30 second point
			scene.add( Line( ((i*TimeIntervals[0][0]*Scale)+50,248),\
                                  	 ((i*TimeIntervals[0][0]*Scale)+50,252),\
                                 	 (0,0,0),0.5,1 ))                
			scene.add(Text(((i*TimeIntervals[0][0]*Scale)+50,257),\
                                     ("%d"%(TimeIntervals[0][0]*i)),5,\
                                     (0,0,0),0,(0,0,0),0))
		i += 1

	#Y AXIS
	try:
		Ratio = MaxDist/MaxScale
	except ZeroDivisionError:
		Ratio = 1
	Step = round(MaxDist,-1) / 10.0
	i = 1
        while i < 11:
		#Top section of graph
                scene.add( Line( (43,(250-(i*(Step/Ratio)))),\
                                 (47,(250-(i*(Step/Ratio)))),\
                                 (0,0,0),0.5,1 ))
		scene.add(Text((35,250-(i*(Step/Ratio))),("%.0f"%((Step*i)/1)),\
			  8,(0,0,0),0,(0,0,0),0))

		#Bottom Section of graph
		scene.add( Line( (43,(250+(i*(Step/Ratio)))),\
                                 (47,(250+(i*(Step/Ratio)))),\
                                 (0,0,0),0.5,1 ))
		scene.add(Text((35,250+(i*(Step/Ratio))),("%.0f"%((Step*i/1))),\
			  8,(0,0,0),0,(0,0,0),0))
                i += 1

        scene.write_svg()

        return OutName

#------------------------------------------------------------------------------
def PlotKymoSpeeds (OutName,KWMeanL,KWMeanR,KWSpeeds,KymographImage,PixelRatio,OutDir):

        OutName   = OutName+"_kymospeeds"
        im        = Image.open(KymographImage).convert("RGBA")

        scene     = Scene(OutDir+"/"+OutName,int(im.size[1]),int(im.size[0]))
        scene.add( SVGImage(im.size[0],im.size[1],KymographImage) )
        scene.add(Line((im.size[0]/2,0),(im.size[0]/2,im.size[1]),(255,255,255),0.5,0.25))

	i = 0
        while i < len(KWMeanL):
                y = i + 0

		if i >= KWSpeeds[0][0][1] and i <= KWSpeeds[0][0][3]:
	                scene.add(Circle(((im.size[0]/2)-(KWMeanL[i]/PixelRatio),y),0.5,0,0,(0,255,0),0.99))
        	        scene.add(Circle(((KWMeanR[i]/PixelRatio)+(im.size[0]/2),y),0.5,0,0,(255,0,0),0.99))
		else:
			scene.add(Circle(((im.size[0]/2)-(KWMeanL[i]/PixelRatio),y),0.5,0,0,(0,255,0),0.5))
                        scene.add(Circle(((KWMeanR[i]/PixelRatio)+(im.size[0]/2),y),0.5,0,0,(255,0,0),0.5))

                i += 1


	#scene.add(Line(((im.size[0]/2)-(KWSpeeds[0][0][0]/PixelRatio),\
	#		KWSpeeds[0][0][1]),\
	#	       ((KWSpeeds[0][0][2]/PixelRatio)-(im.size[0]/2),\
	#		KWSpeeds[0][0][3]),\
	#	       (0,255,0),0.95,0.5) )

	scene.add(Line((((im.size[0]/2)-(KWSpeeds[0][0][0]/PixelRatio)),KWSpeeds[0][0][1]),\
                       (((im.size[0]/2)-(KWSpeeds[0][0][2]/PixelRatio)),KWSpeeds[0][0][3]),\
                       (0,255,0),0.95,0.5) )

	scene.add(Line((((im.size[0]/2)+(KWSpeeds[0][1][0]/PixelRatio)),KWSpeeds[0][1][1]),\
                       (((im.size[0]/2)+(KWSpeeds[0][1][2]/PixelRatio)),KWSpeeds[0][1][3]),\
                       (255,0,0),0.95,0.5) )

	scene.add(Text((10,10),("%.2f"%KWSpeeds[1]),\
		  8,(0,0,0),0,(0,255,0),0))
	scene.add(Text(( im.size[0]-10,10),("%.2f"%KWSpeeds[2]),\
		  8,(0,0,0),0,(255,0,0),0))

        scene.write_svg()

        return OutName


#------------------------------------------------------------------------------
def PlotRadialHistogram ( OutName,TrailVectors,FinalIMSize,AxisColour ):

	OutName = OutName+"_radialhistogram_1"
	scene = Scene(OutName,FinalIMSize,FinalIMSize)
	scene.add( DefineArrow( 7,7,0,5,(0,0,0) ) )

	scene.add( linearGradient("gradwhite2"+str(AxisColour[0]),\
                   0,100,0,0,(255,255,255),PS_Outputs.ColourConvert(AxisColour[0]) ))
        scene.add( linearGradient("gradwhite2"+str(AxisColour[1]),\
                   0,0,100,0,(255,255,255), PS_Outputs.ColourConvert(AxisColour[1]) ))
        scene.add( linearGradient("gradwhite2"+str(AxisColour[2]),\
                   0,0,0,100,(255,255,255), PS_Outputs.ColourConvert(AxisColour[2]) ))
        scene.add( linearGradient("gradwhite2"+str(AxisColour[3]),\
                   100,0,0,0,(255,255,255), PS_Outputs.ColourConvert(AxisColour[3]) ))

	Angle  = [315,45,225,135]
        CX     = 256
        CY     = 256
        Radius = 150
        i = 0
        while i < len(Angle):
		gradient = ""
                if  ( Angle[i] >= 0   and Angle[i] < 45 ):
                        gradient = "gradwhite2"+str(AxisColour[0])
                elif( Angle[i] >= 45  and Angle[i] < 135):
                        gradient = "gradwhite2"+str(AxisColour[1])
                elif( Angle[i] >= 135 and Angle[i] < 225):
                        gradient = "gradwhite2"+str(AxisColour[2])
                elif( Angle[i] >= 225 and Angle[i] < 315):
                        gradient = "gradwhite2"+str(AxisColour[3])
                elif( Angle[i] >= 315 and Angle[i] <= 360):
                        gradient = "gradwhite2"+str(AxisColour[0])

                (XE1,YE1) = PS_Maths.GetCircleEdgeCoords(CX,CY,Angle[i],
                                                         Radius)
                (XE2,YE2) = PS_Maths.GetCircleEdgeCoords(CX,CY,Angle[i]+90,\
                                                         Radius)
                (XE3,YE3) = PS_Maths.GetCircleEdgeCoords(CX,CY,Angle[i]+45,\
                                                         (Radius/3)*2)
                scene.add( Path( ("M"+str(CX)+","+str(CY)+" "+\
                                  "L"+str(XE1)+","+str(YE1)+" "+\
                                  "A"+str(Radius)+","+str(Radius)+" 0 0,1 "+\
                                  str(XE2)+","+str(YE2)+" z"),gradient,1))
                scene.add( ArrowLine( (CX,CY),(XE3,YE3),(0,0,0),2))
		i += 1
	
	scene.add(Text((256-5,256-200-20),"D",20,(0,0,0),0,(0,0,0)))
        scene.add(Text((256-5,256+200+25),"V",20,(0,0,0),0,(0,0,0)))
        scene.add(Text((256-200-30,256),"A",20,(0,0,0),0,(0,0,0)))
        scene.add(Text((256+200+25,256),"P",20,(0,0,0),0,(0,0,0)))	

	#ADD ACTUAL DATA
	Angle     = []
	Magnitude = []
	i = 0
        while i < len(TrailVectors):
		Angle.append( int(PS_Maths.CalculateVectorAngle( TrailVectors[i] ) ) )
		Magnitude.append( PS_Maths.CalculateVectorMagnitude( TrailVectors[i] ) )
		i += 1

	j = 0
	while j < 360:
		Stack = 155
		i = 0
        	while i < len(TrailVectors):
			if(Angle[i] == j):
				Magnitude[i] = Magnitude[i] / max(Magnitude)
				X,Y = PS_Maths.GetCircleEdgeCoords( 256,256,Angle[i],Stack )
				scene.add(Circle((X,Y),(2.5),0,0,(0,0,0),0.5))
				Stack += (5 + (Magnitude[i]*10))
			i += 1
		j += 1


	scene.write_svg()
	ImageName = OutName

	return ImageName

#------------------------------------------------------------------------------
def PlotRoseDiagram ( OutName,Label,TrailVectors,Mag,StepAng,FinalIMSize,\
		      AxisColour,ScalePie,AxisLabels ):

        OutName = OutName+Label #"_rosediagram_wmag"
        scene = Scene(OutName,FinalIMSize,FinalIMSize)
        scene.add( DefineArrow( 7,7,0,5,(0,0,0) ) )
        scene.add( linearGradient("gradwhite2"+str(AxisColour[0]),\
                   0,100,0,0,(255,255,255),PS_Outputs.ColourConvert(AxisColour[0]) ))
        scene.add( linearGradient("gradwhite2"+str(AxisColour[1]),\
                   0,0,100,0,(255,255,255), PS_Outputs.ColourConvert(AxisColour[1]) ))
        scene.add( linearGradient("gradwhite2"+str(AxisColour[2]),\
                   0,0,0,100,(255,255,255), PS_Outputs.ColourConvert(AxisColour[2]) ))
        scene.add( linearGradient("gradwhite2"+str(AxisColour[3]),\
                   100,0,0,0,(255,255,255), PS_Outputs.ColourConvert(AxisColour[3]) ))

	Step   = StepAng
        CX     = 256
        CY     = 256
        Radius = 150

        scene.add(Circle((CX,CY),50,1,0.5,(0,0,0),0))
        scene.add(Circle((CX,CY),100,1,0.5,(0,0,0),0))
        scene.add(Circle((CX,CY),150,1,0.5,(0,0,0),0))
        scene.add(Circle((CX,CY),200,1,0.5,(0,0,0),0))

	Angle = [] 
	Magnitude = []
	i = 0
	while i < 360: 
		Magnitude.append( 0 )
		Angle.append(float("%.6f"%i))
		i += Step

	i = 0
        while i < len(TrailVectors):
		Ang = PS_Maths.CalculateVectorAngle( TrailVectors[i] )

		j = 0
		while j < len(Angle):

			if( Ang >= Angle[j] and Ang < (Angle[j]+Step) ):
                                if(Mag == 1):
                                        Magnitude[j] += PS_Maths.CalculateVectorMagnitude(TrailVectors[i])
                                else:
                                        Magnitude[j] += 1.0
				next
			j += 1
		i += 1

        i = 0
        while i < len(Angle):
		try:
			Radius = 2 * (100 * (Magnitude[i] / sum(Magnitude)))
			ScaleFactor = (100 * (max(Magnitude) / sum(Magnitude)))
			Scale       = 1		

			if(ScalePie):
				#Scale = int(  100 / ScaleFactor )
				Scale = 3

			Radius = Radius * Scale

		except ZeroDivisionError:
			Radius = 0

		gradient = ""
                if  ( Angle[i] >= 0   and Angle[i] < 45 ):
                        gradient = "gradwhite2"+str(AxisColour[0])
                elif( Angle[i] >= 45  and Angle[i] < 135):
                        gradient = "gradwhite2"+str(AxisColour[1])
                elif( Angle[i] >= 135 and Angle[i] < 225):
                        gradient = "gradwhite2"+str(AxisColour[2])
                elif( Angle[i] >= 225 and Angle[i] < 315):
                        gradient = "gradwhite2"+str(AxisColour[3])
                elif( Angle[i] >= 315 and Angle[i] <= 360):
                        gradient = "gradwhite2"+str(AxisColour[0])

		if (StepAng > 45) and (Angle[i] < 180):
			gradient = "gradwhite2"+str(AxisColour[1])
		elif (StepAng > 45) and (Angle[i] >= 180):
                        gradient = "gradwhite2"+str(AxisColour[3])


                (XE1,YE1) = PS_Maths.GetCircleEdgeCoords(CX,CY,Angle[i],
                                                         Radius)
                (XE2,YE2) = PS_Maths.GetCircleEdgeCoords(CX,CY,Angle[i]+Step,\
                                                         Radius)
                (XE3,YE3) = PS_Maths.GetCircleEdgeCoords(CX,CY,Angle[i]+(Step/2),\
                                                         (Radius/3)*2)
                scene.add( Path( ("M"+str(CX)+","+str(CY)+" "+\
                                  "L"+str(XE1)+","+str(YE1)+" "+\
                                  "A"+str(Radius)+","+str(Radius)+" 0 0,1 "+\
                                  str(XE2)+","+str(YE2)+" z"),gradient,1))
                i += 1

	#ADD ACTUAL DATA
        Angle     = []
        i = 0
        while i < len(TrailVectors):
                #Angle.append( int(PS_Maths.CalculateVectorAngle(TrailVectors[i])+0.00001) )
		Angle.append( int(PS_Maths.CalculateVectorAngle(TrailVectors[i])) )
                i += 1
        j = 0
        while j < 360:
                Stack = 202 
                i = 0
                while i < len(TrailVectors):
                        if(Angle[i] == j):
                                X,Y = PS_Maths.GetCircleEdgeCoords( 256,256,Angle[i],Stack )
                                scene.add(Circle((X,Y),2,0,0,(0,0,0),0.75))
                                Stack += 3
                        i += 1
                j += 1

	if StepAng == 180:
		Left =  ("%.2f"%(100*(Magnitude[1]/sum(Magnitude) ) ) ) 
		scene.add(Text((256-156,490),str(Left)+"%",50,(0,0,0),0,(0,0,0),0))

		Right = ("%.2f"%(100*(Magnitude[0]/sum(Magnitude) ) ) )
                scene.add(Text((256+150,490),str(Right)+"%",50,(0,0,0),0,(0,0,0),0))

	#else:
	scene.add(Text((256-50-5,256),  str(round(25/Scale, 1))+"%", 10,(0,0,0),0,(0,0,0),0))
	scene.add(Text((256-100-10,256),str(round(50/Scale, 1))+"%",10,(0,0,0),0,(0,0,0),0))
	scene.add(Text((256-150-10,256),str(round(75/Scale, 1))+"%",10,(0,0,0),0,(0,0,0),0))
	scene.add(Text((256-200-10,256),str(round(100/Scale,1))+"%",10,(0,0,0),0,(0,0,0),0))

	#Add the labels for the axes
        scene.add(Text((256,256-200-20),AxisLabels[0],20,(0,0,0),0,(0,0,0),0))
        scene.add(Text((256,256+200+25),AxisLabels[1],20,(0,0,0),0,(0,0,0),0))
        scene.add(Text((256-200-30,256),AxisLabels[2],20,(0,0,0),0,(0,0,0),0))
        scene.add(Text((256+200+25,256),AxisLabels[3],20,(0,0,0),0,(0,0,0),0))

        scene.write_svg()
        ImageName = OutName

        return ImageName

#------------------------------------------------------------------------------
def PlotRoseDiagram2 ( OutName,TrailVectors,FinalIMSize,AxisColour ):

        OutName = OutName+"_rosediagram_nomag"
        scene = Scene(OutName,FinalIMSize,FinalIMSize)
        scene.add( DefineArrow( 7,7,0,5,(0,0,0) ) )
        scene.add( linearGradient("gradwhite2"+str(AxisColour[0]),\
                   0,100,0,0,(255,255,255),PS_Outputs.ColourConvert(AxisColour[0]) ))
        scene.add( linearGradient("gradwhite2"+str(AxisColour[1]),\
                   0,0,100,0,(255,255,255), PS_Outputs.ColourConvert(AxisColour[1]) ))
        scene.add( linearGradient("gradwhite2"+str(AxisColour[2]),\
                   0,0,0,100,(255,255,255), PS_Outputs.ColourConvert(AxisColour[2]) ))
        scene.add( linearGradient("gradwhite2"+str(AxisColour[3]),\
                   100,0,0,0,(255,255,255), PS_Outputs.ColourConvert(AxisColour[3]) ))

        Step   = 15
        CX     = 256
        CY     = 256
        Radius = 150

        scene.add(Circle((CX,CY),50,1,0.5,(0,0,0),0))
        scene.add(Circle((CX,CY),100,1,0.5,(0,0,0),0))
        scene.add(Circle((CX,CY),150,1,0.5,(0,0,0),0))
        scene.add(Circle((CX,CY),200,1,0.5,(0,0,0),0))

        Angle  = []
        Magnitude = []
        i = 0
        while i <= 360:
                Angle.append( i )
                Magnitude.append( 0 )
                i += Step

        i = 0
        while i < (len(Angle)-1):
                j = 0
                while j < len(TrailVectors):
                        Ang = PS_Maths.CalculateVectorAngle( TrailVectors[j] )

                        if( Ang >= Angle[i] and Ang < Angle[i+1] ):
                                Magnitude[i] += 1.0 
                                                
                        j += 1
                i += 1

        i = 0
        while i < len(Angle):
                #Radius = randint(10,200)
                Radius = 200 * (Magnitude[i] / max(Magnitude))
		#print Magnitude[i], max(Magnitude), (Magnitude[i] / max(Magnitude))

                gradient = ""
                if  ( Angle[i] >= 0   and Angle[i] < 45 ):
                        gradient = "gradwhite2"+str(AxisColour[0])
                elif( Angle[i] >= 45  and Angle[i] < 135):
                        gradient = "gradwhite2"+str(AxisColour[1])
                elif( Angle[i] >= 135 and Angle[i] < 225):
                        gradient = "gradwhite2"+str(AxisColour[2])
                elif( Angle[i] >= 225 and Angle[i] < 315):
                        gradient = "gradwhite2"+str(AxisColour[3])
                elif( Angle[i] >= 315 and Angle[i] <= 360):
                        gradient = "gradwhite2"+str(AxisColour[0])

                (XE1,YE1) = PS_Maths.GetCircleEdgeCoords(CX,CY,Angle[i],
                                                         Radius)
                (XE2,YE2) = PS_Maths.GetCircleEdgeCoords(CX,CY,Angle[i]+Step,\
                                                         Radius)
                (XE3,YE3) = PS_Maths.GetCircleEdgeCoords(CX,CY,Angle[i]+(Step/2),\
                                                         (Radius/3)*2)
                scene.add( Path( ("M"+str(CX)+","+str(CY)+" "+\
                                  "L"+str(XE1)+","+str(YE1)+" "+\
                                  "A"+str(Radius)+","+str(Radius)+" 0 0,1 "+\
                                  str(XE2)+","+str(YE2)+" z"),gradient,1))
                i += 1

        #ADD ACTUAL DATA
        Angle     = []
        i = 0
        while i < len(TrailVectors):
                Angle.append( int(PS_Maths.CalculateVectorAngle( TrailVectors[i] ) ) )
                i += 1
        j = 0
        while j < 360:
                Stack = 202
                i = 0
                while i < len(TrailVectors):
                        if(Angle[i] == j):
                                X,Y = PS_Maths.GetCircleEdgeCoords( 256,256,Angle[i],Stack )
                                scene.add(Circle((X,Y),2,0,0,(0,0,0),0.75))
                                Stack += 3
                        i += 1
                j += 1

        scene.add(Text((256-50-5,256),  "25%", 12,(0,0,0),0,(0,0,0),0))
        scene.add(Text((256-100-10,256),"50%",12,(0,0,0),0,(0,0,0),0))
        scene.add(Text((256-150-10,256),"75%",12,(0,0,0),0,(0,0,0),0))
        scene.add(Text((256-200-10,256),"100%",12,(0,0,0),0,(0,0,0),0))

        scene.add(Text((256,256-200-20),"D",20,(0,0,0),0,(0,0,0),0))
        scene.add(Text((256,256+200+25),"V",20,(0,0,0),0,(0,0,0),0))
        scene.add(Text((256-200-30,256),"A",20,(0,0,0),0,(0,0,0),0))
        scene.add(Text((256+200+25,256),"P",20,(0,0,0),0,(0,0,0),0))

        scene.write_svg()
        ImageName = OutName

        return ImageName

#------------------------------------------------------------------------------
def PlotCompareRoseDiagram ( Runs,FinalIMSize,CoordsSet,Sheet,DirGraphs ):

	AxisColour = ["red","blue","purple","cyan"]
	AxisColour = ["red","blue","red","blue"]

	if Sheet == 99:
		OutName = "Compare_"+str(CoordsSet)+"_All_comprosediagram"
	else:
		OutName = "Compare_"+str(CoordsSet)+"_"+str(Sheet)+"_comprosediagram"

        scene = Scene(DirGraphs+"/"+OutName,FinalIMSize,FinalIMSize)
        scene.add( DefineArrow( 7,7,0,5,(0,0,0) ) )
        scene.add( linearGradient("gradwhite2"+str(AxisColour[0]),\
                   0,100,0,0,(255,255,255),PS_Outputs.ColourConvert(AxisColour[0]) ))
        scene.add( linearGradient("gradwhite2"+str(AxisColour[1]),\
                   0,0,100,0,(255,255,255), PS_Outputs.ColourConvert(AxisColour[1]) ))
        scene.add( linearGradient("gradwhite2"+str(AxisColour[2]),\
                   0,0,0,100,(255,255,255), PS_Outputs.ColourConvert(AxisColour[2]) ))
        scene.add( linearGradient("gradwhite2"+str(AxisColour[3]),\
                   100,0,0,0,(255,255,255), PS_Outputs.ColourConvert(AxisColour[3]) ))

        Step   = 15
        CX     = 256
        CY     = 256
        Radius = 150

        scene.add(Circle((CX,CY),50,1,0.5,(0,0,0),0))
        scene.add(Circle((CX,CY),100,1,0.5,(0,0,0),0))
        scene.add(Circle((CX,CY),150,1,0.5,(0,0,0),0))
        scene.add(Circle((CX,CY),200,1,0.5,(0,0,0),0))

        Angle  = []
        Magnitude = []
        i = 0
        while i <= 360:
                Angle.append( i )
                Magnitude.append( 0 )
                i += Step

	Ang = []
	Dis = []
	j = 0
	while j < len(Runs):
		k = 0
                while k < len(Runs[j]['Runs']):
			if Runs[j]['Runs'][k][2] != 0 and Runs[j]['CoordsSet'] == CoordsSet:
				Ang.append(Runs[j]['Runs'][k][6])
				Dis.append(Runs[j]['Runs'][k][3])
			k += 1
		j += 1

        i = 0
        while i < (len(Angle)-1):
                j = 0
                while j < len(Ang):
                        if( Ang[j] >= Angle[i] and Ang[j] < Angle[i+1] ):
				#No magnitude
                                #Magnitude[i] += 1.0
				#With run length as magnitude
				Magnitude[i] += Dis[j]
                        j += 1
                i += 1

	i = 0
        while i < len(Angle):
		if max(Magnitude) != 0:
	                Radius = 200 * (Magnitude[i] / max(Magnitude))
	                gradient = ""
	                if  ( Angle[i] >= 0   and Angle[i] < 45 ):
	                        gradient = "gradwhite2"+str(AxisColour[0])
	                elif( Angle[i] >= 45  and Angle[i] < 135):
	                        gradient = "gradwhite2"+str(AxisColour[1])
	                elif( Angle[i] >= 135 and Angle[i] < 225):
	                        gradient = "gradwhite2"+str(AxisColour[2])
	                elif( Angle[i] >= 225 and Angle[i] < 315):
	                        gradient = "gradwhite2"+str(AxisColour[3])
	                elif( Angle[i] >= 315 and Angle[i] <= 360):
	                        gradient = "gradwhite2"+str(AxisColour[0])
	
	                (XE1,YE1) = PS_Maths.GetCircleEdgeCoords(CX,CY,Angle[i],
	                                                         Radius)
	                (XE2,YE2) = PS_Maths.GetCircleEdgeCoords(CX,CY,Angle[i]+Step,\
	                                                         Radius)
	                (XE3,YE3) = PS_Maths.GetCircleEdgeCoords(CX,CY,Angle[i]+(Step/2),\
	                                                         (Radius/3)*2)
	                scene.add( Path( ("M"+str(CX)+","+str(CY)+" "+\
	                                  "L"+str(XE1)+","+str(YE1)+" "+\
	                                  "A"+str(Radius)+","+str(Radius)+" 0 0,1 "+\
	                                  str(XE2)+","+str(YE2)+" z"),gradient,1))
                i += 1

        #ADD ACTUAL DATA
        j = 0
        while j < 360:
                Stack = 202
                i = 0
                while i < len(Ang):
                        if(int(Ang[i]) == j):
                                X,Y = PS_Maths.GetCircleEdgeCoords( 256,256,int(Ang[i]),Stack )
                                scene.add(Circle((X,Y),2,0,0,(0,0,0),0.75))
                                Stack += 3
                        i += 1
                j += 1

        scene.add(Text((256-50-5,256),  "25%", 12,(0,0,0),0,(0,0,0),0))
        scene.add(Text((256-100-10,256),"50%",12,(0,0,0),0,(0,0,0),0))
        scene.add(Text((256-150-10,256),"75%",12,(0,0,0),0,(0,0,0),0))
        scene.add(Text((256-200-10,256),"100%",12,(0,0,0),0,(0,0,0),0))

        scene.add(Text((256,256-200-20),"0",20,(0,0,0),0,(0,0,0),0))
        scene.add(Text((256,256+200+25),"180",20,(0,0,0),0,(0,0,0),0))
        scene.add(Text((256-200-30,256),"270",20,(0,0,0),0,(0,0,0),0))
        scene.add(Text((256+200+25,256),"90",20,(0,0,0),0,(0,0,0),0))

        scene.write_svg()
        ImageName = OutName

        return ImageName

#------------------------------------------------------------------------------
def PlotDirectionTable ( TrailVectors ):

	Table = 0

	Step = 45
	Angle  = []
	Directionality = []
        i = 0
        while i < 360:
                Angle.append( i )
		Directionality.append( 0 )
                i += Step

	i = 0
        while i < len(Angle):
                j = 0
                while j < len(TrailVectors):
                        Ang = PS_Maths.CalculateVectorAngle( TrailVectors[j] )

                        if( Ang >= Angle[i] and Ang < (Angle[i]+Step) ):
                                Directionality[i] += 1
                        j += 1
                i += 1	

	print "+------------+-------------------+"
	i = 0
        while i < len(Angle):
		DirPercent = 100*(float(Directionality[i])/float(sum(Directionality)))
                print "| %3d to %3d | %6.2f%s (%3d/%3d) |"%(Angle[i], Angle[i]+Step,\
							   DirPercent,"%",Directionality[i],\
							   sum(Directionality))
                i += 1
	print "+------------+-------------------+"
	i = 0
        while i < len(Angle):
		DirPercent = 100*(float(Directionality[i]+Directionality[i+1])/float(sum(Directionality)))
		print "| %3d to %3d | %6.2f%s (%3d/%3d) |"%(Angle[i], Angle[i]+(2*Step),\
							    DirPercent, "%", \
							    Directionality[i]+Directionality[i+1],\
							    sum(Directionality))
		i += 2
	print "+------------+-------------------+"

	i = 0
        while i < len(Angle):
                DirPercent = 100*(float(Directionality[i]+Directionality[i+1]+\
			     Directionality[i+2]+Directionality[i+3])/float(sum(Directionality)))
                print "| %3d to %3d | %6.2f%s (%3d/%3d) |"%(Angle[i], Angle[i]+(4*Step),\
                                                            DirPercent, "%", \
                                                            Directionality[i]+Directionality[i+1]+\
							    Directionality[i+2]+Directionality[i+3],\
                                                            sum(Directionality))
                i += 4
        print "+------------+-------------------+"
	print "| 315 to  45 | %6.2f%s (%3d/%3d) |"%(100*(float(Directionality[-1]+Directionality[0])/\
						   float(sum(Directionality))),\
						   "%",Directionality[-1]+Directionality[0],\
                                                   sum(Directionality))
        print "|  45 to 135 | %6.2f%s (%3d/%3d) |"%(100*(float(Directionality[1]+Directionality[2])/\
						   float(sum(Directionality))),\
                                                   "%",Directionality[1]+Directionality[2],\
                                                   sum(Directionality)) 
        print "| 135 to 225 | %6.2f%s (%3d/%3d) |"%(100*(float(Directionality[3]+Directionality[4])/\
                                                   float(sum(Directionality))),\
                                                   "%",Directionality[3]+Directionality[4],\
                                                   sum(Directionality))
        print "| 225 to 315 | %6.2f%s (%3d/%3d) |"%(100*(float(Directionality[5]+Directionality[6])/\
                                                   float(sum(Directionality))),\
                                                   "%",Directionality[5]+Directionality[6],\
                                                   sum(Directionality))
	print "+------------+-------------------+"

	return Table


#------------------------------------------------------------------------------
def PlotVertDirectionTable ( TrailVectors ):

        Table = 0

        Step = 45
        Angle  = []
        Directionality = []
        i = 0
        while i < 360:
                Angle.append( i )
                Directionality.append( 0 )
                i += Step

        i = 0
        while i < len(Angle):
                j = 0
                while j < len(TrailVectors):
                        Ang = PS_Maths.CalculateVectorAngle( TrailVectors[j] )

                        if( Ang >= Angle[i] and Ang < (Angle[i]+Step) ):
                                Directionality[i] += 1
                        j += 1
                i += 1

        print "+------------+-------------------+"
        i = 0
        while i < len(Angle):
                DirPercent = 100*(float(Directionality[i])/float(sum(Directionality)))
                print "| %3d to %3d | %6.2f%s (%3d/%3d) |"%(Angle[i], Angle[i]+Step,\
                                                           DirPercent,"%",Directionality[i],\
                                                           sum(Directionality))
                i += 1
        print "+------------+-------------------+"
        i = 0
        while i < len(Angle):
                DirPercent = 100*(float(Directionality[i]+Directionality[i+1])/float(sum(Directionality)))
                print "| %3d to %3d | %6.2f%s (%3d/%3d) |"%(Angle[i], Angle[i]+(2*Step),\
                                                            DirPercent, "%", \
                                                            Directionality[i]+Directionality[i+1],\
                                                            sum(Directionality))
                i += 2
        print "+------------+-------------------+"

        i = 0
        while i < len(Angle):
                DirPercent = 100*(float(Directionality[i]+Directionality[i+1]+\
                             Directionality[i+2]+Directionality[i+3])/float(sum(Directionality)))
                print "| %3d to %3d | %6.2f%s (%3d/%3d) |"%(Angle[i], Angle[i]+(4*Step),\
                                                            DirPercent, "%", \
                                                            Directionality[i]+Directionality[i+1]+\
                                                            Directionality[i+2]+Directionality[i+3],\
                                                            sum(Directionality))
                i += 4
        print "+------------+-------------------+"
        print "| 315 to  45 | %6.2f%s (%3d/%3d) |"%(100*(float(Directionality[-1]+Directionality[0])/\
                                                   float(sum(Directionality))),\
                                                   "%",Directionality[-1]+Directionality[0],\
                                                   sum(Directionality))
        print "|  45 to 135 | %6.2f%s (%3d/%3d) |"%(100*(float(Directionality[1]+Directionality[2])/\
                                                   float(sum(Directionality))),\
                                                   "%",Directionality[1]+Directionality[2],\
                                                   sum(Directionality))
        print "| 135 to 225 | %6.2f%s (%3d/%3d) |"%(100*(float(Directionality[3]+Directionality[4])/\
                                                   float(sum(Directionality))),\
                                                   "%",Directionality[3]+Directionality[4],\
                                                   sum(Directionality))
        print "| 225 to 315 | %6.2f%s (%3d/%3d) |"%(100*(float(Directionality[5]+Directionality[6])/\
                                                   float(sum(Directionality))),\
                                                   "%",Directionality[5]+Directionality[6],\
                                                   sum(Directionality))
        print "+------------+-------------------+"

        print "| 270 to 90 | %6.2f%s (%3d/%3d) |"%(100*(float(Directionality[-2]+Directionality[-1]+Directionality[0]+Directionality[1])/\
                                                   float(sum(Directionality))),\
                                                   "%",Directionality[-2]+Directionality[-1]+Directionality[0]+Directionality[1],\
                                                   sum(Directionality))
	print "| 90 to 270 | %6.2f%s (%3d/%3d) |"%(100*(float(Directionality[2]+Directionality[3]+Directionality[4]+Directionality[5])/\
                                                   float(sum(Directionality))),\
                                                   "%",Directionality[2]+Directionality[3]+Directionality[4]+Directionality[5],\
                                                   sum(Directionality))

        print "+------------+-------------------+"

	return Table

#------------------------------------------------------------------------------
def PlotKymoSpeedCompare (AveSpeeds,SheetNames,FullColours,OutDir):

	SheetNames = ["A","B","C","D","E","F"]
	FullColours = [["darkgreen","green"], ["red","salmon"], ["blue","steelblue"],
                      ["darkviolet","orchid"], ["grey","black"],["orange","yellow"]]

	#del AveSpeeds[-1]

	params = {'axes.labelsize':16,'text.fontsize':16,\
                  'xtick.labelsize':8,'ytick.labelsize':2}

	x_coords = arange( len(AveSpeeds))
	Speeds   = []
	StdDev   = []
	StdErr   = []
	Colours  = []
        i = 0
        while i < len(AveSpeeds):
		Colours.append(FullColours[i][0])
		stddev,stderr = PS_Maths.Standard_Dev_Error(AveSpeeds[i])
		StdDev.append( float(stddev) )
		StdErr.append( float(stderr) )
		Ave = 0
		j = 0
		while j < len(AveSpeeds[i]):
			Ave += AveSpeeds[i][j]                          
               		j += 1 
		Speeds.append( float(Ave/len(AveSpeeds[i])) )
                i += 1

        figure()
	p = bar(x_coords+0.1,Speeds, align='center', color=Colours, yerr=StdDev, ecolor="black")

        xticks(arange(len(AveSpeeds))+0.1,SheetNames)
        #ylabel('Speeds xxx/sec')
        title_text = 'Speed Comparisons'
        title(title_text)

	savefig(OutDir+"/"+"kymo_SpeedCompare.png")
	savefig(OutDir+"/"+"kymo_SpeedCompare.svg")

	return "kymo_SpeedCompare"

#------------------------------------------------------------------------------
def PlotSpeedVsTime (Coordinates,FrameRate):

	i = 1
	Speed = []
	Time = []
	while i < len(Coordinates):
		Speed.append (  ParticleStats_Maths.Calculate2PointSpeed(
				Coordinates[i-1][2],Coordinates[i-1][3],\
				Coordinates[i][2],Coordinates[i][3],FrameRate) ) 
		Time.append(i)
		i += 1
	figure()
	bar(Time,Speed,1,color='y')

	xlabel('time (s)')
	ylabel('pixels (px)')
	title_text = 'Speed Vs Time (Assumes ' + str(FrameRate) + ' frames per sec)'
	title(title_text)
	grid(True)
	savefig('GraphOutput/Speed.png')

#------------------------------------------------------------------------------
def PlotDisplacementSquaredVsTime (Coordinates,PixelRatio):

        i = 1
        Displacement = []
        Time = []
        while i < len(Coordinates):
		Displacement.append ( pow(ParticleStats_Maths.Calculate2PointsDistance(
					Coordinates[0][4],Coordinates[0][5],\
					Coordinates[i][4],Coordinates[i][5],PixelRatio),2) )
                Time.append(i)
                i += 1
	figure()
        bar(Time,Displacement,1,color='g')

        xlabel('time (s)')
        ylabel('displacement^2 (pixels)')
        title('Particle Displacement Squared Vs Time')
        grid(True)
        savefig('GraphOutput/DisplacementSquaredVsTime.png')

#------------------------------------------------------------------------------
def PlotDisplacementVsTime (Coordinates,PixelRatio):

        i = 1
        Displacement = []
        Time = []
        while i < len(Coordinates):
                Displacement.append (ParticleStats_Maths.Calculate2PointsDistance(
                                Coordinates[0][2],Coordinates[0][3],\
                                Coordinates[i][2],Coordinates[i][3],PixelRatio))
                Time.append(i)
                i += 1
	figure()
        bar(Time,Displacement,1,color='g')

        xlabel('time (s)')
        ylabel('pixels (px)')
        title('Particle Displacement Vs Time')
        grid(True)
        savefig('GraphOutput/DisplacementVsTime.png')

#------------------------------------------------------------------------------
def PlotDisplacementVsTimeRunsNPauses (Coordinates,PixelRatio,Runs,Pauses):

	figure()
        i            = 1
        while i < len(Coordinates):
		Colour = 'silver'
                Displacement = (ParticleStats_Maths.Calculate2PointsDeltaY(
                                Coordinates[0][3], Coordinates[i][3],PixelRatio))

		j = 0
		while j < len(Runs):
			if (i >= Runs[j][0] and i <= Runs[j][1] and Runs[j][2] > 0):
				Colour = 'r'
			elif (i >= Runs[j][0] and i <= Runs[j][1] and Runs[j][2] < 0):
				Colour = 'b'
			j += 1

		k = 0
                while k < len(Pauses):
                        if (i >= Pauses[k][0] and i <= Pauses[k][1]):
                                Colour = 'purple'
                        k += 1

		bar(i,Displacement,1,color=Colour)
                i += 1
		 
        xlabel('time (s)')
        ylabel('pixels (px)')
        title('Particle Displacement (Delta Y) Vs Time')
        grid(True)
        savefig('GraphOutput/DisplacementVsTimeRunsNPauses.png')

#------------------------------------------------------------------------------
def PlotDistanceVsTimeRunsNPauses (Coordinates,PixelRatio,Runs,Pauses):

        figure()
        i            = 1
        while i < len(Coordinates):
                Colour = 'silver'
		Distance = (ParticleStats_Maths.Calculate2PointsDeltaY(
                                Coordinates[i-1][3], Coordinates[i][3],PixelRatio))

                j = 0
                while j < len(Runs):
                        if (i >= Runs[j][0] and i <= Runs[j][1] and Runs[j][2] > 0):
                                Colour = 'r'
			elif (i >= Runs[j][0] and i <= Runs[j][1] and Runs[j][2] < 0):
                                Colour = 'b'
                        j += 1

                k = 0
#                while k < len(Pauses):
#                        if (i >= Pauses[k][0] and i <= Pauses[k][1]):
#                                Colour = 'purple'
#                        k += 1

                bar(i,Distance,1,color=Colour)
                i += 1

        xlabel('time (s)')
        ylabel('pixels (px)')
        title('Particle Distance (Delta Y) Vs Time')
        grid(True)
        savefig('GraphOutput/DistanceVsTimeRunsNPauses.png')

#------------------------------------------------------------------------------
def PlotRuns (Runs,PixelRatio,Colours,Name,DirGraphs):

        figure()
        params = {'axes.labelsize':2,'text.fontsize':2,\
                  'xtick.labelsize':8,'ytick.labelsize':2}
	x = []
	y = []
        RunCounter = 0
        i = 0
        while i < len(Runs):
                j = 0
                while j < len(Runs[i]):
                        if( Runs[i][j][2] == -1 ) and (Runs[i][j][3] != 0):
                                x.append( RunCounter)
                                y.append( Runs[i][j][3] )
				RunCounter += 1
                        elif( Runs[i][j][2] ==  1 ) and (Runs[i][j][3] != 0):
                                x.append( RunCounter);
                                y.append( Runs[i][j][3] )
				RunCounter += 1
                        j += 1
		i += 1

	y.sort()
	pylab.bar(x, y, 1, color='green' )

        yticklabels = getp(gca(), 'yticklabels')
        setp(yticklabels, 'color', 'black', fontsize=14)
        xticklabels = getp(gca(), 'xticklabels')
        setp(xticklabels, 'color', 'black', fontsize=14)

        xlabel('Runs')
        ylabel('Run Lengths (nm)')
        title('Run Lengths')

        savefig(DirGraphs+'/RunsLengths_'+Name+'.png',dpi=100)
	savefig(DirGraphs+'/RunsLengths_'+Name+'.svg',dpi=350)
	del(Runs)

#------------------------------------------------------------------------------
def PlotTrailMagnitudes( OutName, TrailVectors, pixStep, AxisLabels ):

	# Create histogram of magnitudes of trails for the ROI
	figure()
        params = {'axes.labelsize':2,'text.fontsize':2,\
                  'xtick.labelsize':8,'ytick.labelsize':2}
        x = []; y = []
	y_N = []; y_E = []; y_S = [];  y_W = [];

        i = 0
        while i < len(TrailVectors):
		Ang = PS_Maths.CalculateVectorAngle( TrailVectors[i] )
		Mag = PS_Maths.CalculateVectorMagnitude( TrailVectors[i] )

		x.append( i )
		y.append( Mag )

		if Ang > 315 and Ang <= 360:
			y_N.append( Mag )
		elif Ang >= 0 and Ang <= 45:
                        y_N.append( Mag )
		elif Ang > 45 and Ang <= 135:
			y_E.append( Mag )
		elif Ang > 135 and Ang <= 225:
			y_S.append( Mag )
		elif Ang > 225 and Ang <= 315:
			y_W.append( Mag )
                i += 1

	yAll = [y,y_N,y_E,y_S,y_W]
	angRanges = [ '0-360','315-45','45-135','135-225','225-315']
	binsize = 15
	pixBins = []
	binNo = 1+(int(max(y) / pixStep ))
	xLab = []; xAxis = []; FreqsAll = [];
	maxFreq = 0

	i = 0
        while i < binNo:
		lab = "%.0f-%.0f"%( i*pixStep,(i*pixStep)+pixStep)
		xLab.append( lab ) 
		xAxis.append(i)
		i += 1

	i = 0
	while i < len(yAll):

#np.zeros((5,), dtype=numpy.int)

		Freqs = na.zeros(binNo,dtype=na.int)
		j = 0
		while j < len(yAll[i]):
			c = 0; k = 0
			while k < int(max(y)):
				if yAll[i][j] >= k and yAll[i][j] < k+pixStep: 
					Freqs[c] += 1
				c += 1
				k += pixStep		
			j += 1

		FreqsAll.append( Freqs )
		if max(Freqs) > maxFreq: maxFreq = max(Freqs)
		i += 1

	AxisLabels2 = [AxisLabels[0],AxisLabels[3],AxisLabels[1],AxisLabels[2]]

	i = 0
        while i < len(FreqsAll):
		figure ()
		pylab.bar(xAxis,FreqsAll[i], 1, color='green' )
		plt.xticks( arange(binNo),(xLab), rotation=45,fontsize='small' )
	        xlabel('Trails Magnitudes')
	        ylabel('Frequency')
		axis([0, binNo, 0, maxFreq ])

		if i > 0:
			dirlab = AxisLabels2[i-1]
		else:
			dirlab = "all"
		

	        title('Trail Magnitude Frequency Plot (angles '+angRanges[i]+' direction='+dirlab+')')
	        savefig(OutName+'_trailmagnitudes_angleset_'+angRanges[i]+'.png',dpi=100)
	        savefig(OutName+'_trailmagnitudes_angleset_'+angRanges[i]+'.svg',dpi=350)
		i += 1

	print " + Frequency Data for magnitude distributions"
	print "+-------+--------+--------+--------+--------+--------+"
	print "| ang   |",
	j = 0
	while j < len(angRanges):
		print "%7s|"%angRanges[j], 
		j += 1
	print 
	print "| dir   | %7s| %7s| %7s| %7s| %7s|"%("all",AxisLabels[0],AxisLabels[3],\
					       AxisLabels[1],AxisLabels[2])
	print "+-------+--------+--------+--------+--------+--------+"
	j = 0
        while j < len(FreqsAll[0]):
		print "|%7s|"%xLab[j],
		k = 0
		while k < len(angRanges):
               		print "%7d|"%FreqsAll[k][j],
			k += 1
                j += 1
		print
	print "+-------+--------+--------+--------+--------+--------+"

#------------------------------------------------------------------------------
def PlotRunsFreq (Runs,Colours,Name,DirGraphs):

        figure()
	params = {'axes.labelsize':2,'text.fontsize':2,\
		  'xtick.labelsize':8,'ytick.labelsize':2}
	x = []
	y = []
	RunCounter = 0
	i = 0	
	while i < len(Runs):
		j = 0
		while j < len(Runs[i]):
			if( Runs[i][j][2] == -1 ):  
				x.append( RunCounter)
				y.append( Runs[i][j][3] )
			elif( Runs[i][j][2] ==  1 ):  
				x.append( RunCounter); 
				y.append( Runs[i][j][3] )

			RunCounter += 1
			j += 1
		i += 1

	ys = na.sort(y)

	i = 0
	factor = 20
	freq = zeros( (int(ys[-1]/factor)+1)  ) 

	xs = []
        i = 0
        while i < len(freq):
                xs.append((i*factor))
                j = 0
                while j < len(ys):
                        if( ys[j] >= (i*factor) and ys[j] < (i*factor)+factor ):
                                freq[i] += 1
                        j += 1
                i += 1

	pylab.bar(xs, freq, color='white' )

	polycoeffs = polyfit(xs, freq, 10)
	yfit = scipy.polyval(polycoeffs, xs)
	pylab.plot(xs, yfit, 'r-')

	yticklabels = getp(gca(), 'yticklabels')
	setp(yticklabels, 'color', 'black', fontsize=14)
	xticklabels = getp(gca(), 'xticklabels')
        setp(xticklabels, 'color', 'black', fontsize=14)

        xlabel('Run Lengths')
        ylabel('Freq')
        title('Frequency Distribution of Run Lengths')

        savefig(DirGraphs+'/DeltaYRunsFreq_'+Name+'.png',dpi=100)
	savefig(DirGraphs+'/DeltaYRunsFreq_'+Name+'.svg',dpi=350)

#------------------------------------------------------------------------------
def PlotDirChangeResults(Changes,CoordSet,DirGraphs):

        figure()
        params = {'axes.labelsize':2,'text.fontsize':2,\
                  'xtick.labelsize':8,'ytick.labelsize':2}

        ys     = na.sort(Changes)
        factor = 1 #max(ys)/20.0
        freq   = zeros( (int(ys[-1]/factor)+1)  )

        xs = []
        i = 0
        while i < len(freq):
                xs.append((i*factor))
                j = 0
                while j < len(ys):
                        if( ys[j] >= (i*factor) and ys[j] < (i*factor)+factor ):
                                freq[i] += 1
                        j += 1
                i += 1

	summy = sum(freq)
	i = 0
        while i < len(freq):
		freq[i] = (freq[i] / summy ) * 100
		i += 1

        pylab.bar(xs, freq, 0.25, align='center', color='green' )

        #polycoeffs = polyfit(xs, freq, 10)
        #yfit = scipy.polyval(polycoeffs, xs)
        #pylab.plot(xs, yfit, 'r-')

        yticklabels = getp(gca(), 'yticklabels')
        setp(yticklabels, 'color', 'black', fontsize=14)
        xticklabels = getp(gca(), 'xticklabels')
        setp(xticklabels, 'color', 'black', fontsize=14)

        xlabel('Direction Changes')
        ylabel('Freq')
        title('Frequency Distribution of Direction Changes Coords='+str(CoordSet))

        #axis([0, (len(xs)+1), 0, 100])
	#axis([0, (len(xs)+1), 0, 50])
        savefig(DirGraphs+'/DirChangesFreq_'+str(CoordSet)+'.png',dpi=100)
        savefig(DirGraphs+'/DirChangesFreq_'+str(CoordSet)+'.svg',dpi=350)

        return "DirChangesFreq_"+str(CoordSet)

#------------------------------------------------------------------------------
def PlotTrailSpeeds(OutName,TrailVectors,TrailNoPoints,TimeInt):

        figure()
        params = {'axes.labelsize':2,'text.fontsize':2,\
                  'xtick.labelsize':8,'ytick.labelsize':2}

	t = []
	d = []
	s = []

	i = 0
	while i < len(TrailVectors):
		t.append( TrailNoPoints[i]*TimeInt )
		d.append( PS_Maths.CalculateVectorMagnitude(TrailVectors[i]) )
		s.append( d[-1]/t[-1] )
		#print "--------", t[-1], d[-1], s[-1]
		i += 1
	
        ss = na.sort(s)
	AveSpd = float( sum(ss) ) / len(ss)

	pylab.hist(ss,bins=20)

        yticklabels = getp(gca(), 'yticklabels')
        setp(yticklabels, 'color', 'black', fontsize=14)
        xticklabels = getp(gca(), 'xticklabels')
        setp(xticklabels, 'color', 'black', fontsize=14)
        xlabel('Run Speeds')
        ylabel('Freq')
        title('Frequency Distribution of Trail Speeds')
        savefig(OutName+'_trailspeeds.png',dpi=100)
        savefig(OutName+'_trailspeeds.svg',dpi=350)

        return(OutName+"_trailspeeds",AveSpd)

#------------------------------------------------------------------------------
def PlotThreeFrameResults(Runs,CoordSet,DirGraphs):

        figure()
        params = {'axes.labelsize':2,'text.fontsize':2,\
                  'xtick.labelsize':8,'ytick.labelsize':2}

        y = []
        i = 0
        while i < len(Runs):
		if(Runs[i][0] == CoordSet):
        	        y.append( Runs[i][4] )
                i += 1

        ys     = na.sort(y)
        factor = 0.5 #max(ys)/20.0
        freq   = zeros( int(int(ys[-1]/factor)+1)  )

	xs = []
	i = 0
	while i < len(freq):
		xs.append((i*factor))
                j = 0
                while j < len(ys):
                        if( ys[j] >= (i*factor) and ys[j] < (i*factor)+factor ):
                                freq[i] += 1
                        j += 1
                i += 1

	summy = sum(freq)
	i = 0
        while i < len(freq):
                freq[i] = ((freq[i] / summy) * 100)
                i += 1

        pylab.bar(xs, freq, 0.25, align='center', color='green' )

        polycoeffs = polyfit(xs, freq, 10)
        yfit = scipy.polyval(polycoeffs, xs)
        pylab.plot(xs, yfit, 'r-')

        yticklabels = getp(gca(), 'yticklabels')
        setp(yticklabels, 'color', 'black', fontsize=14)
        xticklabels = getp(gca(), 'xticklabels')
        setp(xticklabels, 'color', 'black', fontsize=14)

        xlabel('Run Speeds')
        ylabel('Freq')
        title('Frequency Distribution of Run Speeds Coords='+str(CoordSet))

        #axis([0, 25, 0, 100])
	#axis([0, 25, 0, 50])

        savefig(DirGraphs+'/ThreeRunsFreq_'+str(CoordSet)+'.png',dpi=100)
        savefig(DirGraphs+'/ThreeRunsFreq_'+str(CoordSet)+'.svg',dpi=350)

	return "ThreeRunsFreq_"+str(CoordSet)

#------------------------------------------------------------------------------
def PlotThreeFrameMaxResults(Runs,CoordSet,DirGraphs):

        figure()
        params = {'axes.labelsize':2,'text.fontsize':2,\
                  'xtick.labelsize':8,'ytick.labelsize':2}

        y = []
        i = 0
        while i < len(Runs):
                if(Runs[i][0] == CoordSet):
                        y.append( Runs[i][4] )
                i += 1

        ys     = na.sort(y)
        factor = 0.5 #max(ys)/20.0
        freq   = zeros( (int(ys[-1]/factor)+1)  )

        xs = []
        i = 0
        while i < len(freq):
                xs.append((i*factor))
                j = 0
                while j < len(ys):
                        if( ys[j] >= (i*factor) and ys[j] < (i*factor)+factor ):
                                freq[i] += 1
                        j += 1
                i += 1

        summy = sum(freq)
        i = 0
        while i < len(freq):
                freq[i] = ((freq[i] / summy) * 100)
                i += 1

        pylab.bar(xs, freq, 0.25, align='center', color='green' )

        polycoeffs = polyfit(xs, freq, 10)
        yfit = scipy.polyval(polycoeffs, xs)
        pylab.plot(xs, yfit, 'r-')

        yticklabels = getp(gca(), 'yticklabels')
        setp(yticklabels, 'color', 'black', fontsize=14)
        xticklabels = getp(gca(), 'xticklabels')
        setp(xticklabels, 'color', 'black', fontsize=14)

        xlabel('Max Run Speeds')
        ylabel('Freq')
        title('Frequency Distribution of Max Run Speeds Coords='+str(CoordSet))

        #axis([0, 25, 0, 100])
	#axis([0, 25, 0, 50])
        savefig(DirGraphs+'/ThreeRunsMaxFreq_'+str(CoordSet)+'.png',dpi=100)
        savefig(DirGraphs+'/ThreeRunsMaxFreq_'+str(CoordSet)+'.svg',dpi=350)

	return "ThreeRunsMaxFreq_"+str(CoordSet)	

#------------------------------------------------------------------------------
def PlotDistanceVsTimeCummulative(Coords,Sheet,Num,Name,TimeUnits,DistanceUnits,\
				  DirGraphs):

	figure()
	params = { 'axes.labelsize':2,'text.fontsize':2,\
                   'xtick.labelsize': 8,'ytick.labelsize': 2}

        Distance = 0
	Dist     = []
        Time     = []
        j        = 1
        Timey   = 0
        while j < len(Coords):
		Distance += abs(PS_Maths.Calculate2PointsDistance(\
                                        Coords[j-1][4],Coords[j-1][5],\
					Coords[j][4],Coords[j][5]))
		Timey += Coords[j][2]
		Dist.append(Distance)
		Time.append(Timey)
                j += 1

	plot(Time,Dist,'r-',Time,Dist,'b+')

        xlabel(("Time in ("+str(TimeUnits)+")") )
        ylabel(("Cummulative Distance Y ("+str(DistanceUnits)+")"))
	title("Cummulative Distance Vs Time for Particle "+str(Num)+" (Frames="+str(j)+")")

	GraphName = 'DistanceVsTime_'+Name+'_st_'+str(Sheet)+'_tr_'+str(Num)
        savefig((DirGraphs+"/"+GraphName+'.png'),dpi=75)
	savefig((DirGraphs+"/"+GraphName+'.svg'),dpi=350)
	del(Coords)
	return GraphName

#------------------------------------------------------------------------------
def PlotDeltaYVsTime (Coords,Name,TimeUnits,DistanceUnits):

	i = 0
	while i < len(Coords):
		figure()
	        params = { 'axes.labelsize':2,'text.fontsize':2,\
			   'xtick.labelsize': 8,'ytick.labelsize': 2}

                Distance = []
                Time     = []
		j        = 1
		DeltaY   = 0
		while j < len(Coords[i]):

			Distance.append ( PS_Maths.Calculate2PointsDeltaY(\
                                    Coords[i][j-1][2], Coords[i][j][2]))

			DeltaY += Coords[i][j][3]

			Time.append(DeltaY)

			j += 1

		plot(Time,Distance)

		xlabel('Time in (msec)')
        	ylabel('Delta Y (nm)')
        	title('Delta Y Vs Time for Particle '+str(i)+' (Frames='+str(j)+')')

        	savefig('GraphOutput/DeltaYVsTime_'+Name+'_Particle_'+str(i)+'.png',dpi=75)
#		savefig('GraphOutput/DeltaYVsTime_'+Name+'_Particle_'+str(i)+'.svg',dpi=350)

                i += 1

#------------------------------------------------------------------------------
def RegressionGraph(Coords,Name,Sheet,Num,Regression,Axes,Runs,DirGraphs):

	figure()
        params = { 'axes.labelsize':2, 'text.fontsize': 2,\
                   'xtick.labelsize':8,'ytick.labelsize': 2}

	X  = []
	Y  = []
	Y2 = []
	i = 0
	while i < len(Coords):
		X.append(Coords[i][4])
		Y.append(Coords[i][5])
		if Axes[0] == 99:
			Y2.append( (Coords[i][4]*Regression['X'])+(Regression['Intercept'])  )
		i += 1

	plot(X,Y,'k:',label="X and Y",linewidth=1)

	#Plot on the Runs and Pauses
	i = 0
	while i < len(Runs):
		Xr = []
		Yr = []
		
		j = int(Runs[i][0])
		while j <= int(Runs[i][1]):
			Xr.append(Coords[j][4])
			Yr.append(Coords[j][5])
			j += 1

		if int(Runs[i][2]) == 1:
			plot(Xr,Yr,'g-',label="+Run   ",linewidth=2 )
			plot([Xr[0]],[Yr[0]]) #PUTS A STAR AT START OF RUN
		elif int(Runs[i][2]) == -1:
			plot(Xr,Yr,'b-',label="-Run   ",linewidth=2 )
                        plot([Xr[0]],[Yr[0]]) 
		else:
			plot(Xr,Yr,'r-',label="Pause  ",linewidth=2 )
		i += 1
	if Axes[0] == 99 and Axes[2] == 99:
		plot(X, Y2,c='gray',ls='-',label='r2 = '+str( ('%.2f'%Regression['R2']) ) )

	elif Axes[0] == 100 and Axes[2] == 120:
		plot([Axes[0],Axes[1]],[Axes[2],Axes[3]],c='gray',ls='-',label='axis')

	elif Axes[0] != 99:
                i = 0
                while i < len(Axes):
                        if Coords[0][0] == Axes[i][0]:
                                break
                        i += 1
		plot([Axes[i][1],Axes[i][3]],[Axes[i][2],Axes[i][4]],c='gray',ls='-',label='axis')

	text(X[0],Y[0],'start',color='black',fontsize='small')
	text(X[len(X)-1],Y[len(Y)-1],'end',  color='black',  fontsize='small')

	legend(markerscale=0.005,borderpad=0.15)
        leg = gca().get_legend()
        ltext  = leg.get_texts()
        leg.draw_frame(False)
        setp(ltext, fontsize='smaller')

	ax = axis() 
	xlocs,xlabs = xticks()

	xlabsNEW = []
	i=0
	while i < len(xlabs):
		t = i
		xlocs = "%s"%xlocs
		xlabsNEW.append( xlabs[i] )
		i += 1

	axis('equal')
	axy = gca()

	xlabel('X')
        ylabel('Y')
        title('CoordSet='+str(Name)+' Sheet='+str(Sheet)+' Particle '+str(Num))

	GraphName = ("Regression_Coords"+str(Name)+"_st_"+str(Sheet)+"_tr_"+str(Num))

        savefig(DirGraphs+'/'+str(GraphName)+'.png',dpi=75)
	savefig(DirGraphs+'/'+str(GraphName)+'.svg',dpi=75)

	return GraphName

#------------------------------------------------------------------------------
def PlotAveRunLength (GlobalDist):

	figure()

	y_coords   = [ abs(float(GlobalDist[0][0])),abs(float(GlobalDist[0][1])),\
        	       abs(float(GlobalDist[1][0])),abs(float(GlobalDist[1][1])) ]
	x_coords   = arange(4)
	err_coords = [ float(GlobalDist[0][2]),float(GlobalDist[0][3]),\
                       float(GlobalDist[1][2]),float(GlobalDist[1][3]) ]
	colours = ["orange","g","orange","g"]

	p = bar(x_coords+0.8,y_coords, color=colours, yerr=err_coords)

	xticks(arange(4)+1.7,('Coords 1','','Coords 2',''))
	legend( (p[0],p[1]), ('+ve Runs', '-ve Runs'))
	xlabel('Comparison of two input files')
        ylabel('Delta Y (nm)')
	savefig('GraphOutput/CompDistance.png',dpi=100)
	#savefig('GraphOutput/CompDistance.svg',dpi=350)


#------------------------------------------------------------------------------
def PlotSpeed (GlobalSpeed):

        figure()

        y_coords   = [ abs(float(GlobalSpeed[0][0])),abs(float(GlobalSpeed[0][1])),\
                       abs(float(GlobalSpeed[1][0])),abs(float(GlobalSpeed[1][1])) ]
        x_coords   = arange(4)
        err_coords = [ float(GlobalSpeed[0][2]),float(GlobalSpeed[0][3]),\
                       float(GlobalSpeed[1][2]),float(GlobalSpeed[1][3]) ]
        colours = ["orange","g","orange","g"]

        p = bar(x_coords+0.8,y_coords, color=colours, yerr=err_coords)

        xticks(arange(4)+1.7,('Coords 1','','Coords 2',''))
        legend( (p[0],p[1]), ('+ve Runs', '-ve Runs'))
	xlabel('Comparison of two input files')
        ylabel('Speed ms/nm')
        savefig('GraphOutput/CompSpeed.png',dpi=100)
	#savefig('GraphOutput/CompSpeed.svg',dpi=350)

#------------------------------------------------------------------------------
# SVG DEFINITIONS
#------------------------------------------------------------------------------

class Scene:
    def __init__(self,name="svg",height=800,width=800):

        self.name = name
        self.items = []
        self.height = height
        self.width = width
        return

    def add(self,item): self.items.append(item)

    def strarray(self):

        var = ["<?xml version=\"1.0\" standalone='no'?> \n",

	       "<!DOCTYPE svg PUBLIC \"-//W3C//DTD SVG 1.0//EN\" ",
	       "\"http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd\">\n",


               "<svg xmlns=\"http://www.w3.org/2000/svg\" ",
	       "xmlns:xlink=\"http://www.w3.org/1999/xlink\" ",
	       "height=\"%dpx\" width=\"%dpx\" viewBox='0 0 %dpx %dpx'> \n" \
		% (self.height,self.width,self.width,self.height) ]

	#Add any defs here
	PatternDef  = re.compile(r'<defs')
	for item in self.items: 
		if PatternDef.search( str(item.strarray()) ):
			var += item.strarray()

	var += [" <g style=\"fill-opacity:1.0; stroke:black;",
               " stroke-width:1;\">\n"]

        for item in self.items:
		if not PatternDef.search( str(item.strarray()) ):
			var += item.strarray()

        var += [" </g>\n</svg>\n"]
	#var += ["</svg>\n"]

        return var

    def write_svg(self,filename=None):
        if filename:
            self.svgname = filename
        else:
            self.svgname = self.name + ".svg"
        file = open(self.svgname,'w')
        file.writelines(self.strarray())
        file.close()
        return

class DefineArrow:
    def __init__(self,height,width,refx,refy,stroke):
        self.height  = height 
        self.width   = width
	self.refx    = refx
	self.refy    = refy
        self.stroke  = stroke
        return

    def strarray(self):
	return ["<defs>\n<marker id='Arrow' orient='auto' markerHeight='%d' markerWidth='%d' markerUnits='userSpaceOnUse' refX='%d' refY='%d' viewBox='0 0 10 10'>\n<polyline stroke='rgb%s' fill='rgb%s' points='0,0 9,5 0,9 0,0'/>\n</marker>\n </defs>\n"%(self.height,self.width,self.refx,self.refy,self.stroke,self.stroke) ]

class linearGradient:
    def __init__(self,name,gradX1,gradY1,gradX2,gradY2,startcol,endcol):
        self.name     = name
	self.gradX1   = gradX1
	self.gradY1   = gradY1
	self.gradX2   = gradX2
        self.gradY2   = gradY2
        self.startcol = startcol
        self.endcol   = endcol
        return

    def strarray(self):
        return ["<defs>\n<linearGradient id='%s' x1='%d%%' y1='%d%%' x2='%d%%' y2='%d%%' >\n<stop offset='0%%' style='stop-color:rgb%s;stop-opacity:0.50'/>\n<stop offset='100%%' style='stop-color:rgb%s;stop-opacity:1'/>\n</linearGradient></defs>\n"%(self.name,self.gradX1,self.gradY1,self.gradX2,self.gradY2,self.startcol,self.endcol) ]

class Line:
    def __init__(self,start,end,color,opacity,width):
        self.start   = start   #xy tuple
        self.end     = end     #xy tuple
	self.color   = color
	self.opacity = opacity
	self.width   = width
        return

    def strarray(self):
        return ["  <line x1=\"%d\" y1=\"%d\" x2=\"%d\" y2=\"%d\" style=\"stroke:rgb%s;stroke-opacity:%s;stroke-width:%f\" />\n" %\
           (self.start[0],self.start[1],self.end[0],self.end[1],self.color,self.opacity,self.width)]

class ArrowLine:
    def __init__(self,start,end,color,width):
        self.start = start   #xy tuple
        self.end   = end     #xy tuple
	self.color = color
	self.width = width
        return

    def strarray(self):
        return ["<line x1='%d' y1='%d' x2='%d' y2='%d' style='stroke:rgb%s;stroke-width:%d;stroke-opacity:1;' marker-end='url(#Arrow)' />\n" %\
                (self.start[0],self.start[1],self.end[0],self.end[1],self.color,self.width)]

class Path:
    def __init__(self,path,color,opacity):
        self.path  = path 

	#Adapted for putting in colour cgradients
        Pattrn  = re.compile(r'grad')
        if Pattrn.search( str(color) ):
                self.color = "url(#"+str(color)+")"
        else:
                self.color = "rgb"+str(color)

	self.opacity = opacity

        return

    def strarray(self):
	return ["<path d=\"%s\" style=\"fill:%s;fill-opacity:%s;stroke-width:1;\" />\n"\
	         %( self.path,self.color,self.opacity )]

class SVGImage:
    def __init__(self,width,height,image):
        self.image  = image
	self.width  = int(width)
	self.height = int(height)
        return
    def strarray(self):
        return ["  <image x=\"0\" y=\"0\" width=\"%d\" height=\"%d\" xlink:href=\"%s\" />\n" % (self.width,self.height,self.image) ]

class Circle:
    def __init__(self,center,radius,stroke,strokeopacity,color,opacity):
        self.center         = center #xy tuple
        self.radius         = radius #xy tuple
	#self.stroke         = stroke
	self.strokeopacity  = strokeopacity
	#Adapted for putting in colour cgradients
        Pattrn  = re.compile(r'grad')
        if Pattrn.search( str(color) ):
                self.color = "url(#"+str(color)+")"
		self.stroke = "url(#"+str(color)+")"
        else:
                self.color = "rgb"+str(color)
		self.stroke = "rgb"+str(color)

        #self.color   = color   
	self.opacity = opacity
        return

    def strarray(self):
        return ["  <circle cx=\"%d\" cy=\"%d\" r=\"%f\" " %\
                (self.center[0],self.center[1],self.radius),
                "style=\"stroke:%s;stroke-opacity:%.2f;fill:%s;fill-opacity:%.2f\"  />\n" % (self.stroke,self.strokeopacity,self.color,self.opacity)]

class Ellipse:
    def __init__(self,center,radius,stroke,strokeopacity,color):
        self.center = center #xy tuple
        self.radius = radius #xy tuple
	self.stroke = stroke
	self.strokeopacity = strokeopacity
        self.color  = color   #rgb tuple in range(0,256)
        return

    def strarray(self):
        return ["  <ellipse cx=\"%d\" cy=\"%d\" rx=\"%d\" ry=\"%d\" " %\
                (self.center[0],self.center[1],self.radius[0],self.radius[1]),\
                " style=\"fill:none;stroke:rgb%s;stroke-width:%d;stroke-opacity:%.2f \"/>\n"%(self.color,self.stroke,self.strokeopacity)]

class PolygonShape:
    def __init__(self,Points,Fill,FillOpacity,Stroke,StrokeOpacity,StrokeWidth):
	self.points        = Points
	self.fill          = Fill
	self.fillopacity   = FillOpacity
	self.stroke        = Stroke
	self.strokeopacity = StrokeOpacity
	self.strokewidth   = StrokeWidth
	return

    def strarray(self):
	return ["<polygon points=\"%s\" style=\"fill:rgb%s;fill-opacity:%s;stroke:rgb%s;stroke-opacity:%s;stroke-width:%s;stroke-dasharray: 9, 5;\" />" % (self.points,self.fill,self.fillopacity,self.stroke,self.strokeopacity,self.strokewidth)]

	# Polygon(polypoints,(255,0,0),0.50,(0,0,0),1,2) )

class Rectangle:
    def __init__(self,origin,height,width,color,opacity,strokecol,strokeopa):
        self.origin    = origin
        self.height    = height
        self.width     = width

	#Adapted for putting in colour cgradients
	Pattrn  = re.compile(r'grad')
	if Pattrn.search( str(color) ):
		self.color = "url(#"+str(color)+")"
        else:               
		self.color = "rgb"+str(color) 

	self.opacity   = opacity
	self.strokecol = strokecol
	self.strokeopa = strokeopa
        return

    def strarray(self):
        return ["  <rect x=\"%d\" y=\"%d\" height=\"%d\" " %\
                (self.origin[0],self.origin[1],self.height),
                "width=\"%d\" style=\"fill:%s;fill-opacity:%s;stroke:%s;stroke-opacity:%s; \" />\n" %\
                (self.width,self.color,self.opacity,self.strokecol,self.strokeopa)]

class Text:
    def __init__(self,origin,text,size,stroke,strokeopa,color,angle):
        self.origin    = origin
        self.text      = text
        self.size      = size
	self.stroke    = stroke
	self.strokeopa = strokeopa
	self.color     = color
	self.angle     = angle
        return

    def strarray(self):
        return ["  <text x=\"%d\" y=\"%d\" font-size=\"%d\" stroke=\"rgb%s\" stroke-opacity=\"%s\" stroke-width=\"0.5\" fill=\"rgb%s\" text-anchor=\"middle\" transform=\"rotate(%d)\">\n" %\
                (self.origin[0],self.origin[1],self.size,self.stroke,self.strokeopa,self.color,self.angle),
                "   %s\n" % self.text,
                "  </text>\n"]

#def colorstr(rgb): return "#%x%x%x" % (rgb[0]/16,rgb[1]/16,rgb[2]/16)

#------------------------------------------------------------------------------
# FIN
#------------------------------------------------------------------------------
