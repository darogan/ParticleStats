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

import os,sys,math,os.path,re
from optparse import OptionParser
###############################################################################
# PARSE IN THE USER OPTIONS 
###############################################################################

parser = OptionParser(usage="%prog -xls1 <Excel>",
                      version="%prog 0.1")

parser.add_option("-o", "--outputtype", metavar="OUTPUTTYPE",
                  dest="OutputType", default="text",
                  help="print text ot html style output: DEFAULT=text")
parser.add_option("-n","--noise",
                  dest="Noise", metavar="NOISE",
		  default="None",
                  help="Correct for noise <None/segmented/edge/segmented_diag>")
parser.add_option("-t","--threshold",
                  dest="Threshold", metavar="THRESHOLD",
                  default="0.10",
                  help="Provide a cut off for the segmented threshold 0.10 = top 90% intensity above noise")
parser.add_option("--speed_start",
                  dest="speed_start", metavar="SPEED_START",
                  default="6",
                  help="Provide a time point start point for speed calculations")
parser.add_option("--speed_end",
                  dest="speed_end", metavar="SPEED_END",
                  default="18",
                  help="Provide a time point end point for speed calculations")
parser.add_option("-x", "--xls", metavar="EXCELFILE",
                  dest="ExcelFile",
                  help="Name of Excel File")
parser.add_option("--pixelratio", metavar="PIXELRATIO",
                  dest="PixelRatio", default=0.15, 
                  help="Pixel Ratio (nm per pixel): Default=0.15")
parser.add_option("--TimeInterval", metavar="TIMEINTERVAL",
                  dest="TimeInterval", default=5, 
                  help="Time Interval between data collection point in kymograph: Default=5secs")
parser.add_option("--tiffdir", metavar="TIFFDIR",
                  dest="TiffDir",
                  help="Specify a directory containing the kymograph tiff files")
parser.add_option("--outdir", metavar="OUTPUTDIR",
                  dest="OutputDir",
                  help="Specify a directory for the output files")
parser.add_option("--outhtml", metavar="OUTPUTHTML",
                  dest="OutputHTML",
                  help="Specify a web location for the HTML output")

(options, args) = parser.parse_args()


#ERROR CHECK

if( options.Noise and options.Noise != "edge" and \
    options.Noise != "None" and options.Noise != "segmented" and \
    options.Noise != "segmented_diag" \
  ):
	print "ERROR: Noise type not correctly specified <None/segmented/edge>"
        sys.exit(0)

###############################################################################
# LOAD IN THE REQUIRED MODULES ONLY AFTER MAIN USER OPTIONS CHECKED
###############################################################################

import numpy as na
import glob
import ParticleStats.ParticleStats_Maths          as PS_Maths
import ParticleStats.ParticleStats_Inputs         as PS_Inputs
import ParticleStats.ParticleStats_Plots          as PS_Plots
import ParticleStats.ParticleStats_Outputs        as PS_Outputs
from PIL import Image

Colours = ["red","blue","green","cyan","orange","yellow",\
           "silver","purple","brown","magenta","black","gold"]
Colours = Colours * 100

FontSize_Titles = 2
FontSize_Text   = 1

if(options.OutputType == "html"):
	PS_Outputs.Print_HTMLHeaders()
PS_Outputs.Print_Welcome(options.OutputType,FontSize_Text)

if(options.OutputDir):
        BaseDir = str(options.OutputDir)
else:
        BaseDir = ""

#if(options.OutputType == "html"):
#        print "\n\n<TABLE WIDTH=690 BGCOLOR=white "+\
#              "STYLE='border:1px;border-style:dashed;border-color:grey;'>"+\
#              "<TR><TD BGCOLOR=white COLSPAN=1><FONT FACE='sans,arial' SIZE=1><PRE>"

print "Running", sys.argv[0]

KWMeanL_AllExcel  = []
KWMeanR_AllExcel  = []
ImagesSizesExcel  = []
KWSpeeds_AllExcel = []
Data = []

if options.ExcelFile:
	# For if the data is nicely given in an Excel file... 
	(ExcelDir,ExcelFile) = os.path.split(options.ExcelFile)
	print " + Excel File            =", ExcelFile
	Data = PS_Inputs.ReadExcelKymographs2(options.ExcelFile)
	print " + Number of Sheets      =", len(Data) 
