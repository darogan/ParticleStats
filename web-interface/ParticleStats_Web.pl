#!/usr/bin/env perl
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

use CGI;

use strict;
use warnings;

use POSIX;
use File::Spec;

my $uploaddir;
my $webspace;

if($ENV{'HTTP_HOST'} =~ m/ctr-web.pdn.cam.ac.uk/)
  {
    $uploaddir = "/storage/www/ParticleStats2.0/PS_Out/";
    $webspace  = "http://ctr-web.pdn.cam.ac.uk/ParticleStats2.0";
  }
else
  {
     exit;
  }


sub Tracker {
  my $Phase = shift;
  my $uploaddir = shift;

  my $date = POSIX::strftime "%F_%H%M", localtime;
  my $Track = sprintf("%-10s\t%25s\t%15s\t%s\n",
                      $Phase, $date, $ENV{REMOTE_ADDR}, $ENV{HTTP_USER_AGENT});
  open (my $counter, ">>", "$uploaddir/Counter.text")
    or return; # Do not die just because we are unable to track stats.
  print {$counter} "$Track";
  close $counter;
}


sub Uploader
{
  my $upload_FH  = shift;
  my $File       = shift;
  my $Directory  = shift;
  my $fpath = File::Spec->catfile ($Directory, $File);

  if (($fpath =~ m/\.xls$/) or ($fpath =~ m/\.tiff?$/) or \
      ($fpath =~ m/\.zip$/) or ($fpath =~ m/\.tar.gz$/))
    {
      open (UPLOADFILE, ">", $fpath) or die "dfsdfsdf: $!\n";
      binmode UPLOADFILE;

      while ( <$upload_FH> )
       {
         print UPLOADFILE;
       }

      close UPLOADFILE;
    }
  return;
}


