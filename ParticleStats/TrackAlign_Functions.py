#!/usr/bin/env python
###############################################################################
#   _____               _       _    _ _                                      # 
#  |_   _| __ __ _  ___| | __  / \  | (_) __ _ _ __                           #
#    | || '__/ _` |/ __| |/ / / _ \ | | |/ _` | '_ \                          #
#    | || | | (_| | (__|   < / ___ \| | | (_| | | | |                         #
#    |_||_|  \__,_|\___|_|\_\_/   \_\_|_|\__, |_| |_|                         #
#                                        |___/                                #
#                                                                             #
###############################################################################
#       TrackAlign: Open source software for the analysis of tracked data     #
#                   to determine optimal parameters and alignment of tracks   #
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

import numpy as na
import os,sys,math,re,random
from numpy import dot
from numpy.linalg import norm
import ParticleStats.ParticleStats_Maths as PS_Maths

#------------------------------------------------------------------------------
def SignificanceScore(RawScore,Xi,Mu,Sigma):
# Calculate the significance score based on the probability distribution 
# function (PDF)

	if Xi == 0:
		tx = math.exp( (-1*(RawScore-Mu))/Sigma )
	else:	
		#if RawScore > 0:
			#print "==============", (1+(Xi*((RawScore-Mu)/Sigma)))
			#print "______________", (-1/Xi), RawScore

		if (1+(Xi*((RawScore-Mu)/Sigma))) < 0:
			tx = math.pow( (1+(Xi*((RawScore-Mu)/Sigma))), int(-1/Xi) )
		else:
			tx = math.pow( (1+(Xi*((RawScore-Mu)/Sigma))), (-1/Xi) )

	Significance = (1/Sigma) * math.pow(tx,Xi+1) * math.exp((-1*tx))

	return Significance

#------------------------------------------------------------------------------
def FormatAlignment (CoordsR,CoordsC,M_R,M_C):


	#print "MINMAX=", min(M_R), max(M_R)
	if( min(M_R) != 0 ):
		FP = ""
		i = 0
		while i < min(M_R):
			FP += "*" 
			i += 1
	#	print "FP\t", FP

	if( max(M_R) < len(CoordsR)):
		EP = ""
		i = 0
		while i < len(CoordsR):
			EP += "*"
			i += 1
	#	print "EP\t", EP


	# Make some arrays for the reference and compare seqs
	S_R   = []
        k = 0
        while k < len(CoordsR):
        	S_R.append("-")
                k += 1
	S_C   = []
        k = 0
        while k < len(CoordsC):
                S_C.append("-")
                k += 1

	# mark where the matches occur
        k = 0
        while k < len(M_R):
		if M_R[k] != "-":
			S_R[M_R[k]] = "+"
                k += 1
	k = 0
        while k < len(M_C):
		if M_C[k] != "-":
                	S_C[M_C[k]] = "+"
                k += 1

	#Pad start of the sequence if necessary
	Dot = [" "]
	if   M_R[0] < M_C[0]:
		S_R = (Dot*(M_C[0]-M_R[0])) + S_R
	elif M_R[0] > M_C[0]:
                S_C = (Dot*(M_R[0]-M_C[0])) + S_C

	#Pad the end of the seqences of necessary
	if len(S_R) > len(S_C):
		S_C = S_C + (Dot*(len(S_R)-len(S_C)))
	if len(S_C) > len(S_R):
                S_R = S_R + (Dot*(len(S_C)-len(S_R)))

	#Convert to a simple string
        AlnR = ""
        k = 0
        while k < len(S_R):
	        AlnR += S_R[k] 
                k += 1

	AlnC = ""
        k = 0
        while k < len(S_C):
                AlnC += S_C[k]       
                k += 1


	return AlnR,AlnC

#------------------------------------------------------------------------------
def TrailBoundaryCalculation (xy,xLim,yLim,xMargin,yMargin):
# For the algorithm speed up, puts a box around the reference track to limit 
# the search space. Also needs a time restriction component!

	boundary = []
	minX = xy[0][0]; minY = xy[0][1]; 
	maxX = xy[0][0]; maxY = xy[0][1];

	i = 0
	while i < len(xy):
		if xy[i][0] > maxX:  maxX = xy[i][0]
		if xy[i][1] > maxY:  maxY = xy[i][1]
		if xy[i][0] < minX:  minX = xy[i][0]
                if xy[i][1] < minY:  minY = xy[i][1]
		i += 1

	if((maxX+xMargin) > xLim): maxX = xLim
	else:                      maxX = maxX + xMargin
	if((maxY+yMargin) > yLim): maxY = yLim
	else:                      maxY = maxY + yMargin
	if((minX-xMargin) < 0):    minX = 0
	else:                      minX = minX - xMargin
	if((minY-yMargin) < 0):    minY = 0
	else:                      minY = minY - yMargin

	boundary.append([minX,minY])
	boundary.append([maxX,minY])
	boundary.append([maxX,maxY])
	boundary.append([minX,maxY])
	boundary.append([minX,minY])

	return boundary