else:
	# For if the data is given on command line + sub directories
	print " + Pixel Ratio           =", options.PixelRatio
	print " + Image File Location   =", options.TiffDir
	Files = os.listdir(options.TiffDir)
	ImgSubDir = []
	i = 0
	while i < len(Files):
		(FileName,FileExt) = os.path.splitext(Files[i])
		PatternDir = re.compile(r'\ASet([0-9])')

		if PatternDir.search( FileName ) and len(FileExt) < 1:
			ImgSubDir.append(FileName)
		i += 1
	ImgSubDir.sort()

	i = 0
        while i < len(ImgSubDir):
		Files = os.listdir(options.TiffDir+"/"+ImgSubDir[i])
		cnt = 0
		DataTmp = []
		j = 0
		while j < len(Files):
			(FileName,FileExt) = os.path.splitext(Files[i])

			if FileExt == ".tif" or FileExt == ".jpg" or \
			   FileExt == ".gif" or FileExt == ".png" or \
			   FileExt == ".jpeg" or FileExt == ".tiff":
				DataTmp.append( [Files[j],float(options.TimeInterval),float(options.PixelRatio)]  )
				cnt += 1
			j += 1
		print " + Image Data Set", i+1, "     =", ImgSubDir[i], "(No. Images="+str(cnt)+")"
		Data.append ( [ImgSubDir[i],DataTmp] )
		i += 1

print " + Noise Correction Type =", options.Noise
print " + Noise Threshold       =", options.Threshold

