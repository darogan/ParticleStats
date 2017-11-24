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

import os,sys,math,os.path
import numpy as na
from optparse import OptionParser

###############################################################################
# PARSE IN THE USER OPTIONS 
###############################################################################

parser = OptionParser(usage="%prog [-x Excel [-t tif] [-s squares]",
                      version="%prog 0.1")

parser.add_option("--txt1", metavar="TXTFILE1",
                  dest="TxtFile1",
                  help="Text file 1 containing tab separated vector values")

parser.add_option("--txt2", metavar="TXTFILE2",
                  dest="TxtFile2",
                  help="Text file 2 containing tab separated vector values")

(options, args) = parser.parse_args()

###############################################################################
# LOAD IN THE REQUIRED MODULES ONLY AFTER MAIN USER OPTIONS CHECKED
###############################################################################

import ParticleStats_Maths   as PS_Maths

print "Running", sys.argv[0]
print

(O_Dir1,O_File1) = os.path.split(options.TxtFile1)
(O_Name1,O_Ext1) = os.path.splitext(O_File1)

TrailFile1       = open(options.TxtFile1,'r')
LineCount1       = len( open(options.TxtFile1,'r').readlines() )
TrailVectorsAll_1 = []
for line1 in TrailFile1:
	line1 = line1.rstrip('\n')
        element1 = line1.split('\t')
        TrailVectorsAll_1.append( [float(element1[0]),float(element1[1])] )
TrailFile1.close()



(O_Dir2,O_File2) = os.path.split(options.TxtFile2)
(O_Name2,O_Ext2) = os.path.splitext(O_File2)

TrailFile2       = open(options.TxtFile2,'r')
LineCount2       = len( open(options.TxtFile2,'r').readlines() )
TrailVectorsAll_2 = []
for line2 in TrailFile2:
        line2 = line2.rstrip('\n')
        element2 = line2.split('\t')
        TrailVectorsAll_2.append( [float(element2[0]),float(element2[1])] )
TrailFile2.close()

import rpy2.robjects as robjects
import rpy2.rpy_classic as rpy
from rpy2.robjects import r

r.library("CircStats")

Angle1   = []
Radians1 = []
Mags1    = []
i = 0
while i < len(TrailVectorsAll_1):
	Angle1.append( float(PS_Maths.CalculateVectorAngle( TrailVectorsAll_1[i] ) ) )
        Radians1.append( float(((math.pi/180)*PS_Maths.CalculateVectorAngle( TrailVectorsAll_1[i] ))) )
        Mags1.append( PS_Maths.CalculateVectorMagnitude( TrailVectorsAll_1[i] ))
        i += 1
rRadians1  = robjects.FloatVector(Radians1)

Angle2   = []
Radians2 = []
Mags2    = []
i = 0
while i < len(TrailVectorsAll_2):
        Angle2.append( float(PS_Maths.CalculateVectorAngle( TrailVectorsAll_2[i] ) ) )
        Radians2.append( float(((math.pi/180)*PS_Maths.CalculateVectorAngle( TrailVectorsAll_2[i] ))) )
        Mags2.append( PS_Maths.CalculateVectorMagnitude( TrailVectorsAll_2[i] ))
        i += 1
rRadians2  = robjects.FloatVector(Radians2)




circ_mean1 = robjects.r['circ.mean'](rRadians1)
print "+ 1 Circular Mean: %.2f"%(robjects.r['deg'](circ_mean1)[0]), " degrees ",
print "(rho = %.2f)"%(robjects.r['circ.summary'](rRadians1)[2][0])

circ_mean2 = robjects.r['circ.mean'](rRadians2)
print "+ 2 Circular Mean: %.2f"%(robjects.r['deg'](circ_mean2)[0]), " degrees ",
print "(rho = %.2f)"%(robjects.r['circ.summary'](rRadians2)[2][0])


robjects.r['watson.two'](rRadians1,rRadians2,plot="true")


#        print "-------------------------------------------------------------"
#        print "+ Circular Mean: %.2f"%(robjects.r['deg'](circ_mean)[0]), " degrees ",
#        print "(rho = %.2f)"%(robjects.r['circ.summary'](rRadians)[2][0])
#        print "+ Circular Dispersion:  n=%d r=%.2f rbar=%.2f var=%.2f"%( \
#              robjects.r['circ.disp'](rRadians)[0][0],\
#              robjects.r['circ.disp'](rRadians)[1][0],\
#              robjects.r['circ.disp'](rRadians)[2][0],\
#              robjects.r['circ.disp'](rRadians)[3][0])
#        print "+ Rayleigh test of uniformity: rbar=%.2f pvalue=%.2e"%(\
#               robjects.r['r.test'](rRadians)[0][0],\
#               robjects.r['r.test'](rRadians)[1][0])
#        print "+ est.kappa: %.2f"%(robjects.r['est.kappa'](rRadians)[0])
#        print "+", robjects.r['kuiper'](rRadians)
#        print "+", robjects.r['watson'](rRadians, dist="uniform")
#        print "+", robjects.r['watson'](rRadians, dist="vm")
#        print "-------------------------------------------------------------"




print "Finished", sys.argv[0]

#------------------------------------------------------------------------------
# FIN
#------------------------------------------------------------------------------