#------------------------------------------------------------------------------
def TrailTimeOverlap(FrameR,FrameC,TimeTol):
# Calculate whether the trails overlap in time before moving onto the more
# costly distance calculations

	# Add some tolerance buffer for the matching
	# Tolderance 1 menas add one frame to start AND end
	# Make a copy as we don't want to actually extend the lists
	FR = []; FR.extend(FrameR)
	FC = []; FC.extend(FrameC)

	if int(TimeTol) > 0:	
		i = 0
		while i < TimeTol:
			if min(FR) > 0: 
				FR.insert(0, (min(FR)-(i+1) ) )
				FR.append( (max(FR)+1) )
			if min(FC) > 0:
				FC.insert(0,(min(FC)-(i+1) ))
				FC.append( (max(FC)+1) )
			i += 1

	RSet    = set(FR)
	CSet    = set(FC)
	Overlap = len ( list( RSet & CSet  ) )

	return Overlap

#------------------------------------------------------------------------------
def TrailSimilarityScore (Coords_R,Coords_C,Frames_R,Frames_C,Flatten,gD,gE):

	MinusInf = -2111111111
	#gD       = 10
	#gE       = 1

	FromM  = 0
	FromIx = 1
	FromIy = 2

	# Initialisation of the scoring matrices
	M  = na.zeros([(len(Coords_R)+1),(len(Coords_C)+1)],na.float64)
	Ix = na.zeros([(len(Coords_R)+1),(len(Coords_C)+1)],na.float64)
	Iy = na.zeros([(len(Coords_R)+1),(len(Coords_C)+1)],na.float64)
	i = 0
	while i < (len(Coords_R)+1):
		j = 0
		while j < (len(Coords_C)+1):
			Ix[i][j] = MinusInf
			Iy[i][j] = MinusInf
			j += 1
		i += 1
	# Initialisation of the traceback matrix
	B = na.zeros([3,3,(len(Coords_R)+1),(len(Coords_C)+1)],na.float64)

	#Smith-Waterman algorithm
	i = 1
        while i < (len(Coords_R)+1):
                j = 1
                while j < (len(Coords_C)+1):
			Similarity = PointSimilarity( Coords_R[i-1],Coords_C[j-1],\
						      Frames_R[i-1],Frames_C[j-1],\
						      Flatten )
			# For the Matrix
			a = 0
			b = M[i-1][j-1]  + Similarity
			c = Ix[i-1][j-1] + Similarity			
			d = Iy[i-1][j-1] + Similarity
			val      = max(a,b,c,d)
                        M[i][j]  = val
			if( val == b ): B[FromM][0][i][j]  = 1
			if( val == c ): B[FromIx][0][i][j] = 1
			if( val == d ): B[FromIy][0][i][j] = 1

			# For gap inserts in X
			a = M[i][j-1]  - gD
			b = Ix[i][j-1] - gE
			c = Iy[i][j-1] - gD
			val      = max(a,b,c)
			Ix[i][j] = val	
			if( val == a ): B[FromM][1][i][j]  = 1
			if( val == b ): B[FromIx][1][i][j] = 1
			if( val == c ): B[FromIy][1][i][j] = 1

			# For gap inserts in Y
			a = M[i-1][j]  - gD
			b = Iy[i-1][j] - gE
			c = Ix[i-1][j] - gD
			val      = max(a,b,c)
			Iy[i][j] = val
			if( val == a ): B[FromM][2][i][j]  = 1
                        if( val == b ): B[FromIy][2][i][j] = 1
                        if( val == c ): B[FromIx][2][i][j] = 1

                        j += 1
                i += 1

	# Start the Tracebacks, by finding the largest score
	superMax = 0
	i = 1
        while i < (len(Coords_R)+1):
                j = 1
                while j < (len(Coords_C)+1):
                       superMax = max(superMax,M[i][j],Ix[i][j],Iy[i][j])
                       j += 1
		i += 1

	# Traceback be finding where the largest score came from - update B
	iMax = 0
	jMax = 0
	kMax = 0
	i = 1
        while i < (len(Coords_R)+1):
                j = 1
                while j < (len(Coords_C)+1):
			if superMax == M[i][j]:
				MarkReachable_SW(B,0,i,j)
				kMax = 0
				iMax = i
				jMax = j
			if superMax == Ix[i][j]:
				MarkReachable_SW(B,1,i,j)
                                kMax = 1
                                iMax = i
                                jMax = j
			if superMax == Iy[i][j]:
				MarkReachable_SW(B,2,i,j)
                                kMax = 2
                                iMax = i
                                jMax = j
			j += 1
                i += 1

	#PrintMatrices(Coords_R,Coords_C,M,Ix,Iy)

	# More traceback to find out what aligns to what
	(Aligned_R,Aligned_C) = Traceback_SW(Coords_R,Coords_C,B,kMax,iMax,jMax)

	return (superMax,Aligned_R,Aligned_C)