KWMeanL_All       = []
KWMeanR_All       = []
KWSpeeds_All      = []
All_AveSpeeds     = []
All_PixelRatios   = []
All_TimeIntervals = []
SheetNames        = []
i = 0
while i < len(Data):
	KWMeanL_All   = []
	KWMeanR_All   = []
	PixelRatios   = []
	TimeIntervals = []
	AveSpeeds     = []
	ImageSizes    = []
	print " + Sheet                 =", (i+1), Data[i][0]
	SheetNames.append(Data[i][0])
	j = 0
	while j < len(Data[i][1]):
		if options.ExcelFile:
			ImageFile = str(options.TiffDir)+"/"+Data[i][1][j][0]
		else:
			ImageFile = str(options.TiffDir)+"/"+ImgSubDir[i]+"/"+Data[i][1][j][0]

		if( os.path.exists(str(ImageFile)) != 1):
			print "\t+ ERROR: MISSING IMAGE", ImageFile,\
			      "- will use missing.tif!!!"
			ImageFile = "Raquel/missing.tif"
		im = Image.open(ImageFile).convert("RGBA")
		ImageSizes.append( im.size )

		print "  +-----------------------------------------------------------"
		print "  + Image Name        =", Data[i][1][j][0]
		print "  + Image Size        =", im.size
		print "  + Pixel Ratio       =", Data[i][1][j][2]
		print "  + Time Interval     =", Data[i][1][j][1] 

		PixelRatios.append( Data[i][1][j][2] )
		TimeIntervals.append( Data[i][1][j][1] )
		#IMPixels = na.zeros([im.size[0],im.size[1]],na.Float64)
		IMPixels = na.zeros([im.size[0],im.size[1]],dtype=na.float64)
		x = 0
		while x < im.size[0]:
			y = 0
			while y < im.size[1]:
				R,G,B,O = im.getpixel((x,y))
				IMPixels[x][y] = ((R / 255.0) * 100.0)
				y += 1
			x += 1

		DataMidPoint = int( im.size[0]/2 )
	        print "  + Data Mid Point    =", DataMidPoint
		IMPixels,ImageNoiseL,ImageNoiseR = PS_Maths.KymoImageNoiseCorrection(\
							options.Noise,options.Threshold,\
							ImageFile,IMPixels,i,DataMidPoint)

		KWMeanL       = []
		KWMeanR       = []
		KWVarStdDevL  = []
		KWVarStdDevR  = []
		KWVarSkewKurL = []
		KWVarSkewKurR = []

		#Time Points
		y = 0
		while y < len(IMPixels[0]):
			
			outputfile = open(str(BaseDir)+"/ps_kymo.data",'a')
			outty = "";
			if (Data[i][1][j][1]*(y) == 60) or (Data[i][1][j][1]*(y) == 90):
				outty = outty + (str(Data[i][1][j][0])+"\t"+\
					str(Data[i][1][j][1]*(y))+\
					"\t%6.2f"%(PS_Maths.KymoWeightedMean(\
					IMPixels,0,y,DataMidPoint,Data[i][1][j][2]))+"\t")
				t = 0
				while t < DataMidPoint:
					outty = outty + (str(IMPixels[t][y])+"\t")
					t += 1
				outty = outty + "\n";

				outty = outty + (str(Data[i][1][j][0])+\
					"\t"+str(Data[i][1][j][1]*(y))+\
					"\t%6.2f"%(PS_Maths.KymoWeightedMean(\
                                        IMPixels,DataMidPoint,y,DataMidPoint,Data[i][1][j][2]))+"\t")
				t = DataMidPoint
                                while t < len(IMPixels):
                                        outty = outty + (str(IMPixels[t][y])+"\t")
                                        t += 1
				outty = outty + "\n"
			outputfile.write(outty)
			outputfile.close()

			print "    + Time %-3d"%(y+1),"(t=%-3d)"%(Data[i][1][j][1]*(y)),
			KWMeanL.append( PS_Maths.KymoWeightedMean(\
                                                IMPixels,0,y,DataMidPoint,Data[i][1][j][2]) )
                        KWMeanR.append( PS_Maths.KymoWeightedMean(\
                                                IMPixels,DataMidPoint,y,DataMidPoint,Data[i][1][j][2]) )

			print "W Mean %6.2f %6.2f"%(KWMeanL[-1],KWMeanR[-1]),
			print "Threshold %6.2f %6.2f"%(ImageNoiseL[y][1],ImageNoiseR[y][1]),
			print "Noise %6.2f %6.2f"%(ImageNoiseL[y][0],ImageNoiseR[y][0])

			KWVarStdDevL.append( PS_Maths.KymoWeightedVariance(\
						IMPixels,0,y,DataMidPoint,Data[i][1][j][2]) )	
			KWVarStdDevR.append( PS_Maths.KymoWeightedVariance(\
						IMPixels,DataMidPoint,y,DataMidPoint,Data[i][1][j][2]) )	
			#KWVarSkewKurL.append( PS_Maths.KymoWeightedSkewKurt(\
			#			Data[i][5][j][0:DataMidPoint] ))
			#KWVarSkewKurR.append( PS_Maths.KymoWeightedSkewKurt(\
			#			Data[i][5][j][DataMidPoint:]  ))
			y += 1

		KWMeanL_All.append( KWMeanL ) 
		KWMeanR_All.append( KWMeanR )
		KWSpeeds = PS_Maths.KymoSpeeds(KWMeanL,KWMeanR,"middleregression",\
					       options.speed_start,options.speed_end,\
					       Data[i][1][j][2],Data[i][1][j][1])

		KWSpeeds_All.append(KWSpeeds[1])
		KWSpeeds_All.append(KWSpeeds[2])

		print "  + Kymo Ave Speed    = L %.2f R %.2f Ave %.2f"%\
			(KWSpeeds[1],KWSpeeds[2],((KWSpeeds[1]+KWSpeeds[2])/2.0)) 
		AveSpeeds.append( ((KWSpeeds[1]+KWSpeeds[2])/2.0) )

		KymoSpeedPlot = PS_Plots.PlotKymoSpeeds(("kymo_"+str(i)+"-"\
							+str(j)+"_"+\
							str(options.Noise)),\
							KWMeanL,KWMeanR,\
							KWSpeeds,\
							ImageFile,Data[i][1][j][2],str(options.OutputDir))

		print "  + Kymo Speed        =", KymoSpeedPlot+".svg"
	        convert = "inkscape --export-png="+str(options.OutputDir)+"/"+KymoSpeedPlot+\
			  ".png --export-dpi=500 "+str(options.OutputDir)+"/"+KymoSpeedPlot+".svg 2>/dev/null"
		os.popen(convert)
		print "  + Kymo Speed        =", KymoSpeedPlot+".png"
	
		KymoPic = PS_Plots.PlotKymoWeighted(("kymo_"+str(i)+"-"\
						     +str(j)+"_"+\
						     str(options.Noise)),\
						     KWMeanL,KWMeanR,\
						     KWVarStdDevL,KWVarStdDevR,\
						     ImageFile,Data[i][1][j][2],str(options.OutputDir))	
		print "  + KymoWeighted      =", KymoPic+".svg"
		convert = "inkscape --export-png="+str(options.OutputDir)+"/"+KymoPic+\
			  ".png --export-dpi=500 "+str(options.OutputDir)+"/"+KymoPic+".svg 2>/dev/null"
		os.popen(convert)
		print "  + KymoWeighted      =", KymoPic+".png"

		if(options.OutputType == "html"):
			print "<UL><TABLE><TR>\n", \
			      "<TD><FONT FACE=sans,arial SIZE=1>\n", \
                              "<IMG SRC='"+str(options.OutputHTML)+\
			      "/"+str(options.OutputDir)+"/"+KymoPic+".png' ", \
                              "WIDTH=200 BORDER=0><BR>", \
                              "<A HREF='"+str(options.OutputHTML)+\
			      "/"+str(options.OutputDir)+"/"+KymoPic+".png' ", \
                              "STYLE='TEXT-DECORATION: NONE' target='_blank'>[PNG]", \
                              "<A HREF='"+str(options.OutputHTML)+\
			      "/"+str(options.OutputDir)+"/"+KymoPic+".svg' ", \
                              "STYLE='TEXT-DECORATION: NONE' target='_blank'>[SVG]</TD>\n", \
			      "<TD><FONT FACE=sans,arial SIZE=1>\n", \
                              "<IMG SRC='"+str(options.OutputHTML)+\
			      "/"+str(options.OutputDir)+"/"+KymoSpeedPlot+".png' ", \
                              "WIDTH=200 BORDER=0><BR>", \
                              "<A HREF='"+str(options.OutputHTML)+\
			      "/"+str(options.OutputDir)+"/"+KymoSpeedPlot+".png' ", \
                              "STYLE='TEXT-DECORATION: NONE' target='_blank'>[PNG]", \
                              "<A HREF='"+str(options.OutputHTML)+\
			      "/"+str(options.OutputDir)+"/"+KymoSpeedPlot+".svg' ", \
                              "STYLE='TEXT-DECORATION: NONE' target='_blank'>[SVG]</TD>\n", \
			      "</TR></TABLE></UL>\n"
		j += 1
		
	All_AveSpeeds.append( AveSpeeds )

	ImagesSizesExcel.append( ImageSizes )
	KWMeanL_AllExcel.append( KWMeanL_All )
	KWMeanR_AllExcel.append( KWMeanR_All )
	KWSpeeds_AllExcel.append( KWSpeeds_All )
	All_PixelRatios.append( PixelRatios )
	All_TimeIntervals.append( TimeIntervals )

	Montage = 0
	if Montage == 1:
		print "\t+ Kymo Speed Montage =", "kymo_montage_sheet_"+str(i)+".png"
		convert = "montage -tile 3x -geometry 75% kymo_"+str(i)+\
			  "-*_kymospeeds.png kymo_montage_sheet_"+str(i)+".png "
		os.popen(convert)

		print "\t+ Kymo Speed Montage =", "kymo_montage_WM_sheet_"+str(i)+".png"
        	convert = "montage -tile 3x -geometry 75% kymo_"+str(i)+\
                	  "-*_weightedMean.png kymo_montage_WM_sheet_"+str(i)+".png"
        	os.popen(convert)
        i += 1

