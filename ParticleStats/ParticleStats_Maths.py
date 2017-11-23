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

import numpy as na
import os,sys,math
from decimal import *
import random
#import Scientific.Statistics as SciPy
import scipy
#from Scientific.Geometry import Vector
#from Scientific.Geometry.VectorModule import Vector 
import ParticleStats_Outputs as PS_Outputs
#import rpy
#from rpy import r
from PIL import Image
import re
#r.library("circular")
#r.library("CircStats")
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr 
import rpy2.rpy_classic as rpy

#------------------------------------------------------------------------------
def geo_mean(iterable):
# Function to calculate the geometric mean of a set of points
# https://stackoverflow.com/questions/43099542/python-easy-way-to-do-geometric-mean-in-python
# Added: 12/10/17

	a = na.log(iterable)
	return na.exp(a.sum()/len(a))

#------------------------------------------------------------------------------
def roundNumber (number, roundTo, direction):
# Function rounds numbers (integers and floats) to the nearest entered number
# however has the added functionality of always rounding UP or DOWN rather than
# just to the nearest selected roundTo number
# Added: 15/01/09
	rounded = (round(number/roundTo))*roundTo

	if direction == "UP":
		rounded = rounded + roundTo
	elif direction == "DOWN":
		rounded = rounded - roundTo

	return rounded 
#------------------------------------------------------------------------------
def rotateXYbyAngAndOrigin(X,Y,Ang,OriginX,OriginY,Scale,Shift):

	#if Ang == 0:
	#	newX = X
	#	newY = Y
	if(OriginX == 0 and OriginY == 0):
    		newX = X * math.cos(math.radians(Ang)) \
			- math.sin(math.radians(Ang)) * Y
		newY = X * math.sin(math.radians(Ang)) \
			+ math.cos(math.radians(Ang)) * Y;
	else:
		newX = ((X - OriginX) * math.cos(math.radians(Ang)) )\
			 - ((Y - OriginY) * math.sin(math.radians(Ang))) + OriginX
		newY = ((X - OriginX) * math.sin(math.radians(Ang)) )\
			 + ((Y - OriginY) * math.cos(math.radians(Ang))) + OriginY;

	if(Shift[0] > 0):
                newX = newX + Shift[0]
        if(Shift[1] > 0):
                newY = newY + Shift[1]

	return newX,newY

#------------------------------------------------------------------------------
def GetCircleEdgeCoords(CX,CY,Angle,Radius):
# Function to give the coordinates of the edge of a circle given the origin,
# angle and ragius of the circle. Outputs a set of coordinates in X and Y

        if  (Angle > 0  ) and (Angle <= 90):
                AngleC = Angle
        elif(Angle > 90 ) and (Angle <= 180):
                AngleC = 180-Angle #Angle-90
        elif(Angle > 180) and (Angle <= 270):
                AngleC = Angle-180
        elif(Angle > 270) and (Angle < 360):
                AngleC = 360-Angle #Angle-270

        elif(Angle <= 0.0):
                AngleC = 360-Angle
        elif(Angle >= 360):
                AngleC = (Angle - 360)
                Angle  = AngleC

        RadiansAngle = (float(AngleC)/360) * 2 * math.pi
        OppSide      = math.sin(RadiansAngle) * Radius
        AdjSide      = math.sqrt( (Radius*Radius) - (OppSide*OppSide) )

        if (Angle <= 90):
                XE = CX+OppSide
                YE = CY-AdjSide
        elif(Angle > 90 ) and (Angle <= 180):
                XE = CX+OppSide
                YE = CY+AdjSide
        elif(Angle > 180) and (Angle <= 270):
                XE = CX-OppSide
                YE = CY+AdjSide
        elif(Angle > 270) and (Angle <= 360):
                XE = CX-abs(OppSide)
                YE = CY-abs(AdjSide)

        return XE, YE

#------------------------------------------------------------------------------
def ColourBasedOnAngleSelector(Angle,AxisCol):
# Function to create RGB colour based on an angle (90 degree colour segments) 
# Created 26/06/08

	#Angle     = CalculateVectorAngle(SquareBigVector)
	#Magnitude = CalculateVectorMagnitude(SquareBigVector) 
	#MagScale = ( float(175) / float(MagnitudeLongest) )
	#H = int(MagScale*Magnitude)
        #Scale = 0
        #Scale = ( float(255) / float(360) )

        R = 0
        G = 0
        B = 0

	PS_Outputs.ColourConvert(AxisCol[0])

        if  (Angle >= 0  ) and (Angle < 45 ):
		#G = 255
		#B = 255
		R,G,B = PS_Outputs.ColourConvert(AxisCol[0])
        elif(Angle >= 45 ) and (Angle < 135):
                #G = Scale*Angle
		#G = 255
		R,G,B = PS_Outputs.ColourConvert(AxisCol[1])
        elif(Angle >= 135) and (Angle < 225):
                #B = Angle
		#B = 255
		R,G,B = PS_Outputs.ColourConvert(AxisCol[2])
        elif(Angle >= 225) and (Angle < 315):
		#R = 255
		#B = 255
		R,G,B = PS_Outputs.ColourConvert(AxisCol[3])
	elif(Angle >= 315  ) and (Angle <= 360 ):
		#G = 255
		#B = 255
		R,G,B = PS_Outputs.ColourConvert(AxisCol[0])

        R = int(R)
        G = int(G)
        B = int(B)

        return R,G,B

#------------------------------------------------------------------------------
def CalculatePointInPolygon(point,polygonPoints):

	assert len(polygonPoints) >= 3

        x,y  = round(point[0],3), round(point[1],3)
        xp   = [round(p[0],3) for p in polygonPoints]
        yp   = [round(p[1],3) for p in polygonPoints]

        c    = False
        i    = 0
        npol = len(polygonPoints)
        j    = npol-1

        while i < npol:
                if ((((yp[i]<=y) and (y<yp[j])) or
                        ((yp[j]<=y) and(y<yp[i]))) and
                        (x < (xp[j]-xp[i]) * (y-yp[i]) / (yp[j]-yp[i])+xp[i])):
                        c = not c
                j = i
                i += 1
       
        return c

#------------------------------------------------------------------------------
def CalculateEquationOfLine(particle):
# Given a line in the forma of an array X1,Y1,X2,Y2 this function will output
# the equation of the line (y = mx + c) plus the changes in X and Y 
	dy = (particle[3]-particle[1])
        dx = (particle[2]-particle[0])

        if(dy == 0) and (dx == 0):
                tm = 0
        elif(dy == 0) and (dx != 0):
                tm = 0
        elif(dy != 0) and (dx == 0):
                tm = 0
		# WAS 1000!!!!!!!!!!!!!!!!!!!!!!!!!!!
        else:
                tm = dy / dx

        tc = (particle[3] - (tm*particle[2]))

	return dx,dy,tm,tc

#------------------------------------------------------------------------------
def SquareWithinROI(polygon,square):

        cross  = 0
	i = 0
	while i < len(square):
		x = square[i][0]
		y = square[i][1]
		if( CalculatePointInPolygon([x,y],polygon)):
			cross = 1
			#print "\t\t\tCROSS"
			break
		i += 1

	if cross == 0:
		x = int(square[0][0])
		while x <= int(square[1][0]):
			y = int(square[0][1])
			while y < int(square[2][1]):	
				if( CalculatePointInPolygon([x,y],polygon)):
                        		cross = 1
                        		#print "\t\t\tEXHAUSTIVE CROSS"
                        		break
				y += 1

			if cross:
				break
			x += 1
        return cross

#------------------------------------------------------------------------------
def LineWithinSquare(allsquare,particle,typer):
# Given the coordinates of a square region of interest as an array of 
# coordinates and a line which may or maynot cross the ROI. This function 
# determines if the line crosses the ROI and if true outputs the coordinates 
# where the line crosses

	#Define the square more fully for the CalculatePointInPolygon function
#        allsquare = []
#        allsquare.append( [square[0],square[1]] )
#        allsquare.append( [square[2],square[1]] )
#        allsquare.append( [square[2],square[3]] )
#        allsquare.append( [square[0],square[3]] )
#        allsquare.append( [square[0],square[1]] )

	line   = []
	
	#Determine the equation of the particle trail
	dx,dy,tm,tc      = CalculateEquationOfLine(particle)

	#Determine if the particle trail crosses the current square
	if typer == 1: # In Square
		cross,line,debug = DoesLineCrossSquare(allsquare,particle,tm,tc)
	elif typer == 0: # In polygon
                cross,line,debug = DoesLineCrossPolygon(allsquare,particle,tm,tc)	

	if( cross != 1):
                line[0][0] = 0.000; 
		line[0][1] = 0.000; 
		line[1][0] = 0.000; 
		line[1][1] = 0.000;


#	if cross:
#		print "\t\t", cross, line, dx, dy, tm, tc
#		print "\t\t\t", particle

        return cross,line,debug

#------------------------------------------------------------------------------
def DoesLineCrossSquare(allsquare,particle,tm,tc):
# Determines if a line given as an array (X1,Y1,X2,Y2) crosses a given square
# The gradient and intersect of the line are also given as input. 

	debug    = []
        cross    = 0
	LineInSq = []
	case = 0

	xmax = 0.0; xmin = 99999999; 
	ymax = 0.0; ymin = 99999999;


	particle[0] = round(particle[0],3);
	particle[1] = round(particle[1],3);
	particle[2] = round(particle[2],3);
	particle[3] = round(particle[3],3);

	i    = 0
	while i < len(allsquare):
		if allsquare[i][0] >= xmax:
			xmax = allsquare[i][0]
		if allsquare[i][0] <= xmin:
                        xmin = allsquare[i][0]
		if allsquare[i][1] >= ymax:
                        ymax = allsquare[i][1]
                if allsquare[i][1] <= ymin:
                        ymin = allsquare[i][1]
		i += 1

	#Find if moving up or down
	if(particle[1] >= particle[3]): #UP
		ParticleYmax = particle[1]
                ParticleYmin = particle[3]
        else:
                ParticleYmax = particle[3]
                ParticleYmin = particle[1]

        #when moving left to right
        #if( particle[0] < particle[2] and (particle[2] - particle[0] > 2)):
	if( particle[0] < particle[2] ):
		case = 1
		#for x in range(int(allsquare[0][0]),int(allsquare[2][0]+1)):
		for x in range(int(xmin),int(xmax+1)):
			y = ((tm * x) + tc)
			if(CalculatePointInPolygon([x,y],allsquare))    and \
			  (x >= particle[0])  and (x <= particle[2])    and \
			  (y >= ParticleYmin) and (y <= ParticleYmax): 
				debug.append(("_Case 1A:",x,y))
				LineInSq.append([round(x,3),y])
                                cross = 1
			else:	debug.append(("_Case 1B:",x,y))

	#when particle moving right to left
        #elif( particle[0] > particle[2] and (particle[0] - particle[2] > 2)):
	elif( particle[0] > particle[2] ):
		case = 2
		#for x in range(int(allsquare[0][0]),int(allsquare[2][0]-1)):
		for x in range(int(xmin),int(xmax+1)):
			y = ( (tm * x) + tc )
			if(CalculatePointInPolygon([x,y],allsquare))    and \
			  (round(x,3) >= particle[2])  and (round(x,3) <= particle[0])    and \
                          (round(y,3) >= ParticleYmin) and (round(y,3) <= ParticleYmax ): 
               			debug.append(("_Case 2A:",x,y))
				LineInSq.append([round(x,3),y])
                                cross = 1
			else:	debug.append(("_Case 2B:",x,y,))

        #when particle not moving on X, but moving down
        elif( particle[0] == particle[2] and particle[1] < particle[3] ):
	##elif particle[1] < particle[3]:
		case = 3
		for y in range(int(particle[1]),int(particle[3]+1)):
		#for y in range(int(ymin),int(ymax+1)):
			if y >= ymin and y <= ymax:
				x = particle[0]
				if(CalculatePointInPolygon([x,y],allsquare)):
					debug.append(("_Case 3A1:",x,y))
					LineInSq.append([round(x,3),y])
					cross = 1
				else:	
					debug.append(("_Case 3A2:",x,y))

	#when particle not moving on X, but moving up
        elif( particle[0] == particle[2] and particle[1] > particle[3] ):
	##elif particle[1] > particle[3]:
		case = 4
                for y in range(int(particle[3]),int(particle[1]+1)):
		#for y in range(int(ymin),int(ymax+1)):
			if y >= ymin and y <= ymax:
				x = particle[0]
	                        if(CalculatePointInPolygon([x,y],allsquare)):
	                        	debug.append(("_Case 3B1:",x,y))
					New_y= int(particle[1]+1)-y
					LineInSq.append([round(x,3),New_y])
	     	                   	cross = 1
				else:	
					debug.append(("_Case 3B2:",x,y))
	else:
		case = 5
                debug.append("_Case 5:")
		
	Line = []
	if(cross):
		if(case == 1):
			Line.append( [LineInSq[0][0], LineInSq[0][1]] )
        		Line.append( [LineInSq[-1][0], LineInSq[-1][1]] )
		elif(case == 4):
			Line.append( [LineInSq[0][0], LineInSq[0][1]] )
                        Line.append( [LineInSq[-1][0], LineInSq[-1][1]] )
		elif(case == 2): 
			Line.append( [LineInSq[-1][0], LineInSq[-1][1]] )
                        Line.append( [LineInSq[0][0], LineInSq[0][1]] )
		elif(case == 3):
			Line.append( [LineInSq[0][0], LineInSq[0][1]] )
                        Line.append( [LineInSq[-1][0], LineInSq[-1][1]] )
	else:
		Line.append( [0.0,0.0] )
		Line.append( [0.0,0.0] )		

	return cross,Line,case