sub Process
{
  my $Phase = shift;
  my $q = shift;
  my $uploaddir = shift;

  my @chars     = ( "A" .. "Z", "a" .. "z", 0 .. 9);
  my $Directory = "PSResults." . join("", @chars[ map { rand @chars } ( 1 .. 20 ) ]);
  my $upload_path = File::Spec->catfile ($uploaddir, $Directory);

  `mkdir $upload_path`;
  `chmod -R 777 $upload_path`;

  my $Command;
  if( $Phase eq "Compare" )
    {
      my $ExcelFile1  = $q->param("excel1");
      $ExcelFile1 =~ s/.*[\/\\](.*)/$1/;
      my $ExcelFile2  = $q->param("excel2");
      $ExcelFile2 =~ s/.*[\/\\](.*)/$1/;

      if($q->param('OPT_Example') !~ m/on/)
        {
          Uploader ($q->upload("excel1"), $ExcelFile1, $upload_path);
          Uploader ($q->upload("excel2"), $ExcelFile2, $upload_path);
        }

      my %Opts;
      if($q->param('OPT_Trails')     =~ m/on/) { $Opts{'OPT_Trails'}     = "-t"; }
      if($q->param('OPT_Graphs')     =~ m/on/) { $Opts{'OPT_Graphs'}     = "-g"; }
      if($q->param('OPT_Regression') =~ m/on/) { $Opts{'OPT_Regression'} = "-r"; }
      if($q->param('OPT_Example')    =~ m/on/) { $Opts{'OPT_Example'}    = "1"; }

      my $Error;
      if($q->param('OPT_RunDistance') =~ m/[^0-9\.]/) {
         $Error = "<FONT FACE=sans,arial COLOR=red>" .
                  "Error: Run Distance Must Be a numerical value</FONT>";
         return $Error; }
      if($q->param('OPT_RunFrames') =~ m/[^0-9]/) {
         $Error = "<FONT FACE=sans,arial COLOR=red>" .
                  "Error: Run Frames must be an integer value</FONT>";
         return $Error; }
      if($q->param('OPT_PauseSpeed') =~ m/[^0-9\.]/) {
         $Error = "<FONT FACE=sans,arial COLOR=red>" .
                  "Error: Pause Speed Must Be a numerical value</FONT>";
         return $Error; }
      if($q->param('OPT_PauseFrames') =~ m/[^0-9]/) {
         $Error = "<FONT FACE=sans,arial COLOR=red>" .
                  "Error: Pause Frames must be an integer value</FONT>";
         return $Error; }
      if($q->param('OPT_PauseDistance') =~ m/[^0-9\.]/) {
         $Error = "<FONT FACE=sans,arial COLOR=red>" .
                  "Error: Pause Distance Must Be a numerical value</FONT>";
         return $Error; }
      if($q->param('OPT_PauseDuration') =~ m/[^0-9]/) {
         $Error = "<FONT FACE=sans,arial COLOR=red>" .
                  "Error: Pause Duration Must Be a numerical value</FONT>";
         return $Error; }
      if($q->param('OPT_Pixels') =~ m/[^0-9\.]/) {
         $Error = "<FONT FACE=sans,arial COLOR=red>" .
                  "Error: Pixels Must Be a numerical value</FONT>";
         return $Error; }
      if($q->param('OPT_Dimensions') =~ m/[^0-9A-Za-z]/) {
         $Error = "<FONT FACE=sans,arial COLOR=red>" .
                  "Error: Dimensions not 2D, 1DX, or 1DY</FONT>";
         return $Error; }

      my $ExtraOptions = $Opts{'OPT_Graphs'}     . " " .
                      $Opts{'OPT_Trails'}     . " " .
                      $Opts{'OPT_Regression'} . " " .
                      "--rundistance="     . $q->param('OPT_RunDistance')   . " " .
                      "--runframes="       . $q->param('OPT_RunFrames')     . " " .
                      "--pausedistance="   . $q->param('OPT_PauseDistance') . " " .
                      "--pauseduration="   . $q->param('OPT_PauseDuration') . " " .
                      "--pausespeed="      . $q->param('OPT_PauseSpeed')    . " " .
                      "--pauseframes="     . $q->param('OPT_PauseFrames')   . " " .
                      "--pausedefinition=" . $q->param('OPT_Pauses')        . " " .
                      "--timestart="       . $q->param('OPT_TimeStart')     . " " .
                      "--timeend="         . $q->param('OPT_TimeEnd')       . " " .
                      "--pixelratio="      . $q->param('OPT_Pixels')        . " " ;

      if($q->param('OPT_Example') =~ m/on/)
        {
          $Command = "ParticleStats_Compare.py -o html $ExtraOptions " .
                     "-a $uploaddir/CompareExample_control.xls " .
                     "-b $uploaddir/CompareExample_variant.xls " .
                     "--outdir=PS_Out/$Directory/ --outhtml=$webspace/";
        }
      else
        {
          $Command = "ParticleStats_Compare.py -o html $ExtraOptions " . 
                     "-a $upload_path/$ExcelFile1 -b $upload_path/$ExcelFile2 " . 
                     "--outdir=PS_Out/$Directory/ --outhtml=$webspace/";
        }
    } 
  elsif( $Phase eq "Directionality" )
    {
      my $ExcelFile1  = $q->param("excel1");
      $ExcelFile1 =~ s/.*[\/\\](.*)/$1/;
      my $TiffFile1   = $q->param("tiff1");
      $TiffFile1  =~ s/.*[\/\\](.*)/$1/;

      my $ExtraOptions = "";

      if($q->param('OPT_ROI'))
        {
          my $ROI = $q->param('OPT_ROI');
          open(ROI,">$upload_path/polygon.text");
          print ROI $ROI;
          close ROI;
          $ExtraOptions .= " -p $upload_path/polygon.text ";
        }

      if($q->param('OPT_Example') !~ m/on/)
        {
          Uploader ($q->upload("excel1"), $ExcelFile1, $upload_path);
          Uploader ($q->upload("tiff1"), $TiffFile1, $upload_path);
        }

      if($q->param('OPT_AxisRotate') =~ m/on/)     { $ExtraOptions .= " -a "; }
      if($q->param('OPT_ShowGrid') =~ m/on/)       { $ExtraOptions .= " -g "; }
      if($q->param('OPT_ShowRectangles') =~ m/on/) { $ExtraOptions .= " -r "; }
      if($q->param('OPT_ShowArrows') =~ m/on/)     { $ExtraOptions .= " -c "; }
      if($q->param('OPT_ScaleRose') =~ m/on/)      { $ExtraOptions .= " --scalerose "; }

      if($q->param('OPT_Example') =~ m/on/)
        {
          $Command = "ParticleStats_Directionality.py " . 
                     "-x $uploaddir/DirectionalityExample.xls " .
                     "-i $uploaddir/DirectionalityExample.tif -s " . $q->param('OPT_Squares') . 
                     " --ArrowColour " . $q->param('OPT_ArrowColour') .
                     " --ROIColour " . $q->param('OPT_ROIColour') .
                     " --AxisLabels=" . $q->param('OPT_AxisLabels') .
                     " $ExtraOptions -o html " .  
                     "--outdir=PS_Out/$Directory/ --outhtml=$webspace/";
        }
      else
        {
          $Command = "ParticleStats_Directionality.py " . 
                     "-x $upload_path/$ExcelFile1 " . 
                     "-i $upload_path/$TiffFile1 -s " . $q->param('OPT_Squares') . 
                     " --ArrowColour=" . $q->param('OPT_ArrowColour') .
                     " --ROIColour=" . $q->param('OPT_ROIColour') .
                     " --AxisLabels=" . $q->param('OPT_AxisLabels') .
                     " $ExtraOptions -o html " .  
                     "--outdir=PS_Out/$Directory/ --outhtml=$webspace/";
        }
    }
  elsif( $Phase eq "Kymographs" )
    {
      my $ExcelFile1  = $q->param("excel1");
      $ExcelFile1 =~ s/.*[\/\\](.*)/$1/;
      my $TiffFile2   = $q->param("tiffcomp");
      $TiffFile2  =~ s/.*[\/\\](.*)/$1/;

      if($q->param('OPT_Example') !~ m/on/)
        {
          Uploader ($q->upload("excel1"), $ExcelFile1, $upload_path);
          Uploader ($q->upload("tiffcomp"), $TiffFile2, $upload_path);
        }
      if($q->param('OPT_Example') =~ m/on/)
        {
          `unzip $uploaddir/KymographExample.zip -d $upload_path`;
        }

      if( ($TiffFile2 =~ m/\.zip\b/) and ($q->param('OPT_Example') !~ m/on/) )
        {
          `unzip $upload_path/$TiffFile2 -d $upload_path`;
        }
      elsif($TiffFile2 =~ m/\.tar.gz\b/)
       {
          `tar -zxvf $upload_path/$TiffFile2 --directory $upload_path`;
       }

      if($q->param('OPT_Example') =~ m/on/)
        {
          $Command = "ParticleStats_Kymographs.py -x $uploaddir/KymographExample.xls " .
                     "--tiffdir=$uploaddir/KymographExample_dir " .
                     "-n " . $q->param('OPT_Noise') . " " .
                     "-t " . $q->param('OPT_Threshold') . " " .
                     "--speed_start=" . $q->param('OPT_TimeStart') . " " .
                     "--speed_end=" . $q->param('OPT_TimeEnd') . " " .
                     "--outdir=PS_Out/$Directory/ --outhtml=$webspace/ -o html";
        }
      else
        {
          $Command = "ParticleStats_Kymographs.py -x $upload_path/$ExcelFile1 " . 
                     "--tiffdir=$upload_path/ " .
                     "-n " . $q->param('OPT_Noise') . " " . 
                     "-t " . $q->param('OPT_Threshold') . " " .
                     "--speed_start=" . $q->param('OPT_TimeStart') . " " .
                     "--speed_end=" . $q->param('OPT_TimeEnd') . " " .
                     "--outdir=PS_Out/$Directory/ --outhtml=$webspace/ -o html";
        }
    }
  else
    {
      die "This is not a valid ParticleStats process step";
    }

  $ENV{'PATH'} = '/bin:/usr/bin:/usr/local/bin';
  $ENV{'MATPLOTLIBDATA'} = $uploaddir;
  $ENV{'MATPLOTLIBRC'} = '/usr/share/matplotlib/';
  $ENV{'HOME'} = $uploaddir;

  my $Runner = `$Command`;

  $Runner =~ s/<HTML>.*<BODY>//s;
  $Runner =~ s/Loading.*\n//g;
  $Runner =~ s/RHOME.*\n//;
  $Runner =~ s/RVERSION.*\n//g;
  $Runner =~ s/RVER.*\n//g;
  $Runner =~ s/RUSER.*\n//g;
  $Runner =~ s/Creating.*\n//g;
  $Runner =~ s/<\/BODY>.*\n//;
  $Runner =~ s/<\/HTML>//;

  my $Output = "<TABLE WIDTH=800 BGCOLOR=white " . 
            "STYLE='border:1px;border-style:dashed;border-color:grey;'>" .
            "<TR><TD COLSPAN=1><FONT FACE='sans,arial' SIZE=2>" .
            "<B>ParticleStats results link and command</B></TD></TR>" .
            "<TR><TD><FONT FACE='sans,arial' SIZE=2>" .
            "<B>Static link available for 1 week</B>:<BR>" .
            "<A HREF='$webspace/PS_Out/$Directory' STYLE='TEXT-DECORATION: NONE'>" .
            "$webspace/PS_Out/$Directory</A>" .
            "<P><B>Command Line Given</B>:<BR>" .
            "<FONT FACE=courier SIZE=1>$Command</TD></TR>" .
            "<TR><TD VALIGN=top COLSPAN=1>" . $Runner . "</TD></TR></TABLE>";

  return ($Output, $Directory);
}

