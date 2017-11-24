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

import ParticleStats_Inputs  as PS_Inputs
import numpy as na
import os,sys
import glob
import time

#------------------------------------------------------------------------------
def Print_Welcome ( Mode, Size ):

	Time = time.asctime()

	print PS_Inputs.Colourer("   ____            _   _      _      ____  _        _         ",
	      "blue",Mode,"bold",Size)
	print PS_Inputs.Colourer("  |  _ \ __ _ _ __| |_(_) ___| | ___/ ___|| |_ __ _| |_ ___   ",
	      "blue",Mode,"bold",Size)
	print PS_Inputs.Colourer("  | |_) / _` | '__| __| |/ __| |/ _ \___ \| __/ _` | __/ __|  ",
	      "blue",Mode,"bold",Size)
	print PS_Inputs.Colourer("  |  __/ (_| | |  | |_| | (__| |  __/___) | || (_| | |_\__ \  ",
	      "blue",Mode,"bold",Size)
	print PS_Inputs.Colourer("  |_|   \__,_|_|   \__|_|\___|_|\___|____/ \__\__,_|\__|___/  ",
	      "blue",Mode,"bold",Size)
	print PS_Inputs.Colourer("","blue",Mode,"",Size)
	print PS_Inputs.Colourer("                                   by Russell S. Hamilton",
	      "blue", Mode, "bold",Size)
	print PS_Inputs.Colourer("","blue",Mode,"",Size)
	print "\tDate     =", PS_Inputs.Colourer(Time,"blue",Mode,"",Size)
	print "\tRun Mode =", Mode


#------------------------------------------------------------------------------
def Print_HTMLHeaders ( ):

	print "<HTML>\n<HEAD>\n<TITLE>ParticleStats</TITLE>\n</HEAD>"
	print "<BODY>"

	print "<TABLE STYLE='border:1px;border-style:solid'>"
	print "<TR>"
	print "<TD><FONT FACE='sans,arial' SIZE=2><B>Program Output</B></TD>"
	print "<TD VALIGN=top><FONT FACE='sans,arial' SIZE=2><B>Graph Outputs</B>: Click to enlarge and open in a new window/tab</TD>"
	print "</TR>" 
	print "<TR>"
	print "<TD VALIGN=top ROWSPAN=2 width=350 BGCOLOR=whitesmoke><FONT FACE=courier SIZE=1><PRE>"