#------------------------------------------------------------------------------
def DoesLineCrossPolygon(polygon,particle,tm,tc):
# Determines if a line given as an array (X1,Y1,X2,Y2) crosses a given square
# The gradient and intersect of the line are also given as input. 

        debug    = []
        cross    = 0
        LineInSq = []
        case = 9

	
	if particle[0] > particle[2]:
		xmax = particle[0]
		xmin = particle[2]
		xdir = -1
	else:
		xmax = particle[2]
		xmin = particle[0]
		xdir = 1

	if particle[1] > particle[3]:
                ymax = particle[1]
                ymin = particle[3]
		ydir = 1
        else:
                ymax = particle[3]
                ymin = particle[1]
		ydir = -1

	#Find main direction. Either X or in Y 
	if abs(particle[2] - particle[0]) > abs(particle[3] - particle[1]):
		Direction = "X"
	else:
		Direction = "Y"

	# Moving LEFT to RIGHT in X
	if Direction == "X":
		case = 1
		for x in range(int(xmin),int(xmax+1)):
			y = ((tm * x) + tc)
			if(CalculatePointInPolygon([x,y],polygon)) and \
			  (y >= ymin) and (y <= ymax):
				LineInSq.append([round(x,3),round(y,3)])
				cross = 1
	elif Direction == "Y": 
                case = 2
                for y in range(int(ymin),int(ymax+1)):
			try:
				x = ((y - tc) / tm)
			except ZeroDivisionError:
                        	x = (y - tc)
                        if(CalculatePointInPolygon([x,y],polygon)) and \
                          (x >= xmin) and (x <= xmax):
                                LineInSq.append([round(x,3),round(y,3)])
				cross = 1
        Line = []
        if(cross):
		if case == 1:
			if xdir == 1:
				Line.append( [LineInSq[0][0], LineInSq[0][1]]  )
				Line.append( [LineInSq[-1][0], LineInSq[-1][1]] )
			else:
				Line.append( [LineInSq[-1][0], LineInSq[-1][1]] )
				Line.append( [LineInSq[0][0], LineInSq[0][1]]  )
		elif case == 2:
			if ydir == -1:
				Line.append( [LineInSq[0][0], LineInSq[0][1]]  )
				Line.append( [LineInSq[-1][0], LineInSq[-1][1]] )
			else:
				Line.append( [LineInSq[-1][0], LineInSq[-1][1]] )
				Line.append( [LineInSq[0][0], LineInSq[0][1]]  )

        else:
                Line.append( [0.0,0.0] )
                Line.append( [0.0,0.0] )

        return cross,Line,case


#------------------------------------------------------------------------------
def Stats_TTests (Runs1, Runs2):

	Output = ""
	Speeds_1 = []
	Distance_1 = []
	Speeds_2 = []
        Distance_2 = []

	j = 0
        while j < len(Runs1):
		if(Runs1[j][2] == 1):
			Speeds_1.append(Runs1[j][7])
			Distance_1.append(Runs1[j][3])
		elif(Runs1[j][2] == -1):
                        Speeds_1.append(Runs1[j][7])
			Distance_1.append(Runs1[j][3])
		j += 1

	j = 0
        while j < len(Runs2):
                if(Runs2[j][2] == 1 ):
                        Speeds_2.append(Runs2[j][7])
                        Distance_2.append(Runs2[j][3])
                elif(Runs2[j][2] == -1):
                        Speeds_2.append(Runs2[j][7])
                        Distance_2.append(Runs2[j][3])
                j += 1

	import rpy2.robjects
	rSpeeds_1   = robjects.FloatVector(Speeds_1)
	rSpeeds_2   = robjects.FloatVector(Speeds_2)
	rDistance_1 = robjects.FloatVector(Distance_1)
	rDistance_2 = robjects.FloatVector(Distance_2)

	print " + T-Test comparison of run speed and distance distributions"
	print " Speed Comparisons "
	print " t                   =", robjects.r['t.test'](rSpeeds_1,rSpeeds_2)[0][0]
	print " df                  =", robjects.r['t.test'](rSpeeds_1,rSpeeds_2)[1][0]
	print " p-value             =", robjects.r['t.test'](rSpeeds_1,rSpeeds_2)[2][0]
	print " confidence interval =", robjects.r['t.test'](rSpeeds_1,rSpeeds_2)[3][0],\
					robjects.r['t.test'](rSpeeds_1,rSpeeds_2)[3][1]
	print " mean of x           =", robjects.r['t.test'](rSpeeds_1,rSpeeds_2)[4][0]
	print " mean of y           =", robjects.r['t.test'](rSpeeds_1,rSpeeds_2)[4][1] 
	print " hypothesis          =", robjects.r['t.test'](rSpeeds_1,rSpeeds_2)[6][0]
	print " test type           =", robjects.r['t.test'](rSpeeds_1,rSpeeds_2)[7][0]
	print " Distance Comparisons "
        print " t                   =", robjects.r['t.test'](rDistance_1,rDistance_2)[0][0]
        print " df                  =", robjects.r['t.test'](rDistance_1,rDistance_2)[1][0]
        print " p-value             =", robjects.r['t.test'](rDistance_1,rDistance_2)[2][0]
        print " confidence interval =", robjects.r['t.test'](rDistance_1,rDistance_2)[3][0],\
                                        robjects.r['t.test'](rDistance_1,rDistance_2)[3][1]
        print " mean of x           =", robjects.r['t.test'](rDistance_1,rDistance_2)[4][0]
        print " mean of y           =", robjects.r['t.test'](rDistance_1,rDistance_2)[4][1]        
        print " hypothesis          =", robjects.r['t.test'](rDistance_1,rDistance_2)[6][0]
        print " test type           =", robjects.r['t.test'](rDistance_1,rDistance_2)[7][0]
	
	#print " + Kolmogorov-Smirnov Tests"
	#print " Speed Comparisons "
	#print "   D KS-statistic = ", robjects.r['ks.test'](rSpeeds_1,rSpeeds_2,alternative="t")[0][0]
	#print "   P-Value        = ", robjects.r['ks.test'](rSpeeds_1,rSpeeds_2)[1][0]
	#print "   alt hypothesis = ", robjects.r['ks.test'](rSpeeds_1,rSpeeds_2)[2]
	#print " Distance Comparisons "
        #print "   D KS-statistic = ", robjects.r['ks.test'](rDistance_1,rDistance_2)[0][0]
        #print "   P-Value        = ", robjects.r['ks.test'](rDistance_1,rDistance_2)[1][0]
        #print "   alt hypothesis = ", robjects.r['ks.test'](rDistance_1,rDistance_2)[2][0]
	return Output

#------------------------------------------------------------------------------
def Stats_Standards (Runs):

	Speeds_P = []
	Speeds_N = []
	Dist_P   = []
	Dist_N   = []
	Stats    = {}

        j = 0
        while j < len(Runs):
		if(   Runs[j][2] >  0):
			Speeds_P.append(Runs[j][7]) 
			Dist_P.append(Runs[j][5])
                elif( Runs[j][2] <  0): 
			Speeds_N.append(Runs[j][7])
			Dist_N.append(Runs[j][5])
		j += 1

	if len(Speeds_P) > 1: 
		Stats['S_P_D'],Stats['S_P_E'] = Standard_Dev_Error(Speeds_P)
	else: 
		Stats['S_P_D'] = 0; Stats['S_P_E'] = 0

	if len(Speeds_N) > 1:                 
		Stats['S_N_D'],Stats['S_N_E'] = Standard_Dev_Error(Speeds_N)
        else:
                Stats['S_N_D'] = 0; Stats['S_N_E'] = 0

	if len(Dist_P) > 1:                 
		Stats['D_P_D'],Stats['D_P_E'] = Standard_Dev_Error(Dist_P)
        else:
                Stats['D_P_D'] = 0; Stats['D_P_E'] = 0

	if len(Dist_N) > 1:                 
		Stats['D_N_D'],Stats['D_N_E'] = Standard_Dev_Error(Dist_N)
        else:
                Stats['D_N_D'] = 0; Stats['D_N_E'] = 0

	Stats['Num_S_P'] = len(Speeds_P)
	Stats['Num_S_N'] = len(Speeds_N)

	Stats['Num_D_P'] = len(Dist_P)
        Stats['Num_D_N'] = len(Dist_N)


	return Stats

#------------------------------------------------------------------------------
def Stats_Particle (Runs):

	Stats_Particle = {}
	Stats_Particle['Ave_Speed_P']   = 0
	Stats_Particle['Ave_Speed_N']   = 0
	Stats_Particle['Ave_Speed_All'] = 0
	Stats_Particle['No_Runs_P']     = 0
	Stats_Particle['No_Runs_N']     = 0
	Stats_Particle['No_Runs_0']     = 0
	Stats_Particle['Ave_RunLen_P']  = 0
	Stats_Particle['Ave_RunLen_N']  = 0
	Stats_Particle['Total_RunLen_P'] = 0
	Stats_Particle['Total_RunLen_N'] = 0

	i = 0
	while i < len(Runs):
	
		if(   Runs[i][2] ==  1):
			Stats_Particle['Ave_Speed_P']    += Runs[i][7]
			Stats_Particle['Ave_RunLen_P']   += Runs[i][5]
			Stats_Particle['Total_RunLen_P'] += Runs[i][5]
			Stats_Particle['No_Runs_P']      += 1
		elif( Runs[i][2] == -1):
                        Stats_Particle['Ave_Speed_N']    += Runs[i][7]
			Stats_Particle['Ave_RunLen_N']   += Runs[i][6]
			Stats_Particle['Total_RunLen_N'] += Runs[i][6]
			Stats_Particle['No_Runs_N']      += 1
		else:
			Stats_Particle['No_Runs_0']      += 1

		Stats_Particle['Ave_Speed_All'] += Runs[i][7]

		i += 1

	try:   Stats_Particle['Ave_Speed_P']  = '%7.2f' % (Stats_Particle['Ave_Speed_P'] / \
                                                Stats_Particle['No_Runs_P'])
	except ZeroDivisionError: Stats_Particle['Ave_Speed_P'] = 0

	try:   Stats_Particle['Ave_Speed_N']  = '%7.2f' % (Stats_Particle['Ave_Speed_N'] / \
                                                Stats_Particle['No_Runs_N'])
	except ZeroDivisionError: Stats_Particle['Ave_Speed_N'] = 0

	try:   Stats_Particle['Ave_Speed_All'] = '%7.2f' % (Stats_Particle['Ave_Speed_All'] / \
						 len(Runs) )
	except ZeroDivisionError: Stats_Particle['Ave_Speed_All'] = 0 

	try:   Stats_Particle['Ave_RunLen_P']  = '%7.2f' % (Stats_Particle['Ave_RunLen_P'] / \
					 	 Stats_Particle['No_Runs_P'])
	except ZeroDivisionError: Stats_Particle['Ave_RunLen_P'] = 0

	try:   Stats_Particle['Ave_RunLen_N']  = '%7.2f' % (Stats_Particle['Ave_RunLen_N'] / \
                                                 Stats_Particle['No_Runs_N'])
        except ZeroDivisionError: Stats_Particle['Ave_RunLen_N'] = 0


	return Stats_Particle

#------------------------------------------------------------------------------
def ChiSquare (Mode):

	ben = []

	bob = [12,100]
	bill = [30,89]

	ben = [12,100,60,90]

	dave = stats.lchisquare(ben)

	print "+++++"
	print dave
	print Mode
	print "+++++"

	return dave

#------------------------------------------------------------------------------
def CalcRegression (Coords):

	x = []; y =[]
	Regression = {}
	i = 0
	while i < len(Coords):
		x.append(Coords[i][4])
		y.append(Coords[i][5])
		i += 1

	rpy.set_default_mode(rpy.NO_CONVERSION)
	linear_model = r.lm(r("y ~ x"), data = r.data_frame(x=x, y=y))
	rpy.set_default_mode(rpy.BASIC_CONVERSION)

	#print "+++++", linear_model.as_py()['coefficients']['x']

	Regression['X']         = linear_model.as_py()['coefficients']['x']
	Regression['Intercept'] = linear_model.as_py()['coefficients']['(Intercept)']
	Regression['R2']        = r.summary(linear_model)['r.squared']
	Regression['aR2']       = r.summary(linear_model)['adj.r.squared']

	x = []; y = []

	return Regression

#------------------------------------------------------------------------------
def CalcRayleighTest (TrailVectors):

	from rpy2.robjects import r
	r.library("CircStats")

	Angle   = []
	Radians = []
	Mags    = []
	i = 0
        while i < len(TrailVectors):
		Angle.append( float(CalculateVectorAngle( TrailVectors[i] ) ) )
		Radians.append( float(((math.pi/180)*CalculateVectorAngle( TrailVectors[i] ))) )
		Mags.append(  CalculateVectorMagnitude( TrailVectors[i] ))
		i += 1

	rRadians  = robjects.FloatVector(Radians)
	circ_mean = robjects.r['circ.mean'](rRadians)
	print "-------------------------------------------------------------"
	print "+ Circular Mean: %.2f"%(robjects.r['deg'](circ_mean)[0]), " degrees ",	
	print "(rho = %.2f)"%(robjects.r['circ.summary'](rRadians)[2][0])
	print "+ Circular Dispersion:  n=%d r=%.2f rbar=%.2f var=%.2f"%( \
	      robjects.r['circ.disp'](rRadians)[0][0],\
	      robjects.r['circ.disp'](rRadians)[1][0],\
	      robjects.r['circ.disp'](rRadians)[2][0],\
	      robjects.r['circ.disp'](rRadians)[3][0])
	print "+ Rayleigh test of uniformity: rbar=%.2f pvalue=%.2e"%(\
	       robjects.r['r.test'](rRadians)[0][0],\
	       robjects.r['r.test'](rRadians)[1][0])
        print "+ est.kappa: %.2f"%(robjects.r['est.kappa'](rRadians)[0])
	print "+", robjects.r['kuiper'](rRadians)
	print "+", robjects.r['watson'](rRadians, dist="uniform")
	print "+", robjects.r['watson'](rRadians, dist="vm")
	print "-------------------------------------------------------------"