sub Directionality
{
  return <<"END_HTML";
<FORM ACTION='ParticleStats_Web.pl' METHOD='post' ENCTYPE='multipart/form-data'>
<INPUT TYPE='HIDDEN' NAME='Phase' VALUE='Directionality'>
<INPUT TYPE='HIDDEN' NAME='Step' VALUE='Run'>

<TABLE WIDTH=800 BGCOLOR=white STYLE='border:1px;border-style:dashed;border-color:grey'>
<TR><TD COLSPAN=2 VALIGN=top>

<FONT FACE='sans,arial' SIZE=3><B>ParticleStats:Directionality:</B><P ALIGN=justify>
<FONT FACE='sans,arial' SIZE=2>
Select an excel file with particle coordinates and an example image from an image stack. Ideally the images will be in 8-bit TIFF format, however JPEG,GIF and PNG formats are accepted. Also select the number of the squares to perform the analysis, the more squares the finer the resolotion. If an orientation line has been provided for the particles/images then select this option for automatic rotation of the image and coordinates. To restric the analysis to a Region of Interest (ROI), input a seties of polygon points describing the ROI (e.g. 0 [368.0, 208.0])
<P></TD></TR>
<TR BGCOLOR=CC99CC>
<TD VALIGN=top><FONT FACE='sans,arial' SIZE=2>Run example</TD>
<TD><FONT FACE='sans,arial' SIZE=2><INPUT TYPE=CHECKBOX NAME='OPT_Example'> 
Leave Excel and Tif Input fields blank<BR>
&nbsp&nbsp&nbsp&nbsp&nbsp The Example is a Drosophila oocyte tracking experiment from Parton <I>et al</I>, 2010, <I>In preparation</I><BR>
&nbsp&nbsp&nbsp&nbsp&nbsp The two files can be downloaded <A HREF='$webspace/PS_Out/DirectionalityExample.xls' STYLE='TEXT-DECORATION: NONE'>[File 1]</A> 
<A HREF='$webspace/PS_Out/DirectionalityExample.xls' STYLE='TEXT-DECORATION: NONE'>[File 2]</A><BR>
&nbsp&nbsp&nbsp&nbsp&nbsp To use the ROI feature cut & paste the coordinated from this file: <A HREF='$webspace/PS_Out/DirectionalityExample_polygon.txt' STYLE='TEXT-DECORATION: NONE'>[ROI]</A>
     "<P>The example takes 2-3 minutes to run, so please be patient
</TD></TR>
<TR BGCOLOR=whitesmoke>
<TD><FONT FACE='sans,arial' SIZE=2>Excel File to Upload</TD>
<TD><INPUT SIZE=50 TYPE='file' NAME='excel1'></TD></TR>
<TR BGCOLOR=whitesmoke>
<TD><FONT FACE='sans,arial' SIZE=2>Image File to Upload</TD>
<TD><INPUT SIZE=50 TYPE='file' NAME='tiff1'></TD></TR>

<TR BGCOLOR=whitesmoke>
<TD><FONT FACE='sans,arial' SIZE=2>Number of Squares</FONT></TD>
<TD><SELECT NAME='OPT_Squares'
STYLE='font-family:sans;font-size:10pt;background-color:whitesmoke'>
<OPTION VALUE='1'>1
<OPTION VALUE='4'>4
<OPTION VALUE='16'>16
<OPTION VALUE='64'>64
<OPTION VALUE='256'>256
<OPTION VALUE='1024'>1024
</TD></TR>
<TR BGCOLOR=whitesmoke>
<TD><FONT FACE='sans,arial' SIZE=2>Axis Rotation</FONT></TD>
<TD><INPUT TYPE=CHECKBOX NAME='OPT_AxisRotate' CHECKED></TD></TR>

<TR BGCOLOR=whitesmoke>
<TD><FONT FACE='sans,arial' SIZE=2 COLOR=black>Axis Labels</TD>
<TD><INPUT TYPE='TEXT' NAME='OPT_AxisLabels' SIZE=6 VALUE='NSWE'
STYLE='font-family:sans;font-size:10pt;color:black;
background-color:whitesmoke'> <FONT FACE='sans,arial' SIZE=2 COLOR=black>
<B>N</B>orth <B>S</B>outh <B>W</B>est <B>E</B>ast</TD></TR>

<TR BGCOLOR=whitesmoke>
<TD><FONT FACE='sans,arial' SIZE=2>Show Arrows</FONT></TD>
<TD><INPUT TYPE=CHECKBOX NAME='OPT_ShowArrows' CHECKED></TD></TR>
<TR BGCOLOR=whitesmoke>
<TD><FONT FACE='sans,arial' SIZE=2>Show Grid</FONT></TD>
<TD><INPUT TYPE=CHECKBOX NAME='OPT_ShowGrid' CHECKED></TD></TR>
<TR BGCOLOR=whitesmoke>
<TD><FONT FACE='sans,arial' SIZE=2>Show Rectangles</FONT></TD>
<TD><INPUT TYPE=CHECKBOX NAME='OPT_ShowRectangles' CHECKED></TD></TR>
<TR BGCOLOR=whitesmoke>
<TD><FONT FACE='sans,arial' SIZE=2>Scale Rose Diagrams</FONT></TD>
<TD><INPUT TYPE=CHECKBOX NAME='OPT_ScaleRose' CHECKED></TD></TR>

<TR BGCOLOR=whitesmoke>
<TD><FONT FACE='sans,arial' SIZE=2>Arrow Colour</FONT></TD>
<TD><SELECT NAME='OPT_ArrowColour'
STYLE='font-family:sans;font-size:10pt;background-color:whitesmoke'>
<OPTION VALUE='white'>white
<OPTION VALUE='black'>black
<OPTION VALUE='red'>red
<OPTION VALUE='blue'>blue
<OPTION VALUE='green'>green
<OPTION VALUE='brown'>brown
<OPTION VALUE='gold'>gold
<OPTION VALUE='maroon'>maroon
<OPTION VALUE='purple'>purple
<OPTION VALUE='orange'>orange
<OPTION VALUE='yellow'>yellow
<OPTION VALUE='silver'>silver
<OPTION VALUE='cyan'>cyan
<OPTION VALUE='magenta'>magenta
<OPTION VALUE='darkgreen'>darkgreen
<OPTION VALUE='steelblue'>steelblue
<OPTION VALUE='orchid'>orchid
<OPTION VALUE='darkviolet'>darkviolet
<OPTION VALUE='salmon'>salmon
<OPTION VALUE='grey'>grey
</TD></TR>

<TR BGCOLOR=whitesmoke>
<TD><FONT FACE='sans,arial' SIZE=2>ROI Line Colour</FONT></TD>
<TD><SELECT NAME='OPT_ROIColour'
STYLE='font-family:sans;font-size:10pt;background-color:whitesmoke'>
<OPTION VALUE='white'>white
<OPTION VALUE='black'>black
<OPTION VALUE='red'>red
<OPTION VALUE='blue'>blue
<OPTION VALUE='green'>green
<OPTION VALUE='brown'>brown
<OPTION VALUE='gold'>gold
<OPTION VALUE='maroon'>maroon
<OPTION VALUE='purple'>purple
<OPTION VALUE='orange'>orange
<OPTION VALUE='yellow'>yellow
<OPTION VALUE='silver'>silver
<OPTION VALUE='cyan'>cyan
<OPTION VALUE='magenta'>magenta
<OPTION VALUE='darkgreen'>darkgreen
<OPTION VALUE='steelblue'>steelblue
<OPTION VALUE='orchid'>orchid
<OPTION VALUE='darkviolet'>darkviolet
<OPTION VALUE='salmon'>salmon
<OPTION VALUE='grey'>grey
</TD></TR>

<TR BGCOLOR=whitesmoke>
<TD><FONT FACE='sans,arial' SIZE=2>ROI Polygon</FONT></TD>
<TD><TEXTAREA NAME='OPT_ROI' ROWS=10 COLS=30 WRAP=hard
STYLE='font-size:8pt;color:black;background-color:white'></TEXTAREA></TD></TR>

<TR BGCOLOR=whitesmoke><TD COLSPAN=2>
<INPUT TYPE='submit' NAME='Submit' VALUE='Submit'>
<INPUT TYPE='reset' VALUE='Reset'>
</TR></TR></TABLE>
</FORM></FONT><P>

END_HTML
}