#------------------------------------------------------------------------------
def PrintMatrices(Coords_R,Coords_C,M,Ix,Iy):
# For debugging - prints out the matrices 
	i = 1
        while i < (len(Coords_R)+1):
		print "M %3d - "%i,
                j = 1
                while j < (len(Coords_C)+1):
			print "%3d "%M[i][j],
			j += 1
		print
		i += 1

	print

	i = 1
        while i < (len(Coords_R)+1):
                print "Ix%3d - "%i,
                j = 1
                while j < (len(Coords_C)+1):
                        print "%3d "%Ix[i][j], 
                        j += 1
                print
                i += 1

	print

	i = 1
        while i < (len(Coords_R)+1):
                print "Iy%3d - "%i,
                j = 1
                while j < (len(Coords_C)+1):
                        print "%3d "%Iy[i][j],
                        j += 1
                print
                i += 1

	return 1

#------------------------------------------------------------------------------
def Traceback_SW(Coords_R,Coords_C,B,kMax,iMax,jMax):
# Traceback through the backtrack matrix to find where the higestes scores are
# them assemble the matching tracks 
	Aligned_R = []
	Aligned_C = []

	while( (B[0][kMax][iMax][jMax] != 0) or \
	       (B[1][kMax][iMax][jMax] != 0) or \
	       (B[2][kMax][iMax][jMax]) ):

		if   B[2][kMax][iMax][jMax]:
			B[2][kMax][iMax][jMax] = 3
			nexttk = 2
		elif B[1][kMax][iMax][jMax]:
                        B[1][kMax][iMax][jMax] = 3
			nexttk = 1
		elif B[0][kMax][iMax][jMax]:
                        B[0][kMax][iMax][jMax] = 3
			nexttk = 0
		
		if   kMax == 0:
			Aligned_R.append( (jMax-1) )
			Aligned_C.append( (iMax-1) )
			iMax = (iMax-1)
			jMax = (jMax-1)
		elif kMax == 1:
			Aligned_R.append( (jMax-1) )
                        Aligned_C.append( "-" ) #GAP
			jMax = (jMax-1)
		elif kMax == 2:
			Aligned_R.append( "-" ) #GAP
                        Aligned_C.append( (iMax-1) )
			iMax = (iMax-1)

		kMax = nexttk

	# Need to reverse the Aligned lists
	Aligned_R.reverse()
        Aligned_C.reverse()

	return (Aligned_C,Aligned_R)

#------------------------------------------------------------------------------
def MarkReachable_SW (B,matrix,i,j):
# Update the B matrix with the maximum values for the traceback
	x = 0
	while x < 3:
		if(B[x][matrix][i][j] == 1):
			B[x][matrix][i][j] = 2

			if matrix == 0:		# in the M matrix
				MarkReachable_SW(B,matrix,i-1,j-1)
			elif matrix == 1:	# in the Ix matrix
				MarkReachable_SW(B,matrix,i-1,j)
			elif matrix == 2:       # in the Iy matrix
				MarkReachable_SW(B,matrix,i,j-1)
		x += 1
	return 1