print "+-----------------------------------------------------------"
print "+ Summary:"

Figures = []
Selection_All = []
Selection = []
i = 0
while i < len(SheetNames):
	Selection_All.append( i )	
	Selection.append( [i] )	
	i += 1

Selection.append(Selection_All)

#Selection = [ [0,1], [0,1,2], [0,1,3], [0,1,2,3], [0,3], [0,1,2,3,4,5], [1,4],[3,5],[0,5,4], [0,3,5] , [0,4]]
#Selection = [ [0,1,2,3] ]

i = 0
while i < len(Selection):

	KymoPicAll = PS_Plots.PlotKymoWeightedAllExcel("kymo_all_excels_"+str(i),\
        	                                       KWMeanL_AllExcel,\
                	                               KWMeanR_AllExcel,Colours,\
                        	                       ImagesSizesExcel,\
						       All_PixelRatios,\
						       All_TimeIntervals,Selection[i],\
						       str(options.OutputDir))
	print "  + Kymo Plot All Excel =", KymoPicAll+".svg"
	convert = "inkscape --export-png="+str(options.OutputDir)+"/"+KymoPicAll+\
        	  ".png --export-dpi=500 "+str(options.OutputDir)+"/"+KymoPicAll+".svg 2>/dev/null"
	os.popen(convert)
	print "  + Kymo Plot All Excel =", KymoPicAll+".png"

	if(options.OutputType == "html"):
		Figures.append( str(KymoPicAll) ) 

	i += 1