#------------------------------------------------------------------------------
def Standard_Dev_Error (Data):

        #dev = scipy.standardDeviation(Data)
	dev = na.std(Data)

	N   = len(Data)

	try:
		err = "%.2f " % (dev / N)
        except ZeroDivisionError:
                err = 0 

	dev = "%.2f " % dev

        return dev, err

#------------------------------------------------------------------------------
def CorrectCoordinates (Coords,Corrections):
	import re	

	i = 0
	while i < len(Corrections):
		j = 0
		while j < len(Corrections[i]):
			Pattern = re.compile(r'\A'+str(Corrections[i][j][0])+'\Z')
			if Pattern.search(Coords[0][0]): 
				k = 0
				while k < len(Coords):
					if int(Corrections[i][j][1]) == int(Coords[k][1]):
						#print "Matches Corr=", Corrections[i][j],\
						#      " Coord=", Coords[k],
						Xcor = Corrections[i][j][2]-Corrections[0][0][2]
						Ycor = Corrections[i][j][3]-Corrections[0][0][3]
						Coords[k][4] = Coords[k][4] - Xcor
						Coords[k][5] = Coords[k][5] - Ycor
						#print "NewX=", Coords[k][4], " NewY=", Coords[k][5]
					k += 1
			j += 1
		i += 1

	return Coords
#------------------------------------------------------------------------------
def FindLongMovements (Coords,RunDistance):

	Runs = []
	Frame = []
        Stats = {}

	Stats['TotalDist']     = 0
        Stats['NetDistance']   = 0 
        Stats['GrossDistance'] = 0 

#	St = 0
#	Fi = 0

        Distance = [];
	Distance.append ( 0 ) # doesn't move until first frame...

	DistanceXY = [];
        DistanceXY.append ( 0 ) 

	TimeInterval = [];
	TimeInterval.append ( 0 )
	
	i = 1
        while i < len(Coords):
                Distance.append   ( Calculate2PointsDeltaY(\
				    Coords[i-1][2],Coords[i][2]))   
		DistanceXY.append ( Calculate2PointsDistance(\
                                    Coords[i-1][1],Coords[i-1][2],
				    Coords[i][1],Coords[i][2]))
		TimeInterval.append (Coords[i-1][3])
		Frame.append (Coords[i][0])
                i += 1	

	j      = 0
	k      = 0
	Run    = []
	Sign1  = 0
	Sign2  = 0
	while j < len(Distance):
		
                if    Distance[j] > 0: Sign1 = 1
                elif  Distance[j] < 0: Sign1 = -1
                else: Sign1 = 0

                Start = j 
		k = j
		Breaker = 0

		if ((j+1) < len(Frame)) and ((Frame[j]+1) != Frame[j+1]):
                  #     print j,len(Distance), len(Frame),(Frame[j]+1), Frame[j+1]
#			print "Breaker=", Breaker, Frame[j]+1, Frame[j+1]
			Breaker = 1

                while k < len(Distance):
			if    Distance[k] > 0: Sign2 = 1
			elif  Distance[k] < 0: Sign2 = -1
			else: Sign2 = 0

			if(Breaker == 1):
				break

                        if Sign2 == Sign1 or Sign2 == 0: 
				k += 1
				continue
			else:
				k -= 1
				Finish = k 
				Run.append([(Start),(Finish),Sign1])
				j = k
                                break

                if k > j: 
			Run.append([Start,(k-1),Sign1])
			break
                j += 1

	j = 0
        while j < len(Distance):
                Stats['NetDistance']   += Distance[j]
                Stats['GrossDistance'] += abs(Distance[j])
                j += 1

        Runs      = []
	Stats['TotalDist'] = 0
	Stats['Dist_n']    = 0
	Stats['Dist_p']    = 0
	Stats['AveSpeed']  = 0
        Stats['NoRuns_p']  = 0
	Stats['NoRuns_n']  = 0
        i         = 0

	S1 = 0
	F1 = 0

        while i < len(Run):
		Dist   = 0
		DistXY = 0
		Time   = 0
		S      = Run[i][0]
		E      = Run[i][1]

		S1 = Coords[S][0]
		F1 = Coords[E][0]

		while S <= E:
			Dist   += Distance[S]
			DistXY += DistanceXY[S]
			Time   += TimeInterval[S]
			S      += 1

		if abs(Dist) >= abs(RunDistance):# an Run[i][2] == -1:
			#format dist???
			#Runs.append ([Run[i][0],Run[i][1],Run[i][2],Dist])
			if S1 == 2: # deals with first coord problem not starting at zero
				S1 = 1
			if( (DistXY == 0) or (Time == 0) ):
				Speed = 0
			else:
				Speed = DistXY / Time
			Stats['AveSpeed'] += Speed
			Runs.append ([S1,F1,Run[i][2],Dist,Speed])
			Stats['TotalDist'] += Dist

			if Run[i][2] == -1:
				Stats['Dist_n']   += Dist
				Stats['NoRuns_n'] += 1
			if Run[i][2] == 1:
				Stats['Dist_p']   += Dist
				Stats['NoRuns_p'] += 1

                i += 1

	return Runs,Stats

#------------------------------------------------------------------------------
def FindLongMovementsAndPauses (Coords,RunDistance,PauseDistance,PauseDuration,Dimensions,Debug):

	Runs         = []
        Distance     = []; Distance.append ( 0 ) # doesn't move until first frame...
	DistanceXY   = []; DistanceXY.append ( 0 ) 
	Angle        = []; Angle.append (0)
	TimeInterval = []; TimeInterval.append ( 0 )
	Frame        = []; Frame.append ( 1 )
	Feature      = []; Feature.append( 0 )	
	RunDirection = []; RunDirection.append( 0 )
	Stats        = {}
	Stats['TotalDist']     = 0
        Stats['NetDistance']   = 0
        Stats['GrossDistance'] = 0

	# SET UP INITIAL ARRAYS, MAINLY FOR Distance calculations
	i = 1
        while i < len(Coords):
		if(Dimensions == "2D"):
			Distance.append( Calculate2PointsDistance(\
	                                    Coords[i-1][1],Coords[i-1][2],
        	                            Coords[i][1],Coords[i][2]))
		elif(Dimensions == "1DY"):
                	Distance.append   ( Calculate2PointsDeltaY(\
					    Coords[i-1][2],Coords[i][2]))   
		elif(Dimensions == "1DX"):
                        Distance.append   ( Calculate2PointsDeltaY(\
                                            Coords[i-1][1],Coords[i][1]))

		Angle.append ( Calculate2PointsAngle(Coords[i-1][1],Coords[i-1][2],\
			       Coords[i][1],Coords[i][2]) )

		DistanceXY.append ( Calculate2PointsDistance(\
                                    Coords[i-1][1],Coords[i-1][2],
				    Coords[i][1],Coords[i][2]))
		TimeInterval.append (Coords[i-1][3])
		Frame.append (Coords[i][0])
		Feature.append(0)
		RunDirection.append(9) # NINE MEANS NO ASSIGNED YET
                i += 1	


	NewPauses = []
	Sign1  = 0
	Sign2  = 0
	Status = ""
	Status_Now  = 0

	#FIND RUNS
	j = 1
	while j < len(Distance):
		Status_Then     = 0
		TimeMoved       = 0
		DistanceMoved   = 0
		DistanceMovedXY = 0
		PSpeed          = 0

		k = (j+1)
		Status = "     : "
                while k < len(Distance):
			DirStat         = 0
			Dir             = 0
			Status_Now      =  0
			TimeMoved       += TimeInterval[k]
			DistanceMoved   += abs(Distance[k])
			DistanceMovedXY += abs(DistanceXY[k])			

			#New 2D Directionality Calculation to replace 1D
			#DirStat,Dir = CalculateDirection(Angle[k])
			DirStat,Dir = CalculateDirectionRelative(Angle[j],Angle[k])

			# Definition of a turn
			if   ( DirStat == "Reversal" and \
				abs(Distance[k]) < RunDistance and j != 0 ):
				Feature[k] = 0;
			elif ( DirStat == "Reversal" and \
				abs(Distance[k]) > RunDistance and j != 0 ):
				Feature[k] = 2;				
				if  ( Distance[k] > 0):
					RunDirection[k] = 1
				elif( Distance[k] < 0):
                                        RunDirection[k] = -1
			elif ( DirStat == "Continue"):
				Feature[k]    = 0;

			# This defines a PAUSE

			if (TimeMoved >= PauseDuration) and (DistanceMoved <= PauseDistance):
				Status_Now = 1
			elif( DistanceMoved > PauseDistance and Status_Then == 1):

				i = (j+1) #was just j - fixfor erronour pauses 11/12/06
				while (i <= (k-1)): 
					Feature[i]      = -1
					RunDirection[i] = 0
					i += 1 
				try:
					PSpeed = (abs(DistanceMovedXY)-abs(Distance[k]))/ \
						 (TimeMoved-TimeInterval[k])
				except ZeroDivisionError:
					PSpeed = 0

				NewPauses.append([ (j+1),(k-1),0,(DistanceMoved),PauseDistance,\
                                                   PSpeed,(TimeMoved-TimeInterval[k]),\
                                                   (DistanceMovedXY-abs(DistanceXY[k])) ])

				TimeMoved     = 0
                                DistanceMoved = 0

				j = k
				break

			Status_Then = Status_Now
			k += 1
                j += 1

	# Print out a feature list
	#if(Debug):
	#	y = 1
	#	while y < len(Distance):
        #        	print y, "Feature=", Feature[y], "RA=", \
	#		      CalculateDirectionRelative(Angle[y-1],Angle[y]), Distance[y]
        #        	y += 1

	# Find run directions
	Continue      = 0
	DirStat       = 0
        Dir           = 0

	j = 1
	while j < len(Distance):

		i = j
		while i < len(Distance):
			#DirStat,Dir = CalculateDirection(Angle[i])
			DirStat,Dir = CalculateDirectionRelative(Angle[j],Angle[i])
		#	if(Debug): print Angle[j],Angle[i],DirStat,Dir,Distance[i],RunDistance;	
	
			if( Feature[i] == -1):
				#changes j to i not sure if this works
				Continue = 0
				break   

			elif( DirStat == "Continue" and abs(Continue) < RunDistance):
		#		if(Debug): print "1", DirStat, Distance[i], j, i
				Continue += abs(Distance[i])
				i += 1
				continue		
			elif( DirStat == "Continue" and abs(Continue) >= RunDistance):
		#		if(Debug): print "2", DirStat, Distance[i], j, i
				Continue += abs(Distance[i])
				i += 1
				for x in range(j,i):
					Feature[x]      = 0
					RunDirection[x] = 1
				continue
			elif( DirStat == "Reversal" and abs(Distance[i]) >= RunDistance ):
		#		if(Debug): print "3", DirStat, Distance[i], j, i
				Continue += abs(Distance[i])
				#j = (i-1)
				j = i
				break

			elif( DirStat == "Reversal" and abs(Distance[i]) < RunDistance ):
		#		if(Debug): print "4", DirStat, Distance[i], j, i
				#j = (i-1)
				j = i
				Continue = 0
				break
			else:
				print "IF YOU SEE THIS SOMETHING WENT WRONG"
		j += 1

	# Clean up run definitions, but including movements less than 
	# RunDistance (not in Runs or Pauses)
	j = 1
	featno = 3
	while j < len(Distance):

		if( Feature[j] == 2 and featno == 4):
			featno     = 3
			Feature[j] = 33
			RunDirection[j] = 3
		elif ( Feature[j] == 2 and featno == 3):
			featno     = 4
			Feature[j] = 44
			RunDirection[j] = 4

		if( Feature[j] == 0):
			Feature[j]     = featno
			RunDirection[j] = featno

		if(Debug): 
			print "Feature[",j,"] =", Feature[j], \
			"RunDirection[",j,"]",RunDirection[j]

		j += 1


	x = 0
	Start     = 0
	End       = 0
	Runs   = []

	j = 1
	i = 1
        while j < (len(Distance)):
		Dist      = 0
        	AbsDist   = 0
		AbsDistXY = 0
		PosDist   = 0
		NegDist   = 0
		TimeRun   = 0
		SpeedRun  = 0

		while i < (len(Distance)):
			if( RunDirection[j] == RunDirection[i]):
				Start      = j
				End        = i
				Dist      += Distance[i]
				AbsDist   += abs(Distance[i])
				AbsDistXY += abs(DistanceXY[i])
				TimeRun   += TimeInterval[i]

				if(RunDirection[i] == 4):
					PosDist += Distance[i]
				elif(RunDirection[i] == 3):
					NegDist += Distance[i]
				i += 1
			else:
				x += 1
				j = (i-1)
				break

		if(RunDirection[j] == 4):
			try:
        	        	SpeedRun = PosDist / TimeRun    
			except ZeroDivisionError:
                        	SpeedRun = 0
		elif(RunDirection[j] == 3):
                        try:
                                SpeedRun = NegDist / TimeRun
                        except ZeroDivisionError:
                                SpeedRun = 0
		else:
			try:
                                SpeedRun = AbsDist / TimeRun
                        except ZeroDivisionError:
                                SpeedRun = 0


		# Cuts out the mini non run
		if( (RunDirection[j] == 3 and abs(NegDist) >= RunDistance) or \
                    (RunDirection[j] == 4 and abs(PosDist) >= RunDistance) or \
                    (RunDirection[j] ==  0) ):
			if  (RunDirection[j] == 3): RunDirection[j] = -1
			elif(RunDirection[j] == 4): RunDirection[j] =  1

			# UNTIL DIRECTIONS SORTED
			Runs.append ([Start,End,RunDirection[j],\
		  	              Dist,AbsDist, PosDist, NegDist,\
                	              abs(SpeedRun),TimeRun,AbsDistXY])
		j = i

	# Prints a report - debugging only
	if(Debug):
		y = 0
	        while y < len(NewPauses):
	                testDist = 0
			testTime = 0
	                print y, NewPauses[y]

	                x = NewPauses[y][0]
	                while  (x <= NewPauses[y][1]):
	                        testDist += abs(Distance[x])
				testTime += TimeInterval[x]
	                        print "\tP\t",  x, "\tF=", Coords[x][0], \
				      "\tD=%6.2f"%Distance[x], "(%6.2f"%testDist, \
				      ")\tTimeInterval=", testTime, \
				      "(", TimeInterval[x], ")", \
				      "\tSpeed=%6.2f"%(testDist/testTime) 
        	                x += 1
                	print
                	y += 1


	return Runs