#------------------------------------------------------------------------------
def PointSimilarity (CoordsR,CoordsC,FrameR,FrameC,Flatten):

	# Calculate the distance between the 2 point
	# Assumes an exponential decay of matching score
	Dist = PS_Maths.Calculate2PointsDistance(CoordsR[0],CoordsR[1],\
						 CoordsC[0],CoordsC[1])

	#Similarity  = (math.exp(-0.25 * Dist)) 

	MaxDist = 724.0
	#Similarity  = ((((MaxDist - Dist) / MaxDist ) * 2.0 ) - 1.0)
	Similarity = 15 - (Dist*Dist)

	if Similarity < -10:
		Similarity = -10

	#print "+++ Distance=", Dist, "+++ Similarity=", Similarity

	if Flatten:
		TSimilarity = 1
	else:
		# Calculate the time distance between points - no of frames
		TDist       = abs( FrameR - FrameC )
		TSimilarity = (math.exp(-0.25 * TDist))

	#return (Similarity*TSimilarity)
	return Similarity

#------------------------------------------------------------------------------
def CoordinatePointInterpolation (x1,y1,x2,y2,tm,tc):
# Function takes 2 points ans determines if there are any full integer points
# in between the points

	InnerCoords = []

	if(x1 < x2):
	# moving right
		for x in range(int(x1),int(x2)):
                        y = ((tm * x) + tc)
			if(x != int(x1) and x != int(x2)):
				InnerCoords.append([x,y])

	elif(x1 > x2):
	# Moving left
		for x in range(int(x2),int(x1)):
                        y = ((tm * x) + tc)
			if(x != int(x1) and x != int(x2)):
				InnerCoords.append([x,y])

	elif(x1 == x2) and (y1 < y2):
	# not moving on x, but moving down
		for y in range(int(y1),int(y2)):
			x = x1
			if(x != int(x1) and x != int(x2)):
				InnerCoords.append([x,y])

	elif(x1 == x2) and (y1 > y2):
	# not moving on x, but moving up
		for y in range(int(y2),int(y1)):
                        x = x1
			if(x != int(x1) and x != int(x2)):
				InnerCoords.append([x,y])

	return InnerCoords

#------------------------------------------------------------------------------
def DefineAssignmentArray (Coords):

	i = 0
	while i < len(Coords):

		i += 1

	return ScoringArray

#------------------------------------------------------------------------------
def VectorCosineSimilarity (v1, v2):

	v1=doc_vec(doc1)
	v2=doc_vec(doc2)
	print "Similarity: %s" % float(dot(v1,v2) / (norm(v1) * norm(v2)))

#------------------------------------------------------------------------------
def ConvertCoordinateFormat (InCoords,Interpolate):

	Coords = []
	Frames = []
	i = 0
	while i < len(InCoords):
	        xy    = []
	        frame = []
	        j = 0
	        while j < len(InCoords[i]):
	                if(j > 0 and Interpolate):
	                        dx,dy,tm,tc = PS_Maths.CalculateEquationOfLine(\
	                                        [InCoords[i][j-1][4],\
	                                         InCoords[i][j-1][5],\
	                                         InCoords[i][j][4],\
	                                         InCoords[i][j][5] ])
	                        InnerCoords = CoordinatePointInterpolation(\
	                                         InCoords[i][j-1][4],\
	                                         InCoords[i][j-1][5],\
	                                         InCoords[i][j][4],\
	                                         InCoords[i][j][5],tm,tc )
	                        if len(InnerCoords) > 0:
	                                k = 0
	                                while k < len(InnerCoords):
        	                                xy.append( [InnerCoords[k][0],InnerCoords[k][1]] )
	                                        frame.append( InCoords[i][j][1] )
                	                        k += 1
	                xy.append([InCoords[i][j][4],InCoords[i][j][5]])
	                frame.append(InCoords[i][j][1])
	                j += 1
	        Coords.append(xy)
	        Frames.append(frame)
	        i += 1
	xy    = []
	frame = []

	return Coords, Frames