#------------------------------------------------------------------------------
def Print_HTMLTails ( DirBase, DirGraph, Excel1, Excel2):

	Ex1_Dir,Ex1File = os.path.split(Excel1)
	Ex2_Dir,Ex2File = os.path.split(Excel2)

	print "</FONT></PRE></TD>"
	print "<TD VALIGN=top WIDTH=450 HEIGHT=500><A HREF='"+ DirBase + DirGraph + \
	      "RunsLengths_Coords1.png' TARGET=_blank><IMG BORDER=0 SRC='"+ DirBase + DirGraph+ \
	      "RunsLengths_Coords1.png' WIDTH=400></A>"
	print "<BR><CENTER><FONT FACE=sans,arial SIZE=2><B>Figure 1.</B> " + \
	      "Run lengths for Coords Set 1 (" + Ex1File + ")<BR>" + \
              " <A HREF='"+DirBase+DirGraph+"RunsLengths_Coords1.png' STYLE='TEXT-DECORATION: NONE' target='_blank'>[PNG]</A>" +\
	      " <A HREF='"+DirBase+DirGraph+"RunsLengths_Coords1.svg' STYLE='TEXT-DECORATION: NONE' target='_blank'>[SVG]</A>" +\
              "</FONT></CENTER>"

	print "<BR><A HREF='"+ DirBase + DirGraph +"RunsLengths_Coords2.png' TARGET=_blank>" +\
	      "<IMG BORDER=0 SRC='" + DirBase + DirGraph + "/RunsLengths_Coords2.png' WIDTH=400></A>"
	print "<BR><CENTER><FONT FACE=sans,arial SIZE=2><B>Figure 2.</B> "+ \
	      "Run lengths for Coords Set 2 (" + Ex2File + ")<BR>" + \
              " <A HREF='"+DirBase+DirGraph+"RunsLengths_Coords2.png' STYLE='TEXT-DECORATION: NONE' target='_blank'>[PNG]</A>" +\
              " <A HREF='"+DirBase+DirGraph+"RunsLengths_Coords2.svg' STYLE='TEXT-DECORATION: NONE' target='_blank'>[SVG]</A>" +\
	      "</FONT></CENTER>"

	print "<BR><A HREF='" + DirBase + DirGraph + "ThreeRunsFreq_0.png' TARGET=_blank>" +\
              "<IMG BORDER=0 SRC='" + DirBase + DirGraph + "ThreeRunsFreq_0.png' WIDTH=400></A>"
	print "<BR><CENTER><FONT FACE=sans,arial SIZE=2><B>Figure 3.</B> " +\
              "Graph Frequencies of Run Speeds (Runs split into 3 frames) Coords Set 0 (red line = polynomial fit)<BR>" +\
              " <A HREF='"+DirBase+DirGraph+"ThreeRunsFreq_0.png' STYLE='TEXT-DECORATION: NONE' TARGET=_blank>[PNG]</A>" +\
              " <A HREF='"+DirBase+DirGraph+"ThreeRunsFreq_0.svg' STYLE='TEXT-DECORATION: NONE' TARGET=_blank>[SVG]</A>" +\
              "</FONT></CENTER>"

	print "<BR><A HREF='" + DirBase + DirGraph + "ThreeRunsFreq_1.png' TARGET=_blank>" +\
              "<IMG BORDER=0 SRC='" + DirBase + DirGraph + "ThreeRunsFreq_1.png' WIDTH=400></A>"
	print "<BR><CENTER><FONT FACE=sans,arial SIZE=2><B>Figure 4.</B> " +\
              "Graph Frequencies of Run Speeds (Runs split into 3 frames) Coords Set 1 (red line = polynomial fit)<BR>" +\
              " <A HREF='"+DirBase+DirGraph+"ThreeRunsFreq_1.png' STYLE='TEXT-DECORATION: NONE' TARGET=_blank>[PNG]</A>" +\
              " <A HREF='"+DirBase+DirGraph+"ThreeRunsFreq_1.svg' STYLE='TEXT-DECORATION: NONE' TARGET=_blank>[SVG]</A>" +\
	      "</FONT></CENTER>"

	print "<BR><A HREF='" + DirBase + DirGraph + "ThreeRunsMaxFreq_0.png' TARGET=_blank>" +\
              "<IMG BORDER=0 SRC='" + DirBase + DirGraph + "ThreeRunsMaxFreq_0.png' WIDTH=400></A>"
        print "<BR><CENTER><FONT FACE=sans,arial SIZE=2><B>Figure 5.</B> " +\
              "Graph Frequencies of Max Run Speeds (Runs split into 3 frames) Coords Set 0 (red line = polynomial fit)<BR>" +\
              " <A HREF='"+DirBase+DirGraph+"ThreeRunsMaxFreq_0.png' STYLE='TEXT-DECORATION: NONE' TARGET=_blank>[PNG]</A>" +\
              " <A HREF='"+DirBase+DirGraph+"ThreeRunsMaxFreq_0.svg' STYLE='TEXT-DECORATION: NONE' TARGET=_blank>[SVG]</A>" +\
	      "</FONT></CENTER>"

        print "<BR><A HREF='" + DirBase + DirGraph + "ThreeRunsMaxFreq_1.png' TARGET=_blank>" +\
              "<IMG BORDER=0 SRC='" + DirBase + DirGraph + "ThreeRunsMaxFreq_1.png' WIDTH=400></A>"
        print "<BR><CENTER><FONT FACE=sans,arial SIZE=2><B>Figure 6.</B> " +\
              "Graph Frequencies of Max Run Speeds (Runs split into 3 frames) Coords Set 1 (red line = polynomial fit)<BR>" +\
              " <A HREF='"+DirBase+DirGraph+"ThreeRunsMaxFreq_1.png' STYLE='TEXT-DECORATION: NONE' TARGET=_blank>[PNG]</A>" +\
              " <A HREF='"+DirBase+DirGraph+"ThreeRunsMaxFreq_1.svg' STYLE='TEXT-DECORATION: NONE' TARGET=_blank>[SVG]</A>" +\
	      "</FONT></CENTER>"

	print "<BR><A HREF='" + DirBase + DirGraph + "DirChangesFreq_0.png' TARGET=_blank>" +\
              "<IMG BORDER=0 SRC='" + DirBase + DirGraph + "DirChangesFreq_0.png' WIDTH=400></A>"
        print "<BR><CENTER><FONT FACE=sans,arial SIZE=2><B>Figure 7.</B> " +\
              "Graph Frequencies of Direction Changes Coords Set 0 " +\
              " <A HREF='"+DirBase+DirGraph+"DirChangesFreq_0.png' STYLE='TEXT-DECORATION: NONE' TARGET=_blank>[PNG]</A>" +\
              " <A HREF='"+DirBase+DirGraph+"DirChangesFreq_0.svg' STYLE='TEXT-DECORATION: NONE' TARGET=_blank>[SVG]</A>" +\
	      "</FONT></CENTER>"

	print "<BR><A HREF='" + DirBase + DirGraph + "DirChangesFreq_1.png' TARGET=_blank>" +\
              "<IMG BORDER=0 SRC='" + DirBase + DirGraph + "DirChangesFreq_1.png' WIDTH=400></A>"
        print "<BR><CENTER><FONT FACE=sans,arial SIZE=2><B>Figure 8.</B> " +\
              "Graph Frequencies of Direction Changes Coords Set 1 " +\
              " <A HREF='"+DirBase+DirGraph+"DirChangesFreq_1.png' STYLE='TEXT-DECORATION: NONE' TARGET=_blank>[PNG]</A>" +\
              " <A HREF='"+DirBase+DirGraph+"DirChangesFreq_1.svg' STYLE='TEXT-DECORATION: NONE' TARGET=_blank>[SVG]</A>" +\
	      "</FONT></CENTER>"

	print "<BR><A HREF='" + DirBase + DirGraph + "Compare_0_All_comprosediagram.png' TARGET=_blank>" +\
              "<IMG BORDER=0 SRC='" + DirBase + DirGraph + "Compare_0_All_comprosediagram.png' WIDTH=400></A>"
        print "<BR><CENTER><FONT FACE=sans,arial SIZE=2><B>Figure 9.</B> " +\
              "Graph Directionality of Runs Coords Set 0 " +\
              " <A HREF='"+DirBase+DirGraph+"Compare_0_All_comprosediagram.png' STYLE='TEXT-DECORATION: NONE' TARGET=_blank>[PNG]</A>" +\
              " <A HREF='"+DirBase+DirGraph+"Compare_0_All_comprosediagram.svg' STYLE='TEXT-DECORATION: NONE' TARGET=_blank>[SVG]</A>" +\
	      "</FONT></CENTER>"

	print "<BR><A HREF='" + DirBase + DirGraph + "Compare_1_All_comprosediagram.png' TARGET=_blank>" +\
              "<IMG BORDER=0 SRC='" + DirBase + DirGraph + "Compare_1_All_comprosediagram.png' WIDTH=400></A>"
        print "<BR><CENTER><FONT FACE=sans,arial SIZE=2><B>Figure 10.</B> " +\
              "Graph Directionality of Runs Coords Set 0 " +\
              " <A HREF='"+DirBase+DirGraph+"Compare_1_All_comprosediagram.png' STYLE='TEXT-DECORATION: NONE' TARGET=_blank>[PNG]</A>" +\
              " <A HREF='"+DirBase+DirGraph+"Compare_1_All_comprosediagram.svg' STYLE='TEXT-DECORATION: NONE' TARGET=_blank>[SVG]</A>" +\
	      "</FONT></CENTER>"

	print "<FONT FACE='sans,arial' SIZE=2><P><B>File Output</B>" +\
              "<P><A HREF='" + DirBase + DirGraph + "ThreeFrameData_All.txt' TARGET=_blank " +\
              "STYLE='TEXT-DECORATION: NONE'>Three Frame Tab Delimited Run Output</A> " 

        print "<P><A HREF='" + DirBase + DirGraph + "ThreeFrameMaxData_All.txt' TARGET=_blank " +\
              "STYLE='TEXT-DECORATION: NONE'>Three Frame Max Tab Delimited Run Output</A> "

	print "<FONT FACE='sans,arial' SIZE=2><P>" +\
              "<P><A HREF='" + DirBase + DirGraph + "DirectionChangeData_All_0.txt' TARGET=_blank " +\
              "STYLE='TEXT-DECORATION: NONE'>Direction Changes Tab Delimited Run Output CoordSet 1</A> " +\
	      "<P><A HREF='" + DirBase + DirGraph + "DirectionChangeData_All_1.txt' TARGET=_blank " +\
              "STYLE='TEXT-DECORATION: NONE'>Direction Changes Tab Delimited Run Output CoordsSet 2</A> "


	print "<BR></TD></TR><TR><TD VALIGN=top><FONT FACE='sans,arial' SIZE=2>" +\
	      "<P><A HREF='" + DirBase + DirGraph + "/ParticleStats_Coords1_Output.text' TARGET=_blank " +\
	      "STYLE='TEXT-DECORATION: NONE'>Tab Delimited Run Output</A> for " + Ex1File + \
	      "<P><A HREF='" + DirBase + DirGraph + "/ParticleStats_Coords2_Output.text' TARGET=_blank " + \
	      "STYLE='TEXT-DECORATION: NONE'>Tab Delimited Run Output</A> for " + Ex2File + \
	      "<BR></TD></TR></TABLE><P>"

        print "</BODY>"
	print "</HTML>"