#------------------------------------------------------------------------------
def FindLongMovementsAndPausesEve (Coords,RunDistance,RunFrames,PauseSpeed,PauseFrames,Dimensions,Debug):

	Runs         = []
        Distance     = []; Distance.append( 0 ) # doesn't move until first frame...
	DistanceXY   = []; DistanceXY.append( 0 ) 
	Angle        = []; Angle.append( 0 )
	TimeInterval = []; TimeInterval.append( 0 )
	Frame        = []; Frame.append( 1 )
	Speed        = []; Speed.append( 0 )
	Feature      = []; Feature.append( 9 )	
	RunDirection = []; RunDirection.append( 9 )
	Stats        = {}
	Stats['TotalDist']     = 0
        Stats['NetDistance']   = 0
        Stats['GrossDistance'] = 0

	# SET UP INITIAL ARRAYS, MAINLY FOR Distance calculations
	i = 1
        while i < len(Coords):
		if(Dimensions == "2D"):
			Distance.append( Calculate2PointsDistance(\
	                                    Coords[i-1][4],Coords[i-1][5],
        	                            Coords[i][4],Coords[i][5]))
		elif(Dimensions == "1DY"):
                	Distance.append   ( Calculate2PointsDeltaY(\
					    Coords[i-1][5],Coords[i][5]))   
		elif(Dimensions == "1DX"):
                        Distance.append   ( Calculate2PointsDeltaY(\
                                            Coords[i-1][4],Coords[i][4]))

		Angle.append ( Calculate2PointsAngle(Coords[i-1][4],Coords[i-1][5],\
			       Coords[i][4],Coords[i][5]) )

		DistanceXY.append ( Calculate2PointsDistance(\
                                    Coords[i-1][4],Coords[i-1][5],
				    Coords[i][4],Coords[i][5]))
		TimeInterval.append (Coords[i][2])
		Frame.append (Coords[i][1])

		try:
			sped = DistanceXY[-1]/TimeInterval[-1]
		except ZeroDivisionError:
			sped = 0
		Speed.append( sped  )

		Feature.append(9)
		RunDirection.append(9) # NINE MEANS NO ASSIGNED YET
                i += 1	

	#FIND PAUSES
	NewPauses = []
	j = 0
	while j <= len(Distance):
		Status_Then     = 0

		k = (j+1)
                while k < len(Distance):
			if(Speed[k] <= float(PauseSpeed)) and (k != (len(Distance)-1)):
				Status_Now = 1
			elif((Speed[k] > float(PauseSpeed))) and (k != (len(Distance)-1)) \
			     and (Status_Then >= int(PauseFrames)):
				NewPauses.append( CalculateMovementDetails( Coords,(j+1),(k-1),\
						  0,Distance,DistanceXY,TimeInterval) )
				Status_Then   = 0
				Status_Now    = 0
				j = k+1
				break

			elif( k == (len(Distance)-1)) and (Speed[k] <= float(PauseSpeed)) \
			     and ( (k-j) >= int(PauseFrames)):

                                NewPauses.append( CalculateMovementDetails( Coords,(j+1),k,\
							0,Distance,DistanceXY,TimeInterval) )
				Status_Then   = 0
                                Status_Now    = 0

				j = k
				break
			else:
				break

			Status_Then += Status_Now
			k += 1
		j += 1

	# Sort out Features 
	i = 0
	while i < len(NewPauses):
		j = NewPauses[i][0]
		while j <= NewPauses[i][1]:
			Feature[j] = 0
			j += 1
		i += 1

	#Calculates RUNS
	NewRuns = []
	i = 0
        while i < len(Feature):
		try:
			speed = (Distance[i]/TimeInterval[i])
		except ZeroDivisionError:
			speed = 0.0
		if(Debug):
			print "Feature", i, "F=%.2f"%Feature[i], "D=%.2f"%Distance[i], \
			      "T=%d"%TimeInterval[i], "S=%.2f"%speed 
		count = 0
		if(Feature[i] != 0): #NOT A PAUSE
			j = i+1
			while j < len(Feature):
				if(Feature[j] != 0) and ( j < (len(Feature)-1) ): #NOT A PAUSE
					try:
                        			speed = (Distance[j]/TimeInterval[j])
                			except ZeroDivisionError:
                        			speed = 0.0
					if(Debug):
						print "\tFeature", j, "F=%.2f"%Feature[j], \
						      "D=%.2f"%Distance[j], "T=%d"%TimeInterval[j],\
						      "S=%.2f"%speed, count, len(Feature)
					count += 1		
				elif( j >= (len(Feature)-1)) and (count >= int(RunFrames) ):
					if(Debug):
                                                print "\t-Feature", j, "F=%.2f"%Feature[j], \
                                                      "D=%.2f"%Distance[j], "T=%d"%TimeInterval[j],\
                                                      "S=%.2f"%speed, count, len(Feature)
						print "\tBIG RUN", i, "to", len(Feature)-1
					NewRuns.append(CalculateMovementDetails(\
                                                       Coords,(j-count-1),j,1,\
                                                       Distance,DistanceXY,TimeInterval))
					i = (j-1)
					break
				else:
					#if( (j-count) >= int(RunFrames)):
					if( count >= int(RunFrames)):
						if(Debug):
							print "\t\tRun from", (j-count-1), "to", \
							      (j-1), "Count=", count, (j-count)	
						NewRuns.append(CalculateMovementDetails(\
							        Coords,(j-count-1),(j-1),1,\
								Distance,DistanceXY,TimeInterval))
						i = (j-1)
						break
				j += 1
                i += 1

	# Sort out Features 
        i = 0
        while i < len(NewRuns):
                j = NewRuns[i][0]
                while j <= NewRuns[i][1]:
                        Feature[j] = 0
                        j += 1
                i += 1


	# Prints a report - debugging only
	if(Debug):
		y = 0
                while y < len(NewRuns):
                        testDist = 0
                        testTime = 0
                        print y, NewRuns[y]

                        x = NewRuns[y][0]
                        while  (x <= NewRuns[y][1]):
                                testDist += abs(Distance[x])
                                testTime += TimeInterval[x]
                                print "\tR\t",  x, "\tF=", Coords[x][1], \
                                      "\tD=%6.2f"%Distance[x], "(%6.2f"%testDist, \
                                      ")\tTimeInterval=%4d"%testTime, \
                                      "(%4d"%TimeInterval[x], ")", \
                                      "\tSpeed=%6.2f"%Speed[x]
                                x += 1
                        print
                        y += 1


		y = 0
	        while y < len(NewPauses):
	                testDist = 0
			testTime = 0
	                print y, NewPauses[y]

	                x = NewPauses[y][0]
	                while  (x <= NewPauses[y][1]):
	                        testDist += abs(Distance[x])
				testTime += TimeInterval[x]
	                        print "\tP\t",  x, "\tF=", Coords[x][1], \
				      "\tD=%6.2f"%Distance[x], "(%6.2f"%testDist, \
				      ")\tTimeInterval=%4d"%testTime, \
				      "(%4d"%TimeInterval[x], ")", \
				      "\tSpeed=%6.2f"%Speed[x] 
        	                x += 1
                	print
                	y += 1

		y = 0
	        while y < len(Feature):	
			if(Feature[y] == 9):
				print "Feature", y, "=", Feature[y]
			y += 1

	Movements = []
	Movements.extend(NewRuns)
	Movements.extend(NewPauses)

	return Movements