#------------------------------------------------------------------------------
def CompareTracks (Coords_R, Coords_C, Frames_R, Frames_C, boundary, \
		   BoundaryFilter,FlattenTime,gapOpen,gapExt,TimeTol):

	Similarity = 0
	Cross      = 1
	A_R        = []
	A_C        = []

	if BoundaryFilter:
	        k = 1
		while k < len(Coords_C):
			Cross = 0
	                TOverlap = TrailTimeOverlap(Frames_R,Frames_C,TimeTol)
	                if((TOverlap > 0) or (FlattenTime)):
	                	Cross,Line,Debug = PS_Maths.LineWithinSquare(boundary,\
	                                                    [Coords_C[k-1][0],\
	                                                     Coords_C[k-1][1],\
	                                                     Coords_C[k][0],\
	                                                     Coords_C[k][1]],1)
			if Cross:
                		(Similarity,A_R,A_C) = TrailSimilarityScore(\
                        	                                  Coords_R,Coords_C,\
                                	                          Frames_R,Frames_C,\
                                        	                  FlattenTime,gapOpen,gapExt)
        	                break
			k += 1
	else:
		(Similarity,A_R,A_C) = TrailSimilarityScore(\
                                                  Coords_R,Coords_C,\
                                                  Frames_R,Frames_C,\
                                                  FlattenTime,gapOpen,gapExt)

	return (Similarity,A_R,A_C,Cross)

#------------------------------------------------------------------------------
def CalculateEVDParameters (MaxSimilarities):

#	from rpy2.robjects.packages import importr 
#	import rpy2.rpy_classic as rpy
#	import rpy2.robjects as robjects
#	from rpy2.robjects import r
	# Create an R object of sorted scores
#	maxsims = robjects.FloatVector( sorted(MaxSimilarities) )
	# MLE Estimates using "ismev" package
#	r.library("ismev")
#	gev_fit = robjects.r['gev.fit'](maxsims)
	#Mu = location, Sigma = scale, Xi = shape
#	Mu    = gev_fit[6][0] 
#	Sigma = gev_fit[6][1]
#	Xi    = gev_fit[6][2]
	#Standard errors for the Mu, Sigma and Xi
#	eMu    = gev_fit[8][0]
#	eSigma = gev_fit[8][1]
#	eXi    = gev_fit[8][2]
#	print "baseR: ", Xi,Mu,Sigma,eXi,eMu,eSigma

	i = 0
	while i < len(MaxSimilarities):
		print i, " -- ", MaxSimilarities[i], " == ",
		if(MaxSimilarities[i] == 0):
			MaxSimilarities[i] = 1
		print MaxSimilarities[i]
		i += 1

	from scipy.stats import genextreme
	import warnings
	with warnings.catch_warnings():
		warnings.simplefilter("ignore")
		gev_shape,gev_loc,gev_scale = genextreme.fit( sorted(MaxSimilarities) )	

	print "scipy: shape=", gev_shape, " loc=", gev_loc, " scale=", gev_scale

	Xi     = abs(gev_shape)
	Mu     = gev_loc
	Sigma  = gev_scale
	eXi    = 0
	eMu    = 0
	eSigma = 0

	return (Xi,Mu,Sigma,eXi,eMu,eSigma)