#------------------------------------------------------------------------------
def Print_Parameters (InputFileName1,Coords1,InputFileName2,Coords2,Mode,Size ):

	print PS_Inputs.Colourer("### READ IN REQUIRED FILES ###", "green", Mode, "bold",Size)

	print "\tReading Input Files"
	print "\t\tSet 1 Excel File =", InputFileName1
	print "\t\tNo Sheets        =", len(Coords1)
	print "\t\tSet 2 Excel File =", InputFileName2
	print "\t\tNo Sheets        =", len(Coords2)

#------------------------------------------------------------------------------
def Print_ParticleStatsLine ( Stats_Particle, Stats_Standards ):

        StatsLine =  " Average Speed       = [+ve " + \
                     str(Stats_Particle['Ave_Speed_P']) + "]" + \
                     "[-ve " +  str(Stats_Particle['Ave_Speed_N']) + "]" + \
                     "[all " +  str(Stats_Particle['Ave_Speed_All']) + "]\n"
        StatsLine += " Average Run Length  = [+ve " +  \
                     str(Stats_Particle['Ave_RunLen_P']) + "] " + \
                     "[-ve " +  str(Stats_Particle['Ave_RunLen_N']) + "]\n"

        StatsLine += " Standard Deviations = Speed [+ve " + \
                     str(Stats_Standards['S_P_D']) + "] " + \
                     "[-ve " +  str(Stats_Standards['S_N_D']) + "]\n"
        StatsLine += "                       Dist  [+ve " +  \
                     str(Stats_Standards['D_P_D']) + "] " + \
                     "[-ve " +  str(Stats_Standards['D_N_D']) + "]\n"

        StatsLine += " Standard Errors     = Speed [+ve " + \
                     str(Stats_Standards['S_P_E']) + "] " + \
                     "[-ve " + str(Stats_Standards['S_N_E']) + "]\n"
        StatsLine += "                       Dist  [+ve " + \
                     str(Stats_Standards['D_P_E']) + "] " + \
                     "[-ve " + str(Stats_Standards['D_N_E']) + "]"

	return StatsLine 