#------------------------------------------------------------------------------
sub Kymographs {
my $Output;

$Output  = "<FORM ACTION='ParticleStats_Web.pl' METHOD='post' ENCTYPE='multipart/form-data'>" .
           "<INPUT TYPE='HIDDEN' NAME='Phase' VALUE='Kymographs'>" .
           "<INPUT TYPE='HIDDEN' NAME='Step' VALUE='Run'>";

$Output .= "<TABLE WIDTH=800 BGCOLOR=white " . 
           "STYLE='border:1px;border-style:dashed;border-color:grey'>";
$Output .= "<TR><TD COLSPAN=2 VALIGN=top>";
$Output .= "<FONT FACE='sans,arial' SIZE=3>" .
           "<B>ParticleStats:Kymographs:</B><P ALIGN=justify><FONT FACE='sans,arial' SIZE=2>" . 
           "Select an excel file and a zip/tar archive containing the kymograph images. Ideally the images will be in 8-bit TIFF format, however JPEG,GIF and PNG formats are accepted. Then decide upon a noise estimation method. Segmented calculatd the noise based on the three pixels at the edges of the images, segmented_diag also calculated the noise from three pixels, but on diagonals from the top center of the images. The threshold determined what proportion of the intensities over the noise estimate to consider in the weighted intensity calculations. Finally a range of times can be specified to restrict the analysis to a particular range of times." .
           "<P></TD></TR>".
           "<TR BGCOLOR=CC99CC>" .
           "<TD VALIGN=top><FONT FACE='sans,arial' SIZE=2>Run example</TD>" .
           "<TD><FONT FACE='sans,arial' SIZE=2><INPUT TYPE=CHECKBOX NAME='OPT_Example'> " .
           "Leave Excel and image input fields blank<BR>" .
           "&nbsp&nbsp&nbsp&nbsp&nbsp The examples are a wt experiment and variant from Oliviera <I>et al</I>, Nature Cell Biology, 2010 <A HREF='http://dx.doi.org/10.1038/ncb2018' STYLE='text-decoration: none;'>[DOI]</A><BR>" .
           "&nbsp&nbsp&nbsp&nbsp&nbsp The two files can be downloaded <A HREF='$webspace/PS_Out/KymographExample.xls' STYLE='TEXT-DECORATION: NONE'>[File 1]</A> " .
           "<A HREF='$webspace/PS_Out/KymographExample.zip' STYLE='TEXT-DECORATION: NONE'>[File 2]</A><BR>" .
           "<P>The example takes 2-3 minutes to run, so please be patient" .
           "</TD></TR>".

           "<TR BGCOLOR=whitesmoke>" .
           "<TD><FONT FACE='sans,arial' SIZE=2>Excel File to Upload</TD>" . 
           "<TD><FONT FACE='sans,arial' SIZE=2><INPUT SIZE=50 TYPE='file' NAME='excel1'></TD></TR>" .
           "<TR BGCOLOR=whitesmoke>" .
           "<TD><FONT FACE='sans,arial' SIZE=2>Image Archive (zip/tar.gz) to Upload</TD>" .  
           "<TD><INPUT SIZE=50 TYPE='file' NAME='tiffcomp'></TD></TR>";
$Output .= "<TR BGCOLOR=whitesmoke>" . 
           "<TD><FONT FACE='sans,arial' SIZE=2>Noise Estimation Method</FONT></TD>" .
           "<TD><SELECT NAME='OPT_Noise' " .
           "STYLE='font-family:sans;font-size:10pt;background-color:whitesmoke'>".
           "<OPTION VALUE='segmented'>segmented\n" .
           "<OPTION VALUE='segmented_diag'>segmented_diag\n" .
           "<OPTION VALUE='None'>None\n" .
           "</TD></TR>";
$Output .= "<TR BGCOLOR=whitesmoke>" . 
            "<TD><FONT FACE='sans,arial' SIZE=2>Noise Threshold</TD>" .
           "<TD><INPUT TYPE='TEXT' NAME='OPT_Threshold' SIZE=6 VALUE='0.10' " .
           "STYLE='font-family:sans;font-size:10pt;color:black;" .
           "background-color:whitesmoke'></TD></TR>";
$Output .= "<TR BGCOLOR=whitesmoke>" . 
           "<TD><FONT FACE='sans,arial' SIZE=2 COLOR=black>Time Frame Start</TD>" .
           "<TD><INPUT TYPE='TEXT' NAME='OPT_TimeStart' SIZE=6 VALUE='6' " .
           "STYLE='font-family:sans;font-size:10pt;color:black;" .
           "background-color:whitesmoke'></TD></TR>" .
           "<TR BGCOLOR=whitesmoke>" . 
           "<TD><FONT FACE='sans,arial' SIZE=2 COLOR=black>Time Frame End</TD>" .
           "<TD><INPUT TYPE='TEXT' NAME='OPT_TimeEnd' SIZE=6 VALUE='18' " .
           "STYLE='font-family:sans;font-size:10pt;color:black;" .
           "background-color:whitesmoke'></TD></TR>";

$Output .= "<TR BGCOLOR=whitesmoke><TD COLSPAN=2>" .
           "<INPUT TYPE='submit' NAME='Submit' VALUE='Submit'>" . 
           "<INPUT TYPE='reset' VALUE='Reset'>";
$Output .= "</TD></TR></TABLE>";
$Output .= "</FORM></FONT><P>";

return $Output;
}