#------------------------------------------------------------------------------
def GenerateRandomCoords (Coords,Frames,Type,ntrails,imagesize,NoiseAmount,\
			  AngMin,AngMax,MagMin,MagMax,FraMin,FraMax):

	RandCoordsAll = []

	# Same as input coord set but add some noise
	if Type == "InputWithNoise":
	        i = 0
	        while i < len(Coords):
			RandCoords = []
	                j = 0
	                while j < len(Coords[i]):
	                	Noise = random.uniform( (-1*NoiseAmount),NoiseAmount )
	                        X1 = Coords[i][j][0] + Noise
	                        Y1 = Coords[i][j][1] + Noise
	                        if(X1 > 0 and Y1 > 0 and X1 < imagesize and \
	                           Y1 < imagesize):
					RandCoords.append([j+1,X1,Y1,1,Frames[i][j],"randomimage.tif"])
        	                else:
                	                j -= 1
        	                j += 1
			RandCoordsAll.append(RandCoords)
                	i += 1

	# In this case take the parameters from the original input file
	if Type == "InputWithRandom":
        	AngRange = []; MagRange = []; FraRange = []
		i = 0
	        while i < len(Coords):
			MagRange.append(PS_Maths.Calculate2PointsDistance(\
                       	                Coords[i][0][0],Coords[i][0][1],\
                               	        Coords[i][-1][0],Coords[i][-1][1]))
	                AngRange.append(PS_Maths.CalculateVectorAngle([\
       	                                Coords[i][-1][0]-Coords[i][0][0],\
               	                        Coords[i][-1][1]-Coords[i][0][1]]))
                	i += 1

		i = 0
		while i < len(Frames):
			FraRange.append(Frames[i][0])
			i += 1

	        FraMin = min(FraRange); FraMax = max(FraRange)
	        AngMin = min(FraRange); AngMax = max(AngRange)
		MagMin = min(FraRange); MagMax = max(MagRange)

	# Tracks generated to user parameters or taken from the original file	
	if Type == "Random" or Type == "InputWithRandom":
	        i = 0
	        while i < int(ntrails):
			RandCoords = []
	                Ang      = random.uniform(AngMin,AngMax)
	                Mag      = random.uniform(MagMin,MagMax)
	                Fra      = random.randrange(FraMin,FraMax)
	                FraStart = random.randrange(0,(100-Fra))
	                X1       = random.uniform(0,imagesize)
	                Y1       = random.uniform(0,imagesize)
	                X2,Y2 = PS_Maths.GetCircleEdgeCoords(X1,Y1,Ang,Mag)

	                if(X1 > 0 and Y1 > 0 and X1 < imagesize and \
	                   Y1 < imagesize and X2 > 0 and Y2 > 0 and \
	                   X2 < imagesize and Y2 < imagesize ):
				RandCoords.append([i+1,X1,Y1,1,FraStart,"randomimage.tif"])
        	                j = 1
	                        while j <= Fra:
        	                        X2,Y2 = PS_Maths.GetCircleEdgeCoords(X1,Y1,Ang,(Mag/Fra))
                	                if(X2 > 0 and Y2 > 0 and X2 < imagesize and \
                        	           Y2 < imagesize ):
						RandCoords.append([i+1,X1,Y1,1,FraStart+j,\
								   "randomimage.tif"])
                                        	X1 = X2
						Y1 = Y2
	                                else:
	                                        j -= 1
	                                j += 1
				RandCoordsAll.append(RandCoords)
	                else:
	                        i -= 1
	                i += 1

	Stats = [Type,ntrails,imagesize,NoiseAmount,\
                 AngMin,AngMax,MagMin,MagMax,FraMin,FraMax]

	return (RandCoordsAll,Stats)

#------------------------------------------------------------------------------
def PlotMatchingTrails (OutName,IMSize,ImageName,Query,Hits,HitList,Colours,\
						Polygon,PolygonColour):

	OutName = OutName+"_Hits"
	scene   = Scene(OutName,IMSize[0],IMSize[1])

	scene.add( SVGImage(IMSize[0],IMSize[1],ImageName))

	PolygonColour = ColourConvert( PolygonColour )
        polypoints = ""
        if( len(Polygon) > 2):
                i = 0
                while i < len(Polygon):
                        polypoints += str(Polygon[i][0])+","+\
                                      str(Polygon[i][1])+" "
                        i += 1
                scene.add( PolygonShape((polypoints),(255,255,255),\
                                        0,PolygonColour,1,3) )

	print "QUE:", Query[0][4], Query[0][5], Query[-1][4], Query[-1][5]
        i = 0
        while i < len(HitList):
		print "SUB:", i, HitList[i], Hits[HitList[i]][0][4], Hits[HitList[i]][0][5], Hits[HitList[i]][-1][4], Hits[HitList[i]][-1][5]
		i += 1


	i = 0
	while i < len(Hits):
		print "sub:", i, Hits[i][0][4], Hits[i][0][5], Hits[i][-1][4], Hits[i][-1][5]
		i += 1

	# Print the reference trail in black, with green/red circles at ends

	scene.add(Circle((Query[0][4],Query[0][5]),1,0,0,(0,255,0),0.5))
	scene.add(Line((Query[0][4],Query[0][5]), (Query[-1][4], Query[-1][5]),(255,0,0),1,0.5))
	scene.add(Circle((Query[-1][4], Query[-1][5]),1,0,0,(255,0,0),0.5))

#	i = 0
#	while i < len(Results[0][0]):
#		if i == 0:
#			scene.add(Circle((Results[0][0][i][0],Results[0][0][i][1]),1,0,0,(0,255,0),0.5))
		#if i == (len(Results[0][0])-1):
		#	scene.add(Circle((Results[0][0][i][0],Results[0][0][i][1]),\
		#				1,0,0,(255,0,0),0.5))
