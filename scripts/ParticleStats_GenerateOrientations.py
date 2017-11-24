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
import numarray as na
import random
import ParticleStats_Maths as PS_Maths
import ParticleStats_Inputs as PS_Inputs

###############################################################################
# MAIN CODE STARTS HERE
###############################################################################

print "Running", sys.argv[0]
print

Movies = ['GF2T',  'GF5T',  'GF6T',  'GF7T', 'GF8T', 'GF9T', 'GF10T','GF11BT', 
          'GF11T', 'GF12BT','GF12T', 'gf14', 'GF15T','GF16T','GF17T','GF18T', 
          'GF20T', 'GF23T', 'GF46T', 'GF51T','GF56T','GF57T','GF58T',
          'GF59T', 'GF60T', 'GF62T', 'GF65T', 
          'osk3',  'osk7',  'os1t',  'os2t', 'os6t', 'os12t','os15t','osk5t','osk6t' ]

Angles = ['31' ,  '2',    '185',  '261',  '183', '40',  '294', '344',
          '344',  '155',  '155',  '155',  '28',  '6',   '290', '129',
          '58',   '140',  '178',  '65',   '150', '262', '262', '262',
          '358',  '358',  '276',  '112',
          '1','1','1','1','1','1','1','1','1' ]

i = 0
while i < len(Movies):
	X1 = 20.00
	Y1 = 20.00

	CorrectedAngle = (int(Angles[i])+90)%360

	X2,Y2 = PS_Maths.GetCircleEdgeCoords(X1,Y1,int(CorrectedAngle),10) 

	print str(Movies[i])+",99,00:00.0,00:00.0,No Label,0,0,"+\
	      str("%.4f"%X1)+","+\
	      str("%.4f"%Y1)+","+\
	      "99,0,0,0,0,0,0,0" 
	print str(Movies[i])+",99,00:00.0,00:00.0,No Label,0,0,"+\
              str("%.4f"%X2)+","+\
              str("%.4f"%Y2)+","+\
              "99,0,0,0,0,0,0,0"
	i += 1

###############################################################################
# FIN
###############################################################################
