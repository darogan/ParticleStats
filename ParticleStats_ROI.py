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

import sys,os
import Tkinter
import Image, ImageTk
from optparse import OptionParser

###############################################################################
# PARSE IN THE USER OPTIONS 
###############################################################################
parser = OptionParser(usage="%prog -img <image>",
                      version="%prog 0.1")

parser.add_option("--img",
                  dest="img", metavar="IMG",
                  help="Provide the image for the ROI creation")
parser.add_option("--out",
                  dest="out", metavar="OUT",default="polygon.txt",
                  help="Provide the filename for the ROI coordinated output")

(options, args) = parser.parse_args()

if( os.path.exists(str(options.img)) != 1):
        print "ERROR: Image file --img does not exists - check correct path and name"
        sys.exit(0)




print "Running",sys.argv[0]

pointcnt = 0
Points   = []

#im = Image.open("imagy_1024_co.png")
#FileName = "interactive.gif" #"imagy_256_co.gif"
im = Image.open(options.img)

root = Tkinter.Tk()
root.title("ParticleStats_ROI")

c = Tkinter.Canvas(root,width=im.size[0],height=im.size[1],background= 'gray')
c.pack()

print "Image Size =", im.size[0], im.size[1]

photo = Tkinter.PhotoImage(file=options.img)
c.create_image(im.size[0]/2,im.size[1]/2, image = photo)

def mouseMove(event):
	print c.canvasx(event.x), c.canvasy(event.y)

def MakePolygon(event):
	global pointcnt
	global Points

	Points.append( [c.canvasx(event.x), c.canvasy(event.y)] )

	print "\t", pointcnt, \
              "[",c.canvasx(event.x), \
              ", ",c.canvasy(event.y),"]" \

	X1 = Points[len(Points)-2][0]
        Y1 = Points[len(Points)-2][1]

	if(pointcnt > 0):
		c.create_line(c.canvasx(event.x),c.canvasy(event.y),\
                	      X1,Y1,fill='green',width='1')
	pointcnt += 1

#def Clikkk(event):
#	print "Clikkk", c.canvasx(event.x), c.canvasy(event.y)
#	c.create_line(0,0,c.canvasx(event.x),c.canvasy(event.y),\
#                      fill='red',width='1')

#def Clikkkk(event):
#        print "Clikkkk", c.canvasx(event.x), c.canvasy(event.y)
#        c.create_line(0,0,c.canvasx(event.x),c.canvasy(event.y),\
#                      fill='black',width='1')
#	global Points
#	Loc = PS_Maths.CalculatePointInPolygon([c.canvasx(event.x), c.canvasy(event.y)],Points)
#	print "In Square =", Loc
	#root.quit()

def Quit(event):
	root.quit()

c.bind('<Button-1>', MakePolygon)
c.bind('<Button-3>', Quit)
#c.bind('<Button-3>', Clikkkk)
root.mainloop()


outputfile = open(options.out,'w')
i = 0
while i < len(Points):
	outty =  str(i) + " " +str(Points[i]) + "\n"
	outputfile.write( outty )
	i += 1
outputfile.close()

print "Polygon coordinates written to", options.out

print "Finished",sys.argv[0]