#------------------------------------------------------------------------------
def FindLongMovementsAndPausesRaquel (Coords,Regression,Axes,PauseDef,\
				      RunDistance,RunFrames,\
				      PauseDistance,PauseSpeed,PauseFrames,\
				      PauseDuration,ReverseFrames,PixelRatio,\
				      Dimensions,TimeStart,TimeEnd,Debug):

	Runs         = []
        Distance     = []; Distance.append( 0 ) # doesn't move until first frame...
	DistanceXY   = []; DistanceXY.append( 0 ) 
	Angle        = []; Angle.append( 0 )
	AngleRel     = []; AngleRel.append( 0 )
	TimeInterval = []; TimeInterval.append( 0 )
	Frame        = []; Frame.append( 1 )
	Speed        = []; Speed.append( 0 )
	Feature      = []; Feature.append( 9 )	
	RunDirection = []; RunDirection.append( 9 )
	Stats        = {}
	Stats['TotalDist']     = 0
        Stats['NetDistance']   = 0
        Stats['GrossDistance'] = 0

	#Get the user defined axes or Regresion Coordinates for the Directionality Baseline
	if Axes[0] == 99 and Axes[2] == 99:
	        regX  = []
	        regY  = []
	        i = 0
	        while i < len(Coords):
	                regX.append(Coords[i][4])
	                regY.append( (Coords[i][4]*Regression['X'])+(Regression['Intercept'])  )
	                i += 1
	        AxisAngle = Calculate2PointsAngleNew(regX[0],regY[0],regX[-1],regY[-1])

	elif Axes[0] == 100 and Axes[2] == 120:
		AxisAngle = 90

	else:
		i = 0
	        while i < len(Axes): 
			#print "+++++++++++++++++", Axes[i][0]

			if Coords[0][0] == Axes[i][0]:
				break
			i += 1
		AxisAngle = Calculate2PointsAngleNew(Axes[i][1],Axes[i][2],Axes[i][3],Axes[i][4])

	# SET UP INITIAL ARRAYS, MAINLY FOR Distance calculations
	i = 1
        while i < len(Coords):
		if(Dimensions == "2D"):
			Distance.append( Calculate2PointsDistance(\
	                                    Coords[i-1][4],Coords[i-1][5],
        	                            Coords[i][4],Coords[i][5]))
		elif(Dimensions == "1DY"):
                	Distance.append   ( Calculate2PointsDeltaY(\
					    Coords[i-1][5],Coords[i][5]))   
		elif(Dimensions == "1DX"):
                        Distance.append   ( Calculate2PointsDeltaY(\
                                            Coords[i-1][4],Coords[i][4]))

		Angle.append ( Calculate2PointsAngleNew(Coords[i-1][4],Coords[i-1][5],\
			       Coords[i][4],Coords[i][5]) )

		AngleRel.append ( ((Angle[-1]+(360-AxisAngle))%360) )

		DistanceXY.append ( Calculate2PointsDistance(\
                                    Coords[i-1][4],Coords[i-1][5],
				    Coords[i][4],Coords[i][5]))
		TimeInterval.append (Coords[i][2])
		Frame.append (Coords[i][1])

		try:
			sped = DistanceXY[-1]/TimeInterval[-1]
		except ZeroDivisionError:
			sped = 0
		Speed.append( sped  )

		Feature.append(9)

		# Setting up of run directions
		if AngleRel[-1] >= 90 and AngleRel[-1] < 270:
			RunDirection.append(1) # PLUS RUN
		else:
			RunDirection.append(-1)  # MINUS RUN

		#print "\t", i, Coords[i-1][4],Coords[i-1][5],Coords[i][4],Coords[i][5],\
		#      " -- ", Distance[-1],sped,TimeInterval[-1],\
		#      " %.1f"%Angle[-1]," %.1f"%AngleRel[-1],RunDirection[-1]

                i += 1	

	#FIND PAUSES
	NewPauses = []
	DDist = 0
	ADist = 0
	j = 0
	while j <= len(Distance):
		Status_Then     = 0
		k = (j+1)
                while k < len(Distance):
			if PauseDef == 1: #Pauses defined by speed
				if(Speed[k] <= float(PauseSpeed)) and (k != (len(Distance)-1)):
					Status_Now = 1
				# SPEED OK, ENOUGH FRAMES
				elif((Speed[k] > float(PauseSpeed))) and (k != (len(Distance)-1)) \
				     and (Status_Then >= int(PauseFrames)):
					NewPauses.append( CalculateMovementDetails(Coords,(j+1),(k-1),\
							  0,Distance,DistanceXY,TimeInterval,AxisAngle) )
					Status_Then   = 0
					Status_Now    = 0
					j = k+1
					break
				# END OF TRACK, Speed and frames OK
				elif( k == (len(Distance)-1)) and (Speed[k] <= float(PauseSpeed)) \
				     and ( (k-j) >= int(PauseFrames)):
        	                        NewPauses.append( CalculateMovementDetails( Coords,(j+1),k,\
							  0,Distance,DistanceXY,TimeInterval,AxisAngle) )
					Status_Then   = 0
                                	Status_Now    = 0
					j = k
					break
				else:
					break
			else: #Pauses defined by distance
				DDist = Calculate2PointsDistance( Coords[j][4],Coords[j][5],\
								  Coords[k][4],Coords[k][5])	
				ADist = sum(Distance[j:k]) 
                                                
				# TOO LONG
                                if(DDist <= float(PauseDistance)) and (k != (len(Distance)-1)):
                                        Status_Now = 1
                                # DISTANCE OK, ENOUGH FRAMES
                                elif((DDist > float(PauseDistance))) and (k != (len(Distance)-1)) \
                                     and (Status_Then >= int(PauseFrames)):
                                        NewPauses.append( CalculateMovementDetails(Coords,(j+1),(k-1),\
                                                          0,Distance,DistanceXY,TimeInterval,AxisAngle) )
                                        Status_Then   = 0
                                        Status_Now    = 0
                                        j = k+1
                                        break
                                # END OF TRACK, Distance and frames OK
                                elif( k == (len(Distance)-1)) and (DDist <= float(PauseDistance)) \
                                     and ( (k-j) >= int(PauseFrames)):
                                        NewPauses.append( CalculateMovementDetails( Coords,(j+1),k,\
                                                          0,Distance,DistanceXY,TimeInterval,AxisAngle) )
                                        Status_Then   = 0
                                        Status_Now    = 0
                                        j = k
                                        break
                                else:
                                        break

			Status_Then += Status_Now
			#DDist = Calculate2PointsDistance( Coords[j][4],Coords[j][5],Coords[k][4],Coords[k][5])
			k += 1
		j += 1

	# Sort out Features 
	i = 0
	while i < len(NewPauses):
		j = NewPauses[i][0]
		while j <= NewPauses[i][1]:
			Feature[j] = 0
			RunDirection[j] = 0
			j += 1
		i += 1

	#Calculates RUNS
	NewRuns = []
	i = 0
        while i < len(Feature):
		RunDist   = 0
		RunDistSE = 0
		RunDir    = []
		RelAng    = []
		Reverse   = 0
		try:
			speed = (Distance[i]/TimeInterval[i])
		except ZeroDivisionError:
			speed = 0.0
		if(Debug):
			print "Feature", i, "F=%.2f"%Feature[i], "D=%.2f"%Distance[i], \
			      "T=%d"%TimeInterval[i], "S=%.2f"%speed 
		count = 0
		DirP  = 0
		DirM  = 0
		if(Feature[i] != 0): #NOT A PAUSE
			j = i+1
			while j < len(Feature):
				if ( j < (len(Feature)-1) ) and (Reverse != 1) and (Feature[j] != 0): 
					try:
                       				speed = (Distance[j]/TimeInterval[j])
               				except ZeroDivisionError:
                       				speed = 0.0

					count += 1		
					RunDist   += Distance[j]
					RunDistSE += Calculate2PointsDistance(Coords[i][4],Coords[i][5],Coords[j][4],Coords[j][5])

					RunDir.append( RunDirection[j] )
					RelAng.append( AngleRel[j] )
					Reverse = CheckReversal( RunDir, RelAng )
					if Reverse == 1: RunDir = []

					if(Debug):
	                                        print "\tRun    %3d"%j, "F=%d"%Feature[j], \
        	                                      "D=%6.2f"%Distance[j], \
                	                              "T=%d"%TimeInterval[j],\
                        	                      "S=%.2f"%speed, "A=%.1f"%Angle[j],count,\
                                	              "Dir=%d"%RunDirection[j], "Reverse=",Reverse

				elif((j >= (len(Feature)-1)) or (Reverse == 1) or (Feature[j] == 0)) and count > 0:
					if(Debug):
	                                        print "\tEnd Run", j, "(", i, ")", "F=%d"%Feature[j], \
        	                               	      "D=%.2f"%Distance[j], \
						      "T=%d"%TimeInterval[j],\
        	        	                      "S=%.2f"%speed, "A=%.1f"%Angle[j],count,\
						      "Dir=%d"%RunDirection[j],"Count=",count, "RunDist=", RunDist

					if Reverse == 1:
						Start = j-count
						End   = j-3
						i     = (j-1)-3
						if sum(RunDirection[Start:End]) >= 1: Direction = 1
						else: Direction = -1
					else:
						Start = j-count
               	                                End   = j
						i     = (j-1)
						if sum(RunDirection[Start:End]) >= 1: Direction = 1
                                       	        else: Direction = -1

					if RunDistSE >= RunDistance and RunDistance > 0: # and RunFrames == 0:
						NewRuns.append(CalculateMovementDetails(\
       		                                               Coords,Start,End,Direction,\
               		                                       Distance,DistanceXY,TimeInterval,AxisAngle))
					elif count >= RunFrames and RunDistance == 0 and RunFrames > 0:
						NewRuns.append(CalculateMovementDetails(\
                                                               Coords,Start,End,Direction,\
                                                               Distance,DistanceXY,TimeInterval,AxisAngle))	
					RunDir = []
					RelAng = []
					break
				else:
					if(Debug):
						print "\t???    %3d"%j, "F=%d"%Feature[j], \
        	                                      "D=%6.2f"%Distance[j], \
                	                              "T=%d"%TimeInterval[j],\
                        	                      "S=%.2f"%speed, "A=%.1f"%Angle[j],count,\
                                	              "Dir=%d"%RunDirection[j], "Reverse=",Reverse
				j += 1
                i += 1

	# Sort out Features 
        i = 0
        while i < len(NewRuns):
                j = NewRuns[i][0]
                while j <= NewRuns[i][1]:
                        Feature[j] = 0
                        j += 1
                i += 1

	# Prints a report - debugging only
	if(Debug):
		y = 0
                while y < len(NewRuns):
                        testDist = 0
                        testTime = 0
                        print y, NewRuns[y]

                        x = NewRuns[y][0]
                        while  (x <= NewRuns[y][1]):
                                testDist += abs(Distance[x])
                                testTime += TimeInterval[x]
                                print "\tR %3d"%x, "  F=%3d"%Coords[x][1], \
                                      "  D=%6.2f"%Distance[x], "(%6.2f"%testDist, \
                                      ")  TimeInt=%4d"%testTime, \
                                      "(%4d"%TimeInterval[x], ")", \
                                      "  Spd=%6.2f"%Speed[x], "  Dir=%2d"%RunDirection[x]
                                x += 1
                        print
                        y += 1


		y = 0
	        while y < len(NewPauses):
	                testDist = 0
			testTime = 0
	                print y, NewPauses[y]

	                x = NewPauses[y][0]
	                while  (x <= NewPauses[y][1]):
	                        testDist += abs(Distance[x])
				testTime += TimeInterval[x]
	                        print "\tP %3d"%x, "\tF=%3d"%Coords[x][1], \
				      "  D=%6.2f"%Distance[x], "(%6.2f"%testDist, \
				      ")  TimeInt=%4d"%testTime, \
				      "(%4d"%TimeInterval[x], ")", \
				      "  Spd=%6.2f"%Speed[x], "  Dir=%2d"%RunDirection[x] 
        	                x += 1
                	print
                	y += 1

		y = 0
	        while y < len(Feature):	
			if(Feature[y] == 9):
				print "Feature", y, "=", Feature[y]
			y += 1

	Movements = []
	Movements.extend(NewRuns)
	Movements.extend(NewPauses)
	Movements.sort(key=lambda x:x[0] )

	return Movements

#------------------------------------------------------------------------------
def CheckReversal ( RunDir, RelAngle ):
# Funtion to determine if a particle goes through a reversal or not
# 

	reversal = 0
	counter  = 0
	First = RunDir[0]
	InitDir = 0
	Start = 0

	#print "----------", RunDir, RelAngle

	i = 1
	while i < len(RunDir):

		if First == RunDir[i]:
			counter += 1
		else:
			First = RunDir[i]
			counter = 0

		if counter == 2:
			InitDir = RunDir[i]
			Start = i
			#print "\t\tInitDir=", InitDir, Start
			break
		i += 1

	i = Start
        while i < len(RunDir):
		if InitDir != 0:
			if RunDir[i] == InitDir:
				counter = 0
			else:
				counter += 1

			if counter == 2:
				#print "\t\t", i, "Reversal!", InitDir, len(RunDir)
				reversal = 1
				break
		i += 1

	return reversal

#------------------------------------------------------------------------------
def CalculateMovementDetails (Coords,j,k,Dir,Distance,DistanceXY,TimeInterval,\
			      AxisAngle):
# This function takes the raw values for the runs and pauses and calculates 
# some basic stats like speeds and distances including regression 
# calculation then feeds back a standardised list of paramenters for runs
# and pauses

	Details = []
	Time    = 0.0
	RSpeed  = 0.0
	Angle   = 0.0
	RegDist = 0
	MovementCoords = []

	Time = 0
	i = j
	while i <= k:
		MovementCoords.append( [ Coords[i][4],Coords[i][5] ] )
		Time += TimeInterval[i]
		i += 1

	S2EDistance = Calculate2PointsDistance(MovementCoords[0][0],  MovementCoords[0][1],\
                                               MovementCoords[-1][0], MovementCoords[-1][1])

	if len(MovementCoords) > 2:
		#Regression = Regression_CVersion(MovementCoords,0,1)
		Regression = KymoRegression(MovementCoords,0,1)
		
		i = 0
                while i < len(MovementCoords):
			try:
                        	MovementCoords[i][0] = float((MovementCoords[i][1]-\
						       Regression['Intercept']) / \
						       Regression['X'])
			except ZeroDivisionError:
				MovementCoords[i][0] = float(MovementCoords[i][1]-\
                                                              Regression['Intercept'])
                        i += 1

		RegDist = Calculate2PointsDistance(MovementCoords[0][0],  MovementCoords[0][1],\
						   MovementCoords[-1][0], MovementCoords[-1][1])
		try:
			RegSpeed = (RegDist/Time) * 60
		except ZeroDivisionError:
			RegSpeed = 0.0
		Angle = Calculate2PointsAngleNew(MovementCoords[0][0],  MovementCoords[0][1],\
                                                 MovementCoords[-1][0], MovementCoords[-1][1])
		#Angle = (Angle+AxisAngle)%360
		Angle = ((360-AxisAngle)+Angle)%360
		
	elif len(MovementCoords) == 2:
		RegDist = Calculate2PointsDistance(MovementCoords[0][0],  MovementCoords[0][1],\
                                                   MovementCoords[-1][0], MovementCoords[-1][1])
		try:
                	RegSpeed = (RegDist/Time) * 60
		except ZeroDivisionError:
			RegSpeed = 0.0
                Angle = Calculate2PointsAngleNew(MovementCoords[0][0],  MovementCoords[0][1],\
                                                 MovementCoords[-1][0], MovementCoords[-1][1])
                #Angle = (Angle+AxisAngle)%360
		Angle = ((360-AxisAngle)+Angle)%360
	else:
		RegSpeed = 0.0
		Angle = 0.0

	if Dir == 0:
		Angle = 0
	else:
		if Angle >= 90 and Angle < 270:
			Dir = 1
		else:
			Dir = -1 

	DistanceMoved   = 0
        DistanceMovedXY = 0
        i = j
        while (i <= k):
		DistanceMoved   += abs(Distance[i])
                DistanceMovedXY += abs(DistanceXY[i])
                i += 1

        try:
              	Speed = ( DistanceMovedXY / Time ) * 60
        except ZeroDivisionError:
                Speed = 0.0

	try:
                S2ESpeed = ( S2EDistance / Time ) * 60
        except ZeroDivisionError:
                S2ESpeed = 0.0

        Details = [ j,k,Dir,DistanceMoved,S2EDistance,RegDist,\
                    Angle,Speed,S2ESpeed,RegSpeed,Time ]

	return Details