#------------------------------------------------------------------------------
sub Compare {

my $Output;

$Output  = "<FORM ACTION='ParticleStats_Web.pl' METHOD='post' ENCTYPE='multipart/form-data'>" .
           "<INPUT TYPE='HIDDEN' NAME='Phase' VALUE='Compare'>" .
           "<INPUT TYPE='HIDDEN' NAME='Step' VALUE='Run'>";

$Output .= "<TABLE WIDTH=800 BGCOLOR=white " . 
           "STYLE='border:1px;border-style:dashed;border-color:grey'>";
$Output .= "<TR BGCOLOR=white>" . 
           "<TD COLSPAN=2 VALIGN=top><FONT FACE='sans,arial' SIZE=3>" .
           "<B>ParticleStats:Compare:</B><P ALIGN=justify><FONT FACE='sans,arial' SIZE=2>" . 
           "Select two excel files containing coordinate datasets for comparison. Next chose a Pause Definition Style to determine how the runs and paused are calculated. The variables for runs and pauses (Run Distance, Run Frames, Pause Distance, Pause Duration, Pause Speed, Pause Frames) can also be altered. The output options (Trails, Graphs, Regression) determine which graphs are produced by the ParticleStats:Compare program. Time Start/End specifiy a time range to perform the analysis, if not selected then the whole time range of the data sets are used. Tracking Dimensions and the Pixel Ratio are also customisable" .

           "<P>The example takes 2-3 minutes to run, so please be patient" .
           "</TD></TR>".

           "<TR BGCOLOR=CC99CC>" .
           "<TD VALIGN=top><FONT FACE='sans,arial' SIZE=2>Run example</TD>" .  
           "<TD><FONT FACE='sans,arial' SIZE=2><INPUT TYPE=CHECKBOX NAME='OPT_Example'> " . 
           "Leave Excel File Input fields blank<BR>" .
           "&nbsp&nbsp&nbsp&nbsp&nbsp The Example are a wt experiment and variant from Oliviera <I>et al</I>, Nature Cell Biology, 2010, <A HREF='http://dx.doi.org/10.1038/ncb2018' STYLE='text-decoration: none;'>[DOI]</A><BR>" .
           "&nbsp&nbsp&nbsp&nbsp&nbsp The two excel files can be downloaded <A HREF='$uploaddir/CompareExample_control.xls' STYLE='TEXT-DECORATION: NONE'>[File 1]</A> " .
           "<A HREF='$uploaddir/CompareExample_variant.xls' STYLE='TEXT-DECORATION: NONE'>[File 2]</A>" .
           "</TD></TR>".
           "<TR BGCOLOR=whitesmoke>" . 
           "<TD><FONT FACE='sans,arial' SIZE=2>Excel File 1 to Upload</TD>" . 
           "<TD><INPUT SIZE=50 TYPE='file' NAME='excel1'></TD></TR>" .
           "<TR BGCOLOR=whitesmoke>" . 
           "<TD><FONT FACE='sans,arial' SIZE=2>Excel File 2 to Upload</TD>" . 
           "<TD><FONT FACE='sans,arial' SIZE=2><INPUT SIZE=50 TYPE='file' NAME='excel2'></TD>" .
           "</TR>";

$Output .= "<TR BGCOLOR=whitesmoke><TD><FONT FACE='sans,arial' SIZE=2>" .
           "<FONT COLOR=black>Pause Definition Style</TD>" .
           "<TD><SELECT NAME='OPT_Pauses' " . 
           "STYLE='font-family:sans;font-size:10pt;background-color:whitesmoke'> " .
           "<OPTION VALUE='distance'>Pauses Distance and Duration\n" .
           "<OPTION VALUE='speed'>Pause Frames and Speed\n" .
           "</TD></TR>";

$Output .= "<TR BGCOLOR=whitesmoke>" . 
#           "<TD><FONT FACE='sans,arial' SIZE=2>Trails</TD>" .
#           "<TD><INPUT TYPE=CHECKBOX NAME='OPT_Trails'></TD></TR>" .
#           "<TR BGCOLOR=whitesmoke>" . 
           "<TD><FONT FACE='sans,arial' SIZE=2 COLOR=black>Graphs</TD>" .
           "<TD><INPUT TYPE=CHECKBOX NAME='OPT_Graphs' CHECKED></TD></TR>" .
           "<TR BGCOLOR=whitesmoke>" . 
           "<TD><FONT FACE='sans,arial' SIZE=2 COLOR=black>Regression</TD>" .
           "<TD><INPUT TYPE=CHECKBOX NAME='OPT_Regression' CHECKED></TD></TR>"; 

$Output .= "<TR BGCOLOR=whitesmoke>" . 
           "<TD><FONT FACE='sans,arial' COLOR=black SIZE=2>Run Distance (min)</TD>" .
           "<TD><INPUT TYPE='TEXT' NAME='OPT_RunDistance' SIZE=6 VALUE='0.8' " .
           "STYLE='font-family:sans;font-size:10pt;color:black;" .
           "background-color:whitesmoke'></TD></TR>" .
           "<TR BGCOLOR=whitesmoke>" . 
           "<TD><FONT FACE='sans,arial' COLOR=black SIZE=2>Run Frames (min)</TD>" .
           "<TD><INPUT TYPE='TEXT' NAME='OPT_RunFrames' SIZE=6 VALUE='0' " .
           "STYLE='font-family:sans;font-size:10pt;color:black;" .
           "background-color:whitesmoke'></TD></TR>" .
           "<TR BGCOLOR=whitesmoke>" . 
           "<TD><FONT FACE='sans,arial' SIZE=2>Pause Distance (min)</TD>" .
           "<TD><INPUT TYPE='TEXT' NAME='OPT_PauseDistance' SIZE=6 VALUE='0.5' " .
           "STYLE='font-family:sans;font-size:10pt;color:black;" .
           "background-color:whitesmoke'></TD></TR>" .
           "<TR BGCOLOR=whitesmoke>" . 
           "<TD><FONT FACE='sans,arial' SIZE=2>Pause Duration (min)</TD>" .
           "<TD><INPUT TYPE='TEXT' NAME='OPT_PauseDuration' SIZE=6 VALUE='2000' " .
           "STYLE='font-family:sans;font-size:10pt;color:black;" .
           "background-color:whitesmoke'></TD></TR>" .
           "<TR BGCOLOR=whitesmoke>" . 
           "<TD><FONT FACE='sans,arial' SIZE=2 COLOR=black>Pause Speed (max)</TD>" .
           "<TD><INPUT TYPE='TEXT' NAME='OPT_PauseSpeed' SIZE=6 VALUE='0.4' " .
           "STYLE='font-family:sans;font-size:10pt;color:black;" .
           "background-color:whitesmoke'></TD></TR>" .
           "<TR BGCOLOR=whitesmoke>" . 
           "<TD><FONT FACE='sans,arial' SIZE=2 COLOR=black>Pause Frames (min)</TD>" .
           "<TD><INPUT TYPE='TEXT' NAME='OPT_PauseFrames' SIZE=6 VALUE='5' " .
           "STYLE='font-family:sans;font-size:10pt;color:black;" .
           "background-color:whitesmoke'></TD></TR>" .
           "<TR BGCOLOR=whitesmoke>" . 
           "<TD><FONT FACE='sans,arial' SIZE=2 COLOR=black>Time Start</TD>" .
           "<TD><INPUT TYPE='TEXT' NAME='OPT_TimeStart' SIZE=6 VALUE='0' " .
           "STYLE='font-family:sans;font-size:10pt;color:black;" .
           "background-color:whitesmoke'></TD></TR>" .
           "<TR BGCOLOR=whitesmoke>" . 
           "<TD><FONT FACE='sans,arial' SIZE=2 COLOR=black>Time End</TD>" .
           "<TD><INPUT TYPE='TEXT' NAME='OPT_TimeEnd' SIZE=6 VALUE='500' " .
           "STYLE='font-family:sans;font-size:10pt;color:black;" .
           "background-color:whitesmoke'></TD></TR>" .
           "<TR BGCOLOR=whitesmoke><TD><FONT FACE='sans,arial' SIZE=2>Tracking Dimensions</TD>" .
           "<TD><SELECT NAME='OPT_Dimensions' " .
           "STYLE='font-family:sans;font-size:10pt;color:black;background-color:whitesmoke'>".
           "<OPTION VALUE='2D'>2D\n"."<OPTION VALUE='1DX'>1DX\n"."<OPTION VALUE='1DY'>1DY\n" .
           "</TD></TR>" .
           "<TR BGCOLOR=whitesmoke><TD><FONT FACE='sans,arial' SIZE=2>Pixel Ratio</TD>" .
           "<TD><INPUT TYPE='TEXT' NAME='OPT_Pixels' SIZE=6 VALUE='0.15' " .
           "STYLE='font-family:sans;font-size:10pt;color:black;" .
           "background-color:whitesmoke'></TD></TR>";

$Output .= "<TR BGCOLOR=whitesmoke><TD COLSPAN=2>" .
           "<INPUT TYPE='submit' NAME='Submit' VALUE='Submit'>" . 
           "<INPUT TYPE='reset' VALUE='Reset'>";

$Output .= "</TD></TR></TABLE>";

$Output .= "</FORM></FONT><P>";

return $Output;
}