Colours2 = [["green","darkgreen"],  ["salmon","red"], ["steelblue","blue"],
            ["orchid","darkviolet"],["grey","black"], ["orange","yellow"] ]
Colours2 = Colours2 * 10

KymoSpeedsCompare = PS_Plots.PlotKymoSpeedCompare(All_AveSpeeds,SheetNames,Colours2,\
						  str(options.OutputDir))
print "  + Kymo Speeds Compare =", KymoSpeedsCompare+".png"
print "  + Kymo Speeds Compare =", KymoSpeedsCompare+".svg"

convert = "inkscape --export-png="+KymoSpeedsCompare+\
          ".png --export-dpi=500 "+KymoSpeedsCompare+".svg 2>/dev/null"
os.popen(convert)


#
# Embarassingly long code to print out the average Speeeds to a file
#
outputfile = open(str(BaseDir)+"avespeeds_"+options.Noise+"_"+options.Threshold+"_"+options.speed_start+"_"+options.speed_end+".txt",'w')
max = 0
i=0
while i < len(All_AveSpeeds):
	a = len(All_AveSpeeds[i])
	if a > max: max = a
	i += 1
#AveSpeedOut = na.zeros([len(All_AveSpeeds),max],na.Float64)
AveSpeedOut = na.zeros([len(All_AveSpeeds),max],dtype=na.float64)
i=0
while i < len(All_AveSpeeds):
	j = 0
	while j < len(All_AveSpeeds[i]):
		AveSpeedOut[i][j] = All_AveSpeeds[i][j]
		j += 1
        i += 1
i=0
while i < len(AveSpeedOut[0]):
	line = ""
        j = 0
        while j < len(AveSpeedOut):
		if AveSpeedOut[j][i] == 0.0:
			line = "%s\t"%(line)
		else:
                	line = "%s%s\t"%(line,AveSpeedOut[j][i])
                j += 1
	line = line+"\n"
	outputfile.write(line)
        i += 1
outputfile.close()

ImagesSizesExcel.append( ImageSizes )
KWMeanL_AllExcel.append( KWMeanL_All )
KWMeanR_AllExcel.append( KWMeanR_All )

KWSpeeds_AllExcel.append( KWSpeeds_All )

print
print "Finished", sys.argv[0]

if(options.OutputType == "html"):
	print "</PRE></TD>"
	print "<TD VALIGN=top><FONT COLOR=black><FONT FACE=sans,arial SIZE=2>"

	i=0
	while i < len(Figures):
                print "<FONT FACE='sans,arial' SIZE=1>"
		print "Plot of speeds for set(s)", Selection[i], "<BR>"
		print "<IMG WIDTH=200 SRC="+str(options.OutputHTML)+"/"+\
		      str(options.OutputDir)+"/"+Figures[i]+".png><BR>"
		print "<A HREF='"+str(options.OutputHTML)+\
                      "/"+str(options.OutputDir)+"/"+Figures[i]+".png' ", \
                      "STYLE='TEXT-DECORATION: NONE' target='_blank'>[PNG]</A>"
		print "<A HREF='"+str(options.OutputHTML)+\
                      "/"+str(options.OutputDir)+"/"+Figures[i]+".svg' ", \
                      "STYLE='TEXT-DECORATION: NONE' target='_blank'>[SVG]</A><P>"
		i += 1

	print "<FONT FACE='sans,arial' SIZE=1>Speed Comparison:<BR>"
        print "<IMG WIDTH=200 SRC="+str(options.OutputHTML)+"/"+\
              str(options.OutputDir)+"/kymo_SpeedCompare.png><BR>"
        print "<A HREF='"+str(options.OutputHTML)+\
              "/"+str(options.OutputDir)+"/kymo_SpeedCompare.png' ", \
              "STYLE='TEXT-DECORATION: NONE' target='_blank'>[PNG]</A>"
        print "<A HREF='"+str(options.OutputHTML)+\
              "/"+str(options.OutputDir)+"/kymo_SpeedCompare.svg' ", \
              "STYLE='TEXT-DECORATION: NONE' target='_blank'>[SVG]</A><P>"

	print "</TD></TR></TABLE>"
        print "</BODY></HTML>\n\n"

#------------------------------------------------------------------------------
# FIN
#------------------------------------------------------------------------------