#------------------------------------------------------------------------------
def ThreeFrameRunAnalysis ( Runs, Coords, DirGraphs ):
#
# Function divides up runs into overlapping three frame windows.
# 29/06/09 

	Results = []
	outputfile = open(DirGraphs+"/ThreeFrameData_All.txt",'w')
	line = "CoordSet\tSheet\tParticleNo\tDirection\tSpeed\n"
	outputfile.write( line )

	i = 0
	while i < len(Runs):
		j = 0
		while j < len(Runs[i]['Runs']):
			if Runs[i]['Runs'][j][2] != 0:
				if(Runs[i]['Runs'][j][1]-Runs[i]['Runs'][j][0]) >= 3: 

					k = (Runs[i]['Runs'][j][0])
					while k <= (Runs[i]['Runs'][j][1]):
						T = 0
						D = 0
						if (k+3) <= Runs[i]['Runs'][j][1]:
							x = 0
							while x < 3: 
								T += Coords[Runs[i]['CoordsSet']]['Coords'][Runs[i]['Sheet']][Runs[i]['Particle']][x+k][2]
								x += 1
							D = Calculate2PointsDistance( Coords[Runs[i]['CoordsSet']]['Coords'][Runs[i]['Sheet']][Runs[i]['Particle']][k][4],Coords[Runs[i]['CoordsSet']]['Coords'][Runs[i]['Sheet']][Runs[i]['Particle']][k][5],Coords[Runs[i]['CoordsSet']]['Coords'][Runs[i]['Sheet']][Runs[i]['Particle']][k+x][4],Coords[Runs[i]['CoordsSet']]['Coords'][Runs[i]['Sheet']][Runs[i]['Particle']][k+x][5] )

							Results.append( [Runs[i]['CoordsSet'],\
									 Runs[i]['Sheet'], \
									 Runs[i]['Particle'],\
									 Runs[i]['Runs'][j][2],\
									 (D/T)*60])

							line = str(Runs[i]['CoordsSet'])+"\t"+\
                                                               str(Runs[i]['Sheet'])+"\t"+\
                                                               str(Runs[i]['Particle'])+"\t"+\
							       str(len(Runs[i]['Runs']))+"\t"+\
                                                               str(Runs[i]['Runs'][j][2])+"\t"+\
                                                               str((D/T)*60)+"\n"

							outputfile.write( line ) 
						k += 1
			j += 1
		i += 1

        outputfile.close()

	return Results

#------------------------------------------------------------------------------
def ThreeFrameMaxRunAnalysis ( Runs, Coords, DirGraphs ):
        Results = []
        outputfile = open(DirGraphs+"/ThreeFrameMaxData_All.txt",'w')
        line = "CoordSet\tSheet\tParticleNo\tDirection\tSpeed\n"
        outputfile.write( line )
	MaxSpeed = []

        i = 0
        while i < len(Runs):
                j = 0
                while j < len(Runs[i]['Runs']):
                        if Runs[i]['Runs'][j][2] != 0:
                                if(Runs[i]['Runs'][j][1]-Runs[i]['Runs'][j][0]) >= 3:
					MaxSpeed = []

                                        k = (Runs[i]['Runs'][j][0])
                                        while k <= (Runs[i]['Runs'][j][1]):
                                                T = 0
                                                D = 0
                                                if (k+3) <= Runs[i]['Runs'][j][1]:
                                                        x = 0
                                                        while x < 3:
                                                                T += Coords[Runs[i]['CoordsSet']]['Coords'][Runs[i]['Sheet']][Runs[i]['Particle']][x+k][2]
                                                                x += 1
                                                        D = Calculate2PointsDistance( \
						Coords[Runs[i]['CoordsSet']]['Coords'][Runs[i]['Sheet']][Runs[i]['Particle']][k][4],\
						Coords[Runs[i]['CoordsSet']]['Coords'][Runs[i]['Sheet']][Runs[i]['Particle']][k][5],\
						Coords[Runs[i]['CoordsSet']]['Coords'][Runs[i]['Sheet']][Runs[i]['Particle']][k+x][4],\
						Coords[Runs[i]['CoordsSet']]['Coords'][Runs[i]['Sheet']][Runs[i]['Particle']][k+x][5] )
							MaxSpeed.append( ((D/T)*60) )
                                                k += 1

				if len(MaxSpeed) < 1: MaxSpeed = [0]

				Results.append( [Runs[i]['CoordsSet'],\
	                                         Runs[i]['Sheet'], \
                                        	 Runs[i]['Particle'],\
                                	         Runs[i]['Runs'][j][2],\
                        	                 max(MaxSpeed)])
				line = str(Runs[i]['CoordsSet'])+"\t"+\
        	                       str(Runs[i]['Sheet'])+"\t"+\
	                               str(Runs[i]['Particle'])+"\t"+\
                        	       str(len(Runs[i]['Runs']))+"\t"+\
                	               str(Runs[i]['Runs'][j][2])+"\t"+\
        	                       str(max(MaxSpeed))+"\n"
				outputfile.write( line )
                        j += 1
                i += 1

        outputfile.close()

        return Results
#------------------------------------------------------------------------------
def DirectionChangesAnalysis ( Runs, CoordsSet, DirGraphs ):

	ParticleDirChanges = []

	outputfile = open(DirGraphs+"/DirectionChangeData_All_"+str(CoordsSet)+".txt",'w')
        line = "CoordSet\tRun\tNoChangesinDir\n"
        outputfile.write( line )

	i = 0
        while i < len(Runs):

		if Runs[i]['CoordsSet'] == CoordsSet:
			DirChange = 0
			RunDir 	  = []

			j = 0
                	while j < len(Runs[i]['Runs']):
				if Runs[i]['Runs'][j][2] != 0:
					RunDir.append(Runs[i]['Runs'][j][2])
				j += 1

			j = 1
      	                while j < len(RunDir):
				if RunDir[j-1] != RunDir[j]:
					DirChange += 1		
				j += 1

			ParticleDirChanges.append(DirChange)
			line = str(CoordsSet)+"\t"+str(i)+"\t"+str(DirChange)+"\n"
			outputfile.write( line )
		i += 1

	outputfile.close()

	return ParticleDirChanges

#------------------------------------------------------------------------------
def AnalyseRuns (Coords,Runs):

	i = 0
	print "Runs Analysis Start"
	while i < len(Runs):
		Start     = int(Runs[i][0])
		Finish    = int(Runs[i][1])
		Direction = int(Runs[i][2])

		Distance  = float(abs(Coords[Finish][3] - Coords[Start][3]))
		Frames    = abs(Runs[i][1] - Runs[i][0])

		print "\tRun= [%3d] " % (i+1),
		print " Dist= [%6.2f]" % Distance,
		print " Frames= [%3d]" % Frames,
		print " Speed= [%6.2f]" % (Distance/Frames)
		i += 1

	print "Runs Analysis End"

#------------------------------------------------------------------------------
def FindRuns (Coordinates,RunDistance,RunDuration,PixelRatio):

	i = 1
	Distance = []
	while i < len(Coordinates):
#		Distance.append ( Calculate2PointsDistance(
#				  Coordinates[i-1][2],Coordinates[i-1][3],\
#				  Coordinates[i][2],Coordinates[i][3],PixelRatio))
		Distance.append ( Calculate2PointsDeltaY(
                                  Coordinates[i-1][3],Coordinates[i][3],PixelRatio))
		i += 1

	j      = 0
	k      = 0
	Start  = 0
	Run    = []
	RunNum = 0
	Sign   = 0

	while j < len(Distance):
		if Distance[j] > 0: Sign = 1
		elif Distance[j] < 0: Sign = -1
		else: Sign = 0
		if Distance[j] <= RunDistance:
			Start = j+1
			k = j
			while k < len(Distance):
				if Distance[k] > RunDistance: 
					j = k
					RunNum += 1
					break
				if Distance[k] <= RunDistance:
					k += 1
					continue
			Run.append([Start,k,Sign])
		if k > j: break
		j += 1

	Runs = [];
	i    = 0
	while i < len(Run):
		if abs(Run[i][1]-Run[i][0]) >= (RunDuration-1):
			Runs.append([ Run[i][0],Run[i][1],Run[i][2] ])

		i += 1

	return Runs

#------------------------------------------------------------------------------
def FindPauses (Coordinates,PauseDistance,PauseDuration,PixelRatio):

        i = 1
        Distance = []
        while i < len(Coordinates):
#                Distance.append ( Calculate2PointsDistance(
#                                  Coordinates[i-1][2],Coordinates[i-1][3],\
#                                  Coordinates[i][2],Coordinates[i][3],PixelRatio))
		Distance.append ( Calculate2PointsDeltaY(
                                  Coordinates[i-1][3],Coordinates[i][3],PixelRatio))
                i += 1

        j      = 0
        k      = 0
        Start  = 0
        Pause    = []
        PauseNum = 0

        while j < len(Distance):
                if abs(Distance[j]) <= PauseDistance:
                        Start = j+1
                        k = j
                        while k < len(Distance):
                                if abs(Distance[k]) > PauseDistance:
                                        j = k
                                        PauseNum += 1
                                        break
                                if abs(Distance[k]) <= PauseDistance:
                                        k += 1
                                        continue
                        Pause.append([Start,k])
                if k > j: break
                j += 1

        Pauses = [];
        i    = 0
        while i < len(Pause):
                if (Pause[i][1]-Pause[i][0]) >= (PauseDuration-1):
                        Pauses.append([Pause[i][0],Pause[i][1]])
                i += 1

        return Pauses

#------------------------------------------------------------------------------
def CalculateAverageSpeedAndError (Values):

	j = 0
	SE_Speed_p = 0
	SE_Dist_p  = 0
	SE_Time_p  = 0
	SE_Mean_p  = 0
	SE_Num_p   = 0
	SE_p = 0
	SD_p = 0


	AverageSpeed = 0
	while j < len(Values):
	        print "--", Values[j]

		if( Values[j][2] == 1 ):
                	SE_Speed_p += Values[j][0]/Values[j][1]
                	SE_Num_p   += 1
        	j += 1

	SE_Mean_p = SE_Speed_p / SE_Num_p

	j = 0
	while j < len(Values):
		if( Values[j][2] == 1 ):
                	SE_p += (SE_Speed_p - SE_Mean_p)**2
		j += 1
	SE_p = SE_p / SE_Num_p
	SD_p = math.sqrt(SE_p)/math.sqrt(SE_Num_p)

	print "+_+", SE_p, SD_p


	return AverageSpeed
#------------------------------------------------------------------------------
def CalculateAverageSpeed (Coordinates,FrameRate):

	i = 1
	Speed = 0
	while i < len(Coordinates):
		Speed += Calculate2PointSpeed( \
				Coordinates[i-1][2],Coordinates[i-1][3],\
				Coordinates[i][2],Coordinates[i][3],FrameRate)
		i += 1
	AverageS = Speed / (i-1)
	return AverageS

#------------------------------------------------------------------------------
def Calculate2PointSpeed (X1,Y1,X2,Y2,Time):

	Speed = 0
	Distance = Calculate2PointsDistance(X1,Y1,X2,Y2)
	Speed = Distance / Time
        return Speed

#------------------------------------------------------------------------------
def CalculateAverageAngle (Coordinates):

        i = 1
        Angle = 0
        while i < len(Coordinates):                 
		Angle += Calculate2PointsAngle( \
				Coordinates[i-1][2],Coordinates[i-1][3],\
				Coordinates[i][2],Coordinates[i][3])
		i += 1
	AverageA = Angle / (i-1)
	return AverageA

#------------------------------------------------------------------------------
def Calculate2PointsAngle (X1,Y1,X2,Y2):

	try:
		Angle = math.atan( ( (Y2-Y1)*-1) / (X2-X1) )
	except ZeroDivisionError:
		Angle = 0
	Angle = (Angle * (180/math.pi))+90 
        return Angle

#------------------------------------------------------------------------------
def Calculate2PointsAngleNew (X1,Y1,X2,Y2):

	dx = float(X2 - X1)
	dy = float(Y2 - Y1)

	# Special angles (90, -90, 180, 0
	if (dy == 0):
                if (dx > 0):
                        Angle = 90
                else:
                        Angle = 270
        elif (dx == 0):
                if (dy > 0):
                        Angle = 0
                else:
                        Angle = 180
	# Non special angles
	else:
		if (dy < 0):
			if (dx > 0):
				Angle = ((abs(math.atan(dy/float(dx)) * \
					(180.0/math.pi) ) ) + 90)
			else:
				Angle = abs(math.atan(dy/float(dx)) * \
					(180.0/math.pi) )  + 180
		else:
			if (dx > 0):
				Angle = (math.atan(dx/float(dy)) * \
					(180.0/math.pi) )
			else:
				Angle = 360 - abs(math.atan(dx/float(dy)) * \
					(180.0/math.pi) ) #+ 270 
        return Angle

#------------------------------------------------------------------------------
def CalculateVectorMagnitude( InVector ):

	if(InVector[0] == 0) and (InVector[1] == 0):
                magnitude = 0
	else:
		#magnitude = Vector( InVector ).length()
		magnitude = na.linalg.norm( InVector )

	return magnitude

#------------------------------------------------------------------------------
def CalculateVectorAngle ( InVector ):

	if(InVector[0] == 0.0) and (InVector[1] == 0.0):
		Angle = 999.0
	else:
		#Angle = Vector([0,1]).angle(Vector(InVector))*(180.0/math.pi)
		v1_u =  [0,1]    / na.linalg.norm( [0,1] )
    		v2_u =  InVector / na.linalg.norm( InVector )
    		Angle =  na.arccos(na.clip(na.dot(v1_u, v2_u), -1.0, 1.0))
	
	# Special angles (90, -90, 180, 0
	if(InVector[0] == 0.0) and (InVector[1] == 0.0):
		#print "\tCASE= 1", Angle, 999
		Angle = 999.0
	elif(InVector[1] == 0.0):
		if (InVector[0] > 0.0):
		#	print "\tCASE=2A", Angle, 90
			Angle = 90.0
                else:
		#	print "\tCASE=2B", Angle, 270
                        Angle = 270.0
	elif(InVector[0] == 0.0):
                if (InVector[1] < 0.0):
		#	print "\tCASE=3A", Angle, 0	
                        Angle = 0.0
                else:
		#	print "\tCASE=3B", Angle, 180
                        Angle = 180.0
	#Add a correcting factor depending on which quadrant the vector is in
	else:
		if (InVector[1] < 0.0):
			if (InVector[0] > 0.0):
				if( (abs(InVector[1]) / InVector[0]) > 1.0):
					#print "\tCASE=4A", Angle
					Angle = 180.0-Angle
				else:	
				#	print "\tCASE=4B", Angle, (180 - abs(Angle))
					Angle = (180.0 - abs(Angle))	



			else:
				#print "\tCASE=4C", Angle, Angle+180
				Angle = Angle + 180.0
		else:
			if (InVector[0] > 0.0):
				#print "\tCASE=5A", Angle, (180 - Angle)
				Angle = (180.0 - Angle) 
			else:
				#print "\tCASE=5B", Angle, Angle+180
				Angle = Angle + 180.0   



	#normo = Vector.normal(Vector(InVector))
	#normo = Vector(InVector)
	#Angle2 = Vector([0,1]).angle(normo)*(180/math.pi)	
	#Angle2 = Angle2 + 90
	#if Angle2 > 360: Angle2 = Angle2 - 360

	if Angle == 360.0: Angle = 0.0

	Angle = round(Angle,3)

	return Angle