#------------------------------------------------------------------------------
def Print_OutputFile ( FileName, FileOut):

	Header = "Event No.\tParticle No.\tRun No.\t" \
                 + "Start Frame\tEnd Frame\tDirection\tDistance\t"\
                 + "Abs Distance\tPositive Distance\tNegative Distance\t"\
                 + "Speed\tTime\tAbs Distancs XY\n"

	outputfile = open(FileName,'w')
	outputfile.write(Header)
	outputfile.write(FileOut)
	outputfile.close()

#------------------------------------------------------------------------------
def Print_ParticleReport (Stats_Particle, Stats_Runs, Mode ):

	print "\t\tRuns:     Total No. Runs           =", Stats_Particle['NoRuns']
	print "\t\tRuns:     Total No. +ve Runs       =", Stats_Particle['NoRuns_p']
        print "\t\tRuns:     Total No. -vt Runs       =", Stats_Particle['NoRuns_n']
	print "\t\tRuns:     Gross Y Distance         =", (Stats_Runs['Dist_p']\
                                                           +abs(Stats_Runs['Dist_n']))
        print "\t\tRuns:     Net Y Distance           =", Stats_Runs['NetDistance']
        print "\t\tRuns:     Total +ve Y Distance     =", \
                        PS_Inputs.Colourer(str(Stats_Runs['Dist_p']),"red",Mode,"",2)
        print "\t\tRuns:     Total -ve Y Distance     =", \
                        PS_Inputs.Colourer(str(abs(Stats_Runs['Dist_n'])),"blue",Mode,"",2)

	try:
                print "\t\tRuns:     Ave +ve Speed (X&Y)      = %.2f" \
                      %(Stats_Particle['AveSpeed_p']/Stats_Particle['NoRuns_p'])
        except ZeroDivisionError:
                print "\t\tRuns:     Ave +ve Speed (X&Y)      = 0"

        try:
                print "\t\tRuns:     Ave -ve Speed (X&Y)      = %.2f" \
                      %(Stats_Particle['AveSpeed_n']/Stats_Particle['NoRuns_n'])
        except ZeroDivisionError:
                print "\t\tRuns:     Ave -ve Speed (X&Y)      = 0"

        print "\t\tParticle: Gross Distance           =", Stats_Runs['GrossDistance']
        print "\t\tParticle: Net Distance             =", Stats_Runs['NetDistance']

        try:
                print "\t\tParticle: Ave +ve Run Distance     = %.1f"% \
                                (Stats_Runs['Dist_p']/Stats_Runs['NoRuns_p'])
        except ZeroDivisionError:
                print "\t\tParticle: Ave +ve Run Distance     = 0.00"

        try:
                print "\t\tParticle: Ave -ve Run Distance     = %.1f"% \
                                (Stats_Runs['Dist_n']/Stats_Runs['NoRuns_n'])
        except ZeroDivisionError:
                print "\t\tParticle: Ave -ve Run Distance     = 0.00"

        try:
                print "\t\tStats:    +ve run dist/ Gross Dist = %.4f" % \
                        abs(Stats_Runs['Dist_p'] / Stats_Runs['GrossDistance'])
        except ZeroDivisionError:
                print "\t\tStats:    +ve run dist/ Gross Dist = 0.0000"

        try:
                print "\t\tStats:    -ve run dist/ Gross Dist = %.4f" % \
                        abs(Stats_Runs['Dist_n'] / Stats_Runs['GrossDistance'])
        except ZeroDivisionError:
                print "\t\tStats:    -ve run dist/ Gross Dist = 0.0000"


        try:
                print "\t\tStats:    Ave+Speed = %.4f" % \
                        abs(Stats_Particle['Dp'] / Stats_Particle['Tp'])
        except ZeroDivisionError:
                print "\t\tStats:    Ave+Speed = 0.0000"
        try:
                print "\t\tStats:    Ave-Speed = %.4f" % \
                        abs(Stats_Particle['Dn'] / Stats_Particle['Tn'])
        except ZeroDivisionError:
                print "\t\tStats:    Ave-Speed = 0.0000"