#		if i > 0:
#			scene.add(Line((Results[0][0][i-1][0],Results[0][0][i-1][1]),\
#					(Results[0][0][i][0],Results[0][0][i][1]),\
#					(255,0,0),1,0.5))
#		i += 1

	# Print the matching trails
	i = 1
	while i < len(HitList):
		RGB = ColourConvert(Colours[i])

		j = 0
		while j < len(Hits[HitList[i]]):

			if j == 0:
				scene.add(Circle((Hits[HitList[i]][j][4], Hits[HitList[i]][j][5]),0.5,0,0,(0,255,0),0.5))
			if j == (len(Hits[HitList[i]])-1):
				scene.add(Circle((Hits[HitList[i]][j][4], Hits[HitList[i]][j][5]),0.5,0,0,(255,0,0),0.5))
			if j > 0:
				scene.add(Line((Hits[HitList[i]][j-1][4],Hits[HitList[i]][j-1][5]),\
                               (Hits[HitList[i]][j][4],  Hits[HitList[i]][j][5]),\
                                         (RGB[0],RGB[1],RGB[2]),0.5,0.5))
			j += 1

		i += 1

#	i = 1
#	while i < len(Results):
#		RGB = ColourConvert(Colours[i])
#		j = 0
#		while j < len(Results[i][0]):
#			if j == 0:
#				scene.add(Circle((Results[i][0][j][0],Results[i][0][j][1]),\
#					  0.5,0,0,(0,255,0),0.5))
#			#if j == (len(Results[i][0])-1):
#			#	scene.add(Circle((Results[i][0][j][0],Results[i][0][j][1]),\
#			#		  0.5,0,0,(255,0,0),0.5))
#			if j > 0:
#				scene.add(Line((Results[i][0][j-1][0],Results[i][0][j-1][1]),\
#                                        (Results[i][0][j][0],Results[i][0][j][1]),\
#                                         (RGB[0],RGB[1],RGB[2]),0.5,0.5))
#			j += 1
#
#		i += 1
		
	scene.write_svg()


	return OutName

#------------------------------------------------------------------------------
def Print_Welcome ( Mode, Size ):

	print "   _____               _        _    _ _              " 
	print "  |_   _| __ __ _  ___| | __   / \  | (_) __ _ _ __   "
	print "    | || '__/ _` |/ __| |/ /  / _ \ | | |/ _` | '_ \  "
	print "    | || | | (_| | (__|   <  / ___ \| | | (_| | | | | "
	print "    |_||_|  \__,_|\___|_|\_\/_/   \_\_|_|\__, |_| |_| "
	print "                                         |___/        "
	print "                 by Russell S. Hamilton         2017  "

#------------------------------------------------------------------------------
def ColourConvert(Colours):

        RGB = []
        if   Colours == "red":          RGB = (255,0,0)
        elif Colours == "blue":         RGB = (0,0,255)
        elif Colours == "green":        RGB = (0,255,0)
        elif Colours == "brown":        RGB = (165,42,42)
        elif Colours == "gold":         RGB = (255,215,0)
        elif Colours == "maroon":       RGB = (128,0,0)
        elif Colours == "purple":       RGB = (160,32,240)
        elif Colours == "orange":       RGB = (255,165,0)
        elif Colours == "yellow":       RGB = (255,255,0)
        elif Colours == "silver":       RGB = (230,232,250)
        elif Colours == "cyan":         RGB = (0,255,255)
        elif Colours == "magenta":      RGB = (255,0,255)
        elif Colours == "white":        RGB = (255,255,255)
        elif Colours == "black":        RGB = (0,0,0)
        elif Colours == "darkgreen":    RGB = (0,100,0)
        elif Colours == "steelblue":    RGB = (70,130,180)
        elif Colours == "orchid":       RGB = (218,112,214)
        elif Colours == "darkviolet":   RGB = (148,0,211)
        elif Colours == "salmon":       RGB = (250,128,114)
        elif Colours == "grey":         RGB = (84,84,84)
        else:   RGB = (0,0,0)

        return RGB[0],RGB[1],RGB[2]

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

class Line:
    def __init__(self,start,end,color,opacity,width):
        self.start   = start   #xy tuple
        self.end     = end     #xy tuple
        self.color   = color
        self.opacity = opacity
        self.width   = width
        return
    def strarray(self):
        return ["  <line x1=\"%d\" y1=\"%d\" x2=\"%d\" y2=\"%d\" style=\"stroke:rgb%s;stroke-opacity:%s;stroke-width:%f\" />\n" %(self.start[0],self.start[1],self.end[0],self.end[1],self.color,self.opacity,self.width)]


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

#------------------------------------------------------------------------------
# FIN
#------------------------------------------------------------------------------