#------------------------------------------------------------------------------
def CalculateDirection(Angle):

	if(Angle >= 0)    and (Angle <=90):
		Direction = "Left"
		Status    = "Reversal"
        elif(Angle > 270) and (Angle <=360):
		Direction = "Right"
		Status    = "Reversal"
        elif(Angle > 90)  and (Angle <=180):
		Direction = "Left"
		Status    = "Continue"
        elif(Angle > 180) and (Angle <=270):
		Direction = "Right"
		Status    = "Continue"
        else: 
		Direction = "ERROR IN DIRECTION"
		Status    = "ERROR IN STATUS"

	return Status,Direction

#------------------------------------------------------------------------------
def CalculateDirectionRelative(Angle1,Angle2):


	Abs = abs(Angle1-Angle2)
#	Angle1 = Angle1 + 720;
#	Difference = (Angle1 - Angle2) % 360

	if Abs <= 90: 
		#print "\tGreater", " Diff=", Difference, "ABS+", Abs, "A1=", Angle1%360, "A2=",Angle2
		Status = "Continue"
	else:
		#print "\tLesser", " Diff=", Difference, "ABS+", Abs, "A1=", Angle1%360, "A2=",Angle2 
		Status = "Reversal"

#	Angle1 = Angle1 % 360

	return Status,Abs

#------------------------------------------------------------------------------
def CalculateAverageDistance (Coordinates,PixelRatio):

	i = 1
	Distance = 0
	while i < len(Coordinates):
		Distance += Calculate2PointsDistance(  
				Coordinates[i-1][2],Coordinates[i-1][3],\
				Coordinates[i][2],Coordinates[i][3],PixelRatio)
		i += 1
	Average = Distance / (i-1)
	return Average

#------------------------------------------------------------------------------
def Calculate2PointsDeltaY (Y1,Y2):

        Distance = Y2 - Y1
        return Distance

#------------------------------------------------------------------------------
def Calculate2PointsDistance (X1,Y1,X2,Y2):

	Distance = math.sqrt( abs(X1 - X2)**2 + abs(Y1 - Y2)**2 )
        return Distance

#------------------------------------------------------------------------------
def KymoSpeeds ( KWMeanL,KWMeanR,Type,LQ,HQ,PixelRatio,Times):

	PixelRatio = 1

	LQ = int(LQ)
	HQ = int(HQ)

	if Type == "middle":
		#LQ = int( 2.0 * (len(Times) / 8.0) )
		#HQ = int( 6.0 * (len(Times) / 8.0) )
		#LQ = 7
		#HQ = LQ + 10
		if HQ >= len(KWMeanL):
			HQ = len(KWMeanL)-1

		AveL = 0
		AveR = 0
		cnt  = 0
		i = LQ
		while i <= HQ:
			DL = abs( abs(KWMeanL[i-1])-abs(KWMeanL[i]))
			DR = abs( abs(KWMeanR[i-1])-abs(KWMeanR[i]))
			DL = DL / PixelRatio
			DR = DR / PixelRatio
			T  = Times[i]-Times[i-1]
			SL = DL/T
			SR = DR/T
			AveL += SL
			AveR += SR
			print "Point %3d %.2f %.2f %.2f %.2f %.2f %.2f %.2f"\
			      %(i,DL,DR,T,SL,SR,AveL,AveR), PixelRatio
			cnt  += 1
			i += 1
		AveL = AveL / cnt
		AveR = AveR / cnt
		Line = [ KWMean[LQ], LQ, KWMean[HQ], HQ ]

	elif Type == "middleregression":
                if HQ >= len(KWMeanL):
                        HQ = len(KWMeanL)-1
		CoordsL = []
		CoordsR = []
                i = LQ
                while i <= HQ:
			CoordsL.append([KWMeanL[i],i,0])
			CoordsR.append([KWMeanR[i],i,0])
			i += 1

		RegressionL = KymoRegression(CoordsL,0,1)
		RegressionR = KymoRegression(CoordsR,0,1)
		#RegressionL = Regression_CVersion(CoordsL,0,1)
		#RegressionR = Regression_CVersion(CoordsR,0,1)

		i = 0
		while i < len(CoordsL):
			CoordsL[i][2] = ((CoordsL[i][1]-RegressionL['Intercept']) / RegressionL['X'])
			CoordsR[i][2] = ((CoordsR[i][1]-RegressionR['Intercept']) / RegressionR['X'])
			i += 1

		Line   = [ [CoordsL[0][2],CoordsL[0][1],CoordsL[-1][2],CoordsL[-1][1]],\
			   [CoordsR[0][2],CoordsR[0][1],CoordsR[-1][2],CoordsR[-1][1]] ]
		AveL   = 60 * ((abs(CoordsL[-1][2]-CoordsL[0][2])*PixelRatio) / \
			 (( Times*CoordsL[-1][1]) - (Times*CoordsL[0][1]) ))

		AveR   = 60 * ((abs(CoordsR[-1][2]-CoordsR[0][2])*PixelRatio) / \
			 (( Times*CoordsR[-1][1]) - (Times*CoordsR[0][1]) ))

	elif Type == "regression":
		MidPoint = (len(KWMeanL) / 2)
		print "Midpoint=", MidPoint, len(KWMeanL)

		i = 1
		while i <= MidPoint:
			min    = MidPoint - i	
			max    = MidPoint + i
			Coords = []
			j      = min
			while j < max:
				Coords.append( [KWMeanL[j],Times[j]] )
				j += 1

			Regression = KymoRegression(Coords,0,1)
			print "\tReg=", min, max, Regression['R2']

			i += 1

	#Speed = [1,10,1.23,1.34]

	Speed = [Line,AveL,AveR] 

	return Speed

#------------------------------------------------------------------------------
def Regression_CVersion (Coords,X,Y):

	import linRegressFit
	import string

	pairs = []; 
	pairs.append( 0 )
	pairs.append( (len(Coords)-1) )
        Regression = {}

        i = 0
        while i < len(Coords):
                pairs.append(Coords[i][X])
                pairs.append(Coords[i][Y])
                i += 1

	rawResult = linRegressFit.calc(pairs)
	resTuple  = string.split(rawResult)

	Regression['X']         = float(resTuple[3])
	Regression['Intercept'] = float(resTuple[2])
	Regression['R2']        = float(resTuple[4])
	Regression['aR2']       = float(resTuple[4])

	return Regression

#------------------------------------------------------------------------------
def KymoRegression (Coords,X,Y):

	x = []; y =[]
        Regression = {}
        i = 0
        while i < len(Coords):
        	x.append(Coords[i][X])
                y.append(Coords[i][Y])
                i += 1

	r = robjects.r
	robjects.globalenv["roX"] = robjects.FloatVector( x )                
	robjects.globalenv["roY"] = robjects.FloatVector( y )

        stats = importr('stats')                       
        linear_model = stats.lm("roY ~ roX")           

        Regression['X']         = linear_model.rx2('coefficients')[1]
        Regression['Intercept'] = linear_model.rx2('coefficients')[0]
	Regression['R2']        = r.summary(linear_model)[7][0]
	Regression['aR2']       = r.summary(linear_model)[8][0]

	return Regression

#------------------------------------------------------------------------------
def KymoImageNoiseCorrection ( Type,SegThresh,ImageName,IMPixels,Sheet,MidPoint):

	im   = Image.open( ImageName )
	ImageNoiseL = []
	ImageNoiseR = []
	thresholdL  = 0
	thresholdR  = 0

	Data = []
	Sheet = 1

	#Normalise the intensity data
	Normalise = 0
	if Normalise:
                i = 0
                while i < len(Data[Sheet][5]):
			IntL = []
			IntR = []
			j = 0
                        while j < len(Data[Sheet][5][i]):
				if( j <= MidPoint):
                                        IntL.append( Data[Sheet][5][i][j][1])
                                else:
                                        IntR.append( Data[Sheet][5][i][j][1])
				j += 1
			j = 0
			while j < len(Data[Sheet][5][i]):
                                if( j <= MidPoint):
					Data[Sheet][5][i][j][1] = 100*(Data[Sheet][5][i][j][1]/\
								  max(IntL) )
				else:
					Data[Sheet][5][i][j][1] = 100*(Data[Sheet][5][i][j][1]/\
								  max(IntR) )
				j += 1
			i += 1

	# No noise correction selected, so just set noise to 0
	if(Type == "None"):
		i = 0
		while i < len(IMPixels[0]):
			ImageNoiseL.append( [0.0,0.0] )
			ImageNoiseR.append( [0.0,0.0] )	
			i += 1

	# The 2 edge pixels are taken from either RHS or LHS and the average
	# taken. This value represents noise then subtracted from all values
	# Seems to be a weak estimate, looking at the weighted mean values.
	elif(Type == "edge"):
		i = 0
	        while i < len(Data[Sheet][4]):
			try:		
				ImageNoiseL.append(((im.getpixel((0,i))+\
						   im.getpixel((1,i)))/2.0) )
			except:
	                        ImageNoiseL.append( 0.0 )
			try:
				ImageNoiseR.append(((im.getpixel(((im.size[0]-2),i))\
						   +im.getpixel(((im.size[0]-1),i)))/2.0)  )
			except:
				ImageNoiseR.append( 0.0 )
			i += 1

	# Estimate the Image noise by calculating the standard deviation of 
	# the intensities for each time point. Then disguard any data less 
	# than one standard deviation away from the mean
	elif(Type == "stddev"):
		ImageMeanL  = []
		ImageMeanR  = []	
		i = 0
                while i < len(Data[Sheet][5]):
			TmpL = []
			TmpR = []
			j = 0
			while j < len(Data[Sheet][5][i]):
				if( j <= MidPoint):	
					TmpL.append( Data[Sheet][5][i][j][1])
				else:
					TmpR.append( Data[Sheet][5][i][j][1])
				j += 1

			ImageMeanL.append( sum(TmpL)/len(TmpL) )
                        ImageMeanR.append( sum(TmpR)/len(TmpR) )

			StdDevL,ErrL = Standard_Dev_Error(TmpL)
			StdDevR,ErrR = Standard_Dev_Error(TmpR)
			ImageNoiseL.append( float((sum(TmpL)/len(TmpL)) - float(StdDevL)))
			ImageNoiseR.append( float((sum(TmpR)/len(TmpR)) - float(StdDevR)))

			#ImageNoiseL.append( float(StdDevL) ) 
                        #ImageNoiseR.append( float(StdDevR) )
			i += 1

	# Estimate the noise by first calculating edge maximum values, then
	# only take the top 95% intensities above the noise level. Equivalent
	# of segmenting the images.
	elif(Type == "segmented"):
		i = 0
                while i < len(IMPixels[i]):
                        try:
				#NoiseL = max( im.getpixel((0,i)),im.getpixel((1,i)),im.getpixel((2,i))  )
				NoiseL = max( IMPixels[0][i],IMPixels[1][i],IMPixels[2][i]  )
                        except:
                                NoiseL = 0.0 
                        try:
				NoiseR = max( IMPixels[-1][i],IMPixels[-2][i],IMPixels[-3][i] )
				#NoiseR = max( im.getpixel(((im.size[0]-1),i)),\
				#	      im.getpixel(((im.size[0]-2),i)),\
				#	      im.getpixel(((im.size[0]-3),i))  )
                        except:
                                NoiseR = 0.0

			TmpL = []
			TmpR = []
			j = 0
			while j < len(IMPixels):
				if( j < MidPoint):
					TmpL.append( IMPixels[j][i] )
				else:
					TmpR.append( IMPixels[j][i] )
				j += 1
			
			#print len(TmpL), max(TmpL), NoiseL, float(SegThresh), MidPoint,
			#print TmpL[0:5]

			thresholdL = ((max(TmpL)-NoiseL) * float(SegThresh) )
			thresholdR = ((max(TmpR)-NoiseR) * float(SegThresh) ) 

			ImageNoiseL.append( [NoiseL,thresholdL] )
                        ImageNoiseR.append( [NoiseR,thresholdR] )
                        i += 1

	elif(Type == "segmented_diag"):
		Step = 0
                i    = 0
                while i < len(IMPixels[i]):
			if i < (len(IMPixels[i])/2):
				MidT   = len(IMPixels[i])/2.0
				MidD   = len(IMPixels)/4.0
				NoiseL = max(IMPixels[int(MidD-Step-1)][i],\
					     IMPixels[int(MidD-Step)][i],\
					     IMPixels[int(MidD-Step+1)][i]  )	
				NoiseR = max(IMPixels[int((3*MidD)+Step-2)][i],\
                                             IMPixels[int((3*MidD)+Step-1)][i],\
                                             IMPixels[int((3*MidD)+Step-0)][i]  )
				Step  += MidD/MidT

			else:
				NoiseL = max( IMPixels[0][i],IMPixels[1][i],IMPixels[2][i]  )
                	        NoiseR = max( IMPixels[-1][i],IMPixels[-2][i],IMPixels[-3][i] )

                        TmpL = []
                        TmpR = []
                        j = 0
                        while j < len(IMPixels):
                                if( j < MidPoint):
                                        TmpL.append( IMPixels[j][i] )
                                else:
                                        TmpR.append( IMPixels[j][i] )
                                j += 1

                        thresholdL = ((max(TmpL)-NoiseL) * float(SegThresh) )
                        thresholdR = ((max(TmpR)-NoiseR) * float(SegThresh) )

                        ImageNoiseL.append( [NoiseL,thresholdL] )
                        ImageNoiseR.append( [NoiseR,thresholdR] )
                        i += 1

        elif(Type == "normalised"):
                print "ERROR: Noise correction type '"+str(Type)+\
                      "' Not yet implemented"
                sys.exit(0)

        elif(Type == "movingaverage"):
                print "ERROR: Noise correction type '"+str(Type)+\
                      "' Not yet implemented"
                sys.exit(0)

	elif(Type == "gaussian"):
		print "ImageName", ImageName

        	import ImageFilter
		import ImageOps
		import numpy
		import numarray
		import numpy.numarray.nd_image
		from numarray.nd_image import gaussian_filter1d
		import os.path

		size=3
		rank=1

		(I_N,I_E) = os.path.splitext( os.path.basename(ImageName) )

        	im.save(I_N+"_original.png","PNG")
		I  = numpy.asarray(Image.open(ImageName))

		sigmaval = 0.0
		while sigmaval < 2:
			II = numarray.nd_image.gaussian_filter(I, sigma=sigmaval,\
							       order=0 )
			Image.fromarray(numpy.uint8(II)).save(I_N+"_npy_gaussian_1_"+\
							      str(sigmaval)+"_Filter.png")
			sigmaval += 0.01


		size = 1
		footprint = [ [0,0],[0,1],[size,1],[size,0] ]  
		while size < 10:
			J = numarray.nd_image.median_filter(I, footprint=footprint )
			Image.fromarray(numpy.uint8(J)).save(I_N+"_npy_median_1_"+\
							     str(size)+"_Filter.png")

			K = numarray.nd_image.minimum_filter1d(I, size=size )
			Image.fromarray(numpy.uint8(K)).save(I_N+"_npy_minimum1d_1_"+\
						     str(size)+"_Filter.png")
			L = numarray.nd_image.maximum_filter1d(I, size=size )
	                Image.fromarray(numpy.uint8(L)).save(I_N+"_npy_maximum1d_1_"+\
        	                                             str(size)+"_Filter.png")

			size += 1


	#Apply the ImageNoise Correction to Data
	i = 0
        #Time Points
        while i < len(IMPixels[0]):
        	j = 0
                #Rows
                while j < len(IMPixels):
                	if(j <= MidPoint):
                        	ImageNoise = ImageNoiseL[i][0]
				Threshold  = ImageNoiseL[i][1]
                        else:
                                ImageNoise = ImageNoiseR[i][0]
				Threshold  = ImageNoiseR[i][1]

                        if(IMPixels[j][i] >= (ImageNoise+Threshold)):