#------------------------------------------------------------------------------
def Print_GlobalStats ( AllRuns_X, Stats_Global, Stats_Standards ):

	GlobalStats =  " Total No. Events    = " + str(len(AllRuns_X)) + "\n"
	GlobalStats += " No. +ve Runs        = " + str(Stats_Global['No_Runs_P']) + "\n"
	GlobalStats += " No. -ve Runs        = " + str(Stats_Global['No_Runs_N']) + "\n"
	GlobalStats += " No. Pauses          = " + str(Stats_Global['No_Runs_0']) + "\n"
	GlobalStats += " Total Run Dist      = [+ve " + \
                       str(Stats_Global['Total_RunLen_P']) + "]" + \
	               "[-ve " + str(Stats_Global['Total_RunLen_N']) + "]\n" 

	GlobalStats += " Average Speed       = [+ve " + \
		       str( Stats_Global['Ave_Speed_P'] )
        GlobalStats += "] " 
	GlobalStats += " [-ve " + str(Stats_Global['Ave_Speed_N']) + "]" + \
	               " [all " + str(Stats_Global['Ave_Speed_All']) + "]\n"

	GlobalStats += " Average Run Length  = [+ve " + \
                       str(Stats_Global['Ave_RunLen_P']) + "]" + \
	               " [-ve " + str(Stats_Global['Ave_RunLen_N']) + "]\n"

	GlobalStats += " Standard Deviations = Speed [+ve" + \
                       str(Stats_Standards['S_P_D']) + "]" + \
	               " [-ve" + str(Stats_Standards['S_N_D']) + "]\n"
	GlobalStats += "                       Dist  [+ve" + \
                       str(Stats_Standards['D_P_D']) + "]" + \
	               " [-ve" + str(Stats_Standards['D_N_D']) + "]\n"

	GlobalStats += " Standard Errors     = Speed [+ve " + \
                       str(Stats_Standards['S_P_E']) + "]" + \
	               " [-ve " + str(Stats_Standards['S_N_E']) + "]\n"
	GlobalStats += "                       Dist  [+ve " + \
                       str(Stats_Standards['D_P_E']) + "]" + \
	               " [-ve " + str(Stats_Standards['D_N_E']) + "]\n"

	return GlobalStats