sub Start_Page
{
  my $cgi_url = CGI::url();

  return <<"END_HTML";
<TABLE BGCOLOR='white' WIDTH=800 STYLE='border:1px;border-style:dashed;border-color:grey'>
  <TR><TD COLSPAN=2><FONT FACE='sans,arial' SIZE=2>
  <B>Welcome to ParticleStats 2.0: </B><BR>A suite of tools for the analysis, comparison, and optimization of tracking data 
  <P>
  <I>ParticleStats:Compare:</I>
  The dynamics of particle movement, such as in the case of motor driven transport, can be explored through the calculation of runs and pauses in the movement. Statistical comparisons can be made between different populations of particles such as in the case of a wild type Vs mutant.
  <P>
  <I>ParticleStats:Directionality:</I>
  The directionality of a set of tracked particles is determined using directional statistics. The windmaps are a novel way of visualising bias in the travel direction of particles. Further evidence is provided with rose diagrams and radial histograms.
  <P>
  <I>ParticleStats:Kymographs:</I>
  Analysis of the dynamics of separating kinetochores as displayed in kymographs<P>

  <B>Please Select ParticleStats Program To Use:</B></TD></TR>
  <TR><TD VALIGN=top ALIGN=center>

  <TABLE BGCOLOR=whitesmoke STYLE='border:0px;border-style:solid'>

    <TR HEIGHT=100 BGCOLOR=white>
    <TD VALIGN=middle><FONT FACE='sans,arial' SIZE=4>1. <FONT COLOR='grey'>ParticleStats::</FONT>Compare</TD>
    <TD width=35 ALIGN=center><FONT FACE='sans,arial' SIZE=2>v1.0</TD>
    <TD VALIGN=MIDDLE><A HREF='$cgi_url?Phase=Compare&Step=Start'>
    <IMG SRC='Images/compare_logo_100px.png' BORDER=0></A></TD>
    <TD VALIGN=middle><FONT FACE='sans,arial' SIZE=2>
    <A HREF='$cgi_url?Phase=Compare&Step=Start' STYLE='TEXT-DECORATION: NONE'>
    Compare Runs & Pauses from Tracked data</A></TD>
    </TR>

    <TR HEIGHT=100 BGCOLOR=white>
    <TD VALIGN=middle><FONT FACE='sans,arial' SIZE=4>2. <FONT COLOR='grey'>ParticleStats::</FONT>Directionality</TD>
    <TD ALIGN=center><FONT FACE='sans,arial' SIZE=2>v1.0</TD>
    <TD><A HREF='$cgi_url?Phase=Directionality&Step=Start'>
    <IMG SRC='Images/directionality_logo_100px.png' BORDER=0></A></TD>
    <TD><FONT FACE='sans,arial' SIZE=2>
    <A HREF='$cgi_url?Phase=Directionality&Step=Start' STYLE='TEXT-DECORATION: NONE'>
    Analyse Directionality from Tracked data</TD>
    </TR>

    <TR HEIGHT=100 BGCOLOR=white>
    <TD VALIGN=middle><FONT FACE='sans,arial' SIZE=4>3. <FONT COLOR='grey'>ParticleStats::</FONT>Kymographs</TD>
    <TD ALIGN=center><FONT FACE='sans,arial' SIZE=2>v1.0</TD>
    <TD><A HREF='$cgi_url?Phase=Kymographs&Step=Start'>
    <IMG SRC='Images/kymograph_logo_100px.png' BORDER=0></TD>
    <TD><FONT FACE='sans,arial' SIZE=2>
    <A HREF='$cgi_url?Phase=Kymographs&Step=Start' STYLE='TEXT-DECORATION: NONE'>
    Analyse Data from Kymographs images</TD>
    </TR>

    <TR HEIGHT=100 BGCOLOR=white>
    <TD VALIGN=middle><FONT FACE='sans,arial' SIZE=4>4. <FONT COLOR='grey'>ParticleStats::</FONT>Behavioural</TD>
    <TD ALIGN=center><FONT FACE='sans,arial' SIZE=2 COLOR='red'>v2.0</TD>
    <TD><A HREF='$cgi_url?Phase=Behavioural&Step=Start'>
    <IMG SRC='Images/directionality_logo_100px.png' BORDER=0></TD>
    <TD><FONT FACE='sans,arial' SIZE=2>
    <A HREF='$cgi_url?Phase=Behavioural&Step=Start' STYLE='TEXT-DECORATION: NONE'>
    Analyse Data from Behavioural assays</TD>
    </TR>

    <TR HEIGHT=100 BGCOLOR=white>
    <TD VALIGN=middle><FONT FACE='sans,arial' SIZE=4>5. <FONT COLOR='grey'>ParticleStats::</FONT>TrackAlign</TD>
    <TD ALIGN=center><FONT FACE='sans,arial' SIZE=2 COLOR='red'>v2.0</TD>
    <TD><A HREF='$cgi_url?Phase=TrackAlign&Step=Start'>
    <IMG SRC='Images/directionality_logo_100px.png' BORDER=0></TD>
    <TD><FONT FACE='sans,arial' SIZE=2>
    <A HREF='$cgi_url?Phase=TrackAlign&Step=Start' STYLE='TEXT-DECORATION: NONE'>
    Compare tracking data</TD>
    </TR>


  </TABLE>

  </TD></TR>
</TABLE>
END_HTML
}