#				print i, j, Data[Sheet][5][i][j][1], ImageNoise+Threshold,	
	
				IMPixels[j][i] = (IMPixels[j][i] - ImageNoise)
				IMPixels[j][i] = (IMPixels[j][i] - Threshold )
                        else:
#				print i, j, Data[Sheet][5][i][j][1], ImageNoise+Threshold,
                                IMPixels[j][i] = 0.0
#				print Data[Sheet][5][i][j][1] 
                        j += 1
		i += 1

	return IMPixels,ImageNoiseL,ImageNoiseR

#------------------------------------------------------------------------------
def KymoMean( DistInt ):

	DistMean   = 0
        IntMean    = 0
	Distances  = 0
	Intensties = 0

	i = 0
        while i < len(DistInt):
		Distances  += DistInt[i][0]
                Intensties += DistInt[i][1]
                i += 1

	DistMean = Distances  / len(DistInt)
	IntMean  = Intensties / len(DistInt)

	return DistMean,IntMean

#------------------------------------------------------------------------------
def KymoWeightedMean( Int, Start, TP, Mid, PixelRatio ):

	KWMean      = 0
	Weights     = 0
	Distances   = 0
	Intensities = 0

	if Start == 0:		
		End = Mid
	elif Start == Mid: 	
		End = len(Int)

	i = Start
	while i < End:
		if Start == 0:		Dist = Mid - i 
		elif Start == Mid:	Dist = i -Mid

		Intensities += Int[i][TP]
		Weights +=  Int[i][TP] * (Dist * PixelRatio)
		i += 1

	try:
		KWMean = Weights/Intensities
	except ZeroDivisionError:
                KWMean = 0

	return KWMean

#------------------------------------------------------------------------------
def KymoWeightedMeanAverager(KWMeans):

	Tmp = []
	i = 0
	while i < len(KWMeans):
		j = 0
		while j < len(KWMeans[i]):
			k = 0
			while k < len(KWMeans[i][j]):
				Tmp.append( [i,j,k,KWMeans[i][j][k]] )
				k += 1
			j += 1
		i += 1

	KWMeansAve = []
	i = 0
	while i < len(KWMeans):
		Aves       = []
		j = 0
	        while j < 100:
			Individual = []
			k = 0
			while k < len(Tmp):
				if(Tmp[k][0] == i) and (Tmp[k][2] == j):
					Individual.append( float(Tmp[k][3]) )
				k += 1
			if len(Individual) > 2:
				Aves.append( sum(Individual)/len(Individual) )
			j += 1
		KWMeansAve.append( Aves )
		i += 1

	return KWMeansAve

#------------------------------------------------------------------------------
def KymoWeightedVariance ( Int, Start, TP, Mid, PixelRatio ):

        KWMean      = KymoWeightedMean( Int, Start, TP, Mid, PixelRatio  )
        Weights     = 0
        KWVariance  = 0
        Intensities = 0

        if Start == 0:
                End = Mid
        elif Start == Mid:
                End = len(Int)

        i = Start
        while i < End:
                if Start == 0:          Dist = Mid - i
                elif Start == Mid:      Dist = i - Mid

                Intensities += Int[i][TP]
                Weights     += Int[i][TP] * pow(( (Dist*PixelRatio) - KWMean), 2)
                i += 1

        try:
                KWVariance = Weights/Intensities
        except ZeroDivisionError:
                KWVariance = 0

	KWStdDev   = math.sqrt(KWVariance)

	return KWVariance, KWStdDev

#------------------------------------------------------------------------------
def KymoWeightedSkewKurt( DistInt ):

	KWMean              = KymoWeightedMean( DistInt )
	KWVariance,KWStdDev = KymoWeightedVariance( DistInt )

	KWSkew      = 0
	KWKurt      = 0
	SkewWeights = 0
	KurtWeights = 0

	i = 0
        while i < len(DistInt):
                SkewWeights += pow( ( DistInt[i][0] - KWMean ), 3)
		KurtWeights += pow( ( DistInt[i][0] - KWMean ), 4)

                i += 1	

	try:
		KWSkew = SkewWeights / ( (len(DistInt)-1) * pow(KWStdDev,3) )
	except ZeroDivisionError:
		KWSkew = 0
	try:
		KWKurt = KurtWeights / ( (len(DistInt)-1) * pow(KWStdDev,4) )
		KWKurt = KWKurt - 3 
	except ZeroDivisionError:
		KWSkew = 0

	KWSkewSumm = "none"
	if(KWSkew > 0):
		KWSkewSumm = "right"
	elif(KWSkew < 0):
		KWSkewSumm = "left"
	KWKurtSumm = "none"
        if(KWKurt > 0):
                KWKurtSumm = "peaked"
        elif(KWKurt <= 0):
                KWKurtSumm = "flat"


	return KWSkew,KWKurt,KWSkewSumm,KWKurtSumm

#------------------------------------------------------------------------------
def CalculatePowerset(seq):
# Returns all the subsets/ordered permutations of seq

    if len(seq) <= 1:
        yield seq
        yield []
    else:
        for item in powerset(seq[1:]):
            yield [seq[0]]+item
            yield item

#------------------------------------------------------------------------------
def getMedian(numericValues):

	theValues = sorted(numericValues)

	if len(theValues) % 2 == 1:
		return theValues[(len(theValues)+1)/2-1]
	else:
		lower = theValues[len(theValues)/2-1]
		upper = theValues[len(theValues)/2]

	return (float(lower + upper)) / 2

# 
# Smallest enclosing circle - Library (Python)
# 
# Copyright (c) 2017 Project Nayuki
# https://www.nayuki.io/page/smallest-enclosing-circle
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with this program (see COPYING.txt and COPYING.LESSER.txt).
# If not, see <http://www.gnu.org/licenses/>.
# 

import math, random


# Data conventions: A point is a pair of floats (x, y). A circle is a triple of floats (center x, center y, radius).

# 
# Returns the smallest circle that encloses all the given points. Runs in expected O(n) time, randomized.
# Input: A sequence of pairs of floats or ints, e.g. [(0,5), (3.1,-2.7)].
# Output: A triple of floats representing a circle.
# Note: If 0 points are given, None is returned. If 1 point is given, a circle of radius 0 is returned.
# 
# Initially: No boundary points known
def make_circle(points):
	# Convert to float and randomize order
	shuffled = [(float(x), float(y)) for (x, y) in points]
	random.shuffle(shuffled)
	
	# Progressively add points to circle or recompute circle
	c = None
	for (i, p) in enumerate(shuffled):
		if c is None or not is_in_circle(c, p):
			c = _make_circle_one_point(shuffled[ : i + 1], p)
	return c


# One boundary point known
def _make_circle_one_point(points, p):
	c = (p[0], p[1], 0.0)
	for (i, q) in enumerate(points):
		if not is_in_circle(c, q):
			if c[2] == 0.0:
				c = make_diameter(p, q)
			else:
				c = _make_circle_two_points(points[ : i + 1], p, q)
	return c


# Two boundary points known
def _make_circle_two_points(points, p, q):
	circ = make_diameter(p, q)
	left = None
	right = None
	px, py = p
	qx, qy = q
	
	# For each point not in the two-point circle
	for r in points:
		if is_in_circle(circ, r):
			continue
		
		# Form a circumcircle and classify it on left or right side
		cross = _cross_product(px, py, qx, qy, r[0], r[1])
		c = make_circumcircle(p, q, r)
		if c is None:
			continue
		elif cross > 0.0 and (left is None or _cross_product(px, py, qx, qy, c[0], c[1]) > _cross_product(px, py, qx, qy, left[0], left[1])):
			left = c
		elif cross < 0.0 and (right is None or _cross_product(px, py, qx, qy, c[0], c[1]) < _cross_product(px, py, qx, qy, right[0], right[1])):
			right = c
	
	# Select which circle to return
	if left is None and right is None:
		return circ
	elif left is None:
		return right
	elif right is None:
		return left
	else:
		return left if (left[2] <= right[2]) else right


def make_circumcircle(p0, p1, p2):
	# Mathematical algorithm from Wikipedia: Circumscribed circle
	ax, ay = p0
	bx, by = p1
	cx, cy = p2
	ox = (min(ax, bx, cx) + max(ax, bx, cx)) / 2.0
	oy = (min(ay, by, cy) + max(ay, by, cy)) / 2.0
	ax -= ox; ay -= oy
	bx -= ox; by -= oy
	cx -= ox; cy -= oy
	d = (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by)) * 2.0
	if d == 0.0:
		return None
	x = ox + ((ax * ax + ay * ay) * (by - cy) + (bx * bx + by * by) * (cy - ay) + (cx * cx + cy * cy) * (ay - by)) / d
	y = oy + ((ax * ax + ay * ay) * (cx - bx) + (bx * bx + by * by) * (ax - cx) + (cx * cx + cy * cy) * (bx - ax)) / d
	ra = math.hypot(x - p0[0], y - p0[1])
	rb = math.hypot(x - p1[0], y - p1[1])
	rc = math.hypot(x - p2[0], y - p2[1])
	return (x, y, max(ra, rb, rc))


def make_diameter(p0, p1):
	cx = (p0[0] + p1[0]) / 2.0
	cy = (p0[1] + p1[1]) / 2.0
	r0 = math.hypot(cx - p0[0], cy - p0[1])
	r1 = math.hypot(cx - p1[0], cy - p1[1])
	return (cx, cy, max(r0, r1))


_MULTIPLICATIVE_EPSILON = 1 + 1e-14

def is_in_circle(c, p):
	return c is not None and math.hypot(p[0] - c[0], p[1] - c[1]) <= c[2] * _MULTIPLICATIVE_EPSILON


# Returns twice the signed area of the triangle defined by (x0, y0), (x1, y1), (x2, y2).
def _cross_product(x0, y0, x1, y1, x2, y2):
	return (x1 - x0) * (y2 - y0) - (y1 - y0) * (x2 - x0)

#------------------------------------------------------------------------------
# FIN
#------------------------------------------------------------------------------