#------------------------------------------------------------------------------
def Print_FileOut ( Runs, RunCounter, i, j):

	FileOut = str(RunCounter) + "\t" + \
	          str(i+1) + "\t" + \
                  str(j+1) + "\t" + \
                  str(Runs[j][0]) + "\t" + \
                  str(Runs[j][1]) + "\t" + \
                  str(Runs[j][2]) + "\t" + \
                  str(Runs[j][3]) + "\t" + \
                  str(Runs[j][4]) + "\t" + \
                  str(Runs[j][5]) + "\t" + \
                  str(Runs[j][6]) + "\t" + \
                  str(Runs[j][7]) + "\t" + \
                  str(Runs[j][8]) + "\t" + \
                  str(Runs[j][9]) + "\n"

	return FileOut

#------------------------------------------------------------------------------
def Print_RunLine ( Runs, j, Event, Error):

	RunLine = " " + Event + " %3d [" % (j+1) +  \
                  "  %3d "   % Runs[j][0] + \
                  "%3d "     % Runs[j][1] + \
                  "%+3d "    % Runs[j][2] + \
                  "%6.1f "  % Runs[j][3] + \
                  "%6.1f "   % Runs[j][4] + \
                  "%6.1f "  % Runs[j][5] + \
                  "%6.1f "  % Runs[j][6] + \
                  "%6.2f "   % Runs[j][7] + \
                  "%6.2f "   % Runs[j][8] + \
		  "%6.2f "   % Runs[j][9] + \
                  "%6.2f "  % Runs[j][10] + \
                  Error + ""

	return RunLine

#------------------------------------------------------------------------------
def ColourConvert(Colours):

	RGB = []

	if   Colours == "red":     	RGB = (255,0,0)
	elif Colours == "blue":    	RGB = (0,0,255)
	elif Colours == "green":   	RGB = (0,255,0)
	elif Colours == "brown":   	RGB = (165,42,42)
	elif Colours == "gold":    	RGB = (255,215,0)
	elif Colours == "maroon":  	RGB = (128,0,0)
        elif Colours == "purple":  	RGB = (160,32,240)
        elif Colours == "orange":  	RGB = (255,165,0)
        elif Colours == "yellow":  	RGB = (255,255,0)
        elif Colours == "silver":  	RGB = (230,232,250)
        elif Colours == "cyan":    	RGB = (0,255,255)
        elif Colours == "magenta": 	RGB = (255,0,255)
	elif Colours == "white":   	RGB = (255,255,255)
	elif Colours == "black":   	RGB = (0,0,0)
	elif Colours == "darkgreen":	RGB = (0,100,0)
	elif Colours == "steelblue":	RGB = (70,130,180)
	elif Colours == "orchid":	RGB = (218,112,214)
	elif Colours == "darkviolet":	RGB = (148,0,211)
	elif Colours == "salmon":	RGB = (250,128,114)
	elif Colours == "grey":		RGB = (84,84,84)
	else:	RGB = (0,0,0)
	

	return RGB[0],RGB[1],RGB[2]

#------------------------------------------------------------------------------
# FIN
#------------------------------------------------------------------------------