sub get_index_html
{
  my $Output = shift;
  my $ga_id = shift;

  my $header = CGI::header("text/html");
  return <<"END_HTML";
$header
<HTML>
<HEAD>
<TITLE>ParticleStats2.0</TITLE>

<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');
  ga('create', '$ga_id', 'ox.ac.uk');
  ga('send', 'pageview');
</script>

</HEAD>

<BODY>
  <TABLE WIDTH=800 STYLE='border:1px;border-style:dashed;border-color:grey'>
    <TR><TD COLSPAN=1 ALIGN=left VALIGN=top width=250>
    <A HREF='http://www.ParticleStats.com'>
    <IMG SRC='$webspace/Images/PS_Logo_Simple_100px.png' BORDER=0></A><BR>
    <FONT FACE='sans,arial' SIZE=2 COLOR=black>
    <B>A suite of tools for the analysis, comparison, and optimization of tracking data</B>
    </TD><TD><FONT FACE='sans,arial' SIZE=2 COLOR=black>
    <B>By Russell S. Hamilton </B><BR>
    <A HREF='http://www.gen.cam.ac.uk' STYLE='TEXT-DECORATION: NONE'>Department of Genetics, University of Cambridge</A><BR>
    <A HREF='http://www.trophoblast.cam.ac.uk' STYLE='TEXT-DECORATION: NONE'>Centre for Trophoblast Research, University of Cambridge</A><P>
    Contact:<BR>&nbsp &nbsp rsh46 -at- cam.ac.uk<BR>
    &nbsp &nbsp <A HREF='http://www.particlestats.com'
    STYLE='TEXT-DECORATION: NONE'>[www.particlestats.com]</A>
    </TD></TR>
    <TR><TD COLSPAN=2><FONT FACE='sans,arial' SIZE=2 COLOR=black>
    <A HREF='$webspace/ParticleStats_Web.pl' STYLE='TEXT-DECORATION: NONE'>[HOME]</A>&nbsp<A HREF='https://github.com/darogan/ParticleStats' STYLE='TEXT-DECORATION: NONE'>[GitHub]</A>&nbsp<A HREF='http://www.particlestats.com' STYLE='TEXT-DECORATION: NONE'>[www.particlestats.com]</A>&nbsp<A HREF='http://www.darogan.co.uk/ParticleStats/ParticleStats_UserGuide.pdf' STYLE='TEXT-DECORATION: NONE'>[ParticleStats_UserGuide.pdf]</A>
    </TD></TR>
  </TABLE>

  <P>$Output<P>

  <TABLE WIDTH=800 STYLE='border:1px;border-style:dashed;border-color:grey'>
    <TR><TD COLSPAN=2 ALIGN=left><FONT FACE='sans,arial' SIZE=2 COLOR=black>
<B>Please cite:</B> 
Hamilton, R.S., Parton, R.M., Oliveira, R.A., Vendra, G., Ball, G., Nasmyth, K. & Davis, I. (2010) ParticleStats: open source software for the analysis of particle motility. <I>Nucl. Acids Res. Web Server Edition</I> <A HREF='http://dx.doi.org/10.1093/nar/GKQ542' STYLE='text-decoration: none;'>[DOI]</A>
    </TD></TR></TABLE> <P>

  <TABLE WIDTH=800 STYLE='border:1px;border-style:dashed;border-color:grey'>
    <TR><TD COLSPAN=2 ALIGN=left><FONT FACE='sans,arial' SIZE=2 COLOR=black>
<B>History:</B><BR>
ParticleStats was originally created by Russell Hamilton and <A HREF='http://www.ilandavis.com' STYLE='TEXT-DECORATION: NONE'>Ilan Davis</A> at the <A HREF='http://www.bioch.ox.ac.uk' STYLE='TEXT-DECORATION: NONE'>Department of Biochemistry, University of Oxford</A> and in collaboration with the <A HREF='http://www.micron.ox.ac.uk' STYLE='TEXT-DECORATION: NONE'>Micron Advanced Imaging Facility</A>.
<P>
<B>Contributions:</B><BR>
Malwina Prater, Graeme Ball, Richard Parton, Alexandra Ashcroft, Ben Shaw 
    </TD></TR></TABLE> <P>


</BODY>
</HTML>
END_HTML
}


sub Print_HTML
{
  my $Output  = shift;
  my $DirRand = shift;

  if (defined $DirRand)
    {
      my $webpage_run = get_index_html ($Output, 'UA-39620323-3');
      $webpage_run =~ s/^Content-Type:.*//g;
      open (WEBPAGE, ">", "$uploaddir/$DirRand/index.html");
      print WEBPAGE $webpage_run;
      close WEBPAGE;
    }
  print get_index_html ($Output, 'UA-39620323-2');
}


sub main
{

  my $q = new CGI;
  my $Phase = $q->param('Phase') // 'Start';
  my $Step = $q->param('Step') // '';

  my %subs = (
    Directionality => \&Directionality,
    Compare => \&Compare,
    Kymographs => \&Kymographs,
  );

  if (! defined $subs{$Phase})
    {
      $Phase = "Start";
      Print_HTML (Start_Page ());
    }
  elsif ($Step eq "Run")
    {
      my ($Output, $DirRand) = Process ($Phase, $q, $uploaddir);
      Print_HTML ($Output, $DirRand);
    }
  else # we have a phase but step is invalid or unset, so same as Start
    {
      Print_HTML (&{$subs{$Phase}} ());
    }

  Tracker($Phase, $uploaddir);
}

main ();
