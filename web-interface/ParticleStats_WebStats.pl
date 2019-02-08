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
#	Please cite:                                                          #
#	Hamilton, R.S. et al (2010) Nucl. Acids Res. Web Server Edition       #
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

my($uploaddir, $webspace, $cgidir, $date, $q,
   $url, @CounterData, $i, $Webpage, $Output,@TempCounterData, 
   %ProgramHash, @IPAddress, %IPHash, $cnt, %Country, %City, $element);

###############################################################################
# Change the values in this section to configure the script for your server

if($ENV{'HTTP_HOST'} =~ /ctr-web.pdn.cam.ac.uk/)
  {
    $uploaddir = "/storage/www/ParticleStats2.0/PS_Out/";
    $webspace  = "http://ctr-web.pdn.cam.ac.uk/ParticleStats2.0";
    $cgidir    = "http://ctr-web.pdn.cam.ac.uk/ParticleStats2.0";
  }
else
  {
#    exit;
    $uploaddir = "/storage/www/ParticleStats2.0/PS_Out/";
    $webspace  = "http://ctr-web.pdn.cam.ac.uk/ParticleStats2.0";
    $cgidir    = "http://ctr-web.pdn.cam.ac.uk/ParticleStats2.0";  
  }

$q = new CGI;

use Net::IPInfoDB;
use GD::Graph::pie;
use MIME::Base64;

$date = `date +%F_%H:%M`;
chomp($date);

open(COUNTER,"$uploaddir/Counter.text");
@CounterData = <COUNTER>;
close COUNTER;

#$cnt = 1;

for($i=0; $i<=$#CounterData; $i++)
   {
     @TempCounterData = split(/\s+/,$CounterData[$i]);

     if ($IPHash{$TempCounterData[2]} < 1 )
       {
         my $APIHash = "1ab51f9a73282cc49ba55a2c14ea917f9d23dee1ee71daed0fbbfa2136ea567d";
         my $g = Net::IPInfoDB->new;
         $g->key($APIHash);
         my $city_level = $g->get_city($TempCounterData[2]);

         my $IP_city      = $city_level->city_name;
         my $IP_country   = $city_level->country_name;
         my $IP_latitude  = $city_level->latitude;
         my $IP_longitude = $city_level->longitude;
         if( length($IP_city)    < 1 ) { $IP_city    = "unknown"; }
         if( length($IP_country) < 1 ) { $IP_country = "unknown"; }

         $City{ $IP_city }++;
         $Country{ $IP_country }++;

         sleep(2);
         #$cnt++
       }
     $IPHash{$TempCounterData[2]}++;
     $ProgramHash{$TempCounterData[0]}++;
   }


delete $ProgramHash{'Start'};

my @prog_names  = keys %ProgramHash;
my @prog_counts = values %ProgramHash;

my @data = ( [@prog_names], [@prog_counts] );

my $mygraph = GD::Graph::pie->new(300, 300);
$mygraph->set(
    title       => 'ParticleStats ::: Module Usage',
    '3d'          => 0,
) or warn $mygraph->error;

$mygraph->set_value_font(GD::gdMediumBoldFont);
my $myimage = $mygraph->plot(\@data) or die $mygraph->error;

$Output .= "<P><TABLE WIDTH=800 STYLE='border:1px;border-style:dashed;border-color:grey'>" .
           "<TR><TD><FONT FACE=sans,arial SIZE=4><B>Visitors using ParticleStats:</B>" .
           "</TD><TD></TD></TR><TR><TD>";

my $cnt_all  = 0;
my $cnt_uniq = 0;
foreach $element (keys %IPHash)
  {
     $cnt_all  = $cnt_all + $IPHash{$element};
     $cnt_uniq = $cnt_uniq + 1;
  }
$Output .= "<TABLE STYLE='border:1px;border-style:solid;border-color:black'>";
$Output .= "<TR><TD><FONT FACE=sans,arial SIZE=2>Total Number of Visits</TD>" .
           "<TD BGCOLOR=whitesmoke><FONT FACE=sans,arial SIZE=2>$cnt_all</TD></TR>";
$Output .= "<TR><TD><FONT FACE=sans,arial SIZE=2>Total Unique Visitors (by IP)</TD>" .
           "<TD BGCOLOR=whitesmoke><FONT FACE=sans,arial SIZE=2>$cnt_uniq</TD></TR>";
$Output .= "</TABLE></TD><TD>";


$Output .= "<TABLE STYLE='border:1px;border-style:solid;border-color:black'>";
$Output .= "<TR><TD VALIGN=top><FONT FACE=sans,arial SIZE=2><I>Program Used:</I></TD>" .
           "<TD><FONT FACE=sans,arial SIZE=2><I>No Visits</I></TD></TR>";
foreach $element (keys %ProgramHash)
  {  
     $Output .= "<TR><TD BGCOLOR=whitesmoke><FONT FACE=sans,arial SIZE=2>$element</TD>" .
                "<TD BGCOLOR=whitesmoke><FONT FACE=sans,arial SIZE=2>$ProgramHash{$element}</TD></TR>";
  }
$Output .= "</TABLE>";

$Output .= "</TD><TD>";
$Output .= sprintf('<P><img src="data:image/png;base64,%s"><P>', encode_base64($myimage->png));

$Output .= "</TD></TR></TABLE>";


$Output .= "<P><TABLE WIDTH=800 STYLE='border:1px;border-style:dashed;border-color:grey'>" .
           "<TR><TD VALIGN=top COLSPAN=2><FONT FACE=sans,arial SIZE=4>" . 
           "<B>Geolocation of ParticleStats Visitors:</B></TD></TR>";
$Output .= "<TR><TD>";

$Output .= "<TABLE STYLE='border:1px;border-style:solid;border-color:black'>";
$Output .= "<TR><TD VALIGN=top><FONT FACE=sans,arial SIZE=2><I>Country</I></TD>" .
           "<TD><FONT FACE=sans,arial SIZE=2><I>No Visits</I></TD></TR>";
foreach $element (keys %Country)
  {
     $Output .= "<TR><TD BGCOLOR=whitesmoke><FONT FACE=sans,arial SIZE=2>$element</TD>" . 
                "<TD BGCOLOR=whitesmoke><FONT FACE=sans,arial SIZE=2>$Country{$element}</TD></TR>";   
  }
$Output .= "</TABLE></TD><TD>";

$Output .= "<TABLE STYLE='border:1px;border-style:solid;border-color:black'>";
$Output .= "<TR><TD VALIGN=top><FONT FACE=sans,arial SIZE=2><I>City</I></TD>" .
           "<TD><FONT FACE=sans,arial SIZE=2><I>No Visits</I></TD></TR>";
foreach $element (keys %City)
  {  
     $Output .= "<TR><TD BGCOLOR=whitesmoke><FONT FACE=sans,arial SIZE=2>$element</TD>" .
                "<TD BGCOLOR=whitesmoke><FONT FACE=sans,arial SIZE=2>$City{$element}</TD></TR>";
  }
$Output .= "</TABLE>";

$Output .= "</TD></TR>" .
           "<TR><TD COLSPAN=2>" .
           "<IMG SRC='PS_Out/map.png' WIDTH=750>";

$Output .= "</TD></TR></TABLE>";

#------------------------------------------------------------------------------
# Print out the final HTML

$Webpage =  "Content-type: text/html\n\n";
$Webpage .= "<HTML><HEAD><TITLE>ParticleStats</TITLE></HEAD>";

$Webpage .= "<BODY>" .
            "<TABLE WIDTH=800 STYLE='border:1px;border-style:dashed;border-color:grey'>" .
            "<TR><TD COLSPAN=1 ALIGN=left VALIGN=top width=250>" .
            "<A HREF='http://www.ParticleStats.com'>" .
            "<IMG SRC='$webspace/Images/PS_Logo_Simple_100px.png' BORDER=0></A><BR>" .
            "<FONT FACE='sans,arial' SIZE=2 COLOR=black>" .
            "<B>A suite of tools for the analysis, comparison, and optimization of tracking data</B>" .
            "</TD><TD><FONT FACE='sans,arial' SIZE=2 COLOR=black><B>By Russell S. Hamilton </B><BR>" .
            "<A HREF='http://www.gen.cam.ac.uk' STYLE='TEXT-DECORATION: NONE'>" .
            "Department of Genetics, University of Cambridge</A><BR>" .
            "<A HREF='http://www.trophoblast.cam.ac.uk' STYLE='TEXT-DECORATION: NONE'>" .
            "Centre for Trophoblast Research, University of Cambridge</A><P>" . 
            "Contact:<BR>&nbsp &nbsp rsh46 -at- cam.ac.uk<BR>&nbsp &nbsp <A HREF='http://www.particlestats.com' " .
            "STYLE='TEXT-DECORATION: NONE'>[www.particlestats.com]</A></TD></TR>" .
            "<TR><TD COLSPAN=2><FONT FACE='sans,arial' SIZE=2 COLOR=black>" .
            "<A HREF='$webspace/ParticleStats_Web.pl' STYLE='TEXT-DECORATION: NONE'>[HOME]</A>" .
            "&nbsp<A HREF='https://github.com/darogan/ParticleStats' STYLE='TEXT-DECORATION: NONE'>[GitHub]</A>" . 
            "&nbsp<A HREF='http://www.particlestats.com' STYLE='TEXT-DECORATION: NONE'>[www.particlestats.com]</A>" .
            "&nbsp<A HREF='http://www.darogan.co.uk/ParticleStats/ParticleStats_UserGuide.pdf' " .
            "STYLE='TEXT-DECORATION: NONE'>[ParticleStats_UserGuide.pdf]</A></TD></TR>" .
            "</TABLE>";

$Webpage .= "<P><TABLE WIDTH=800 STYLE='border:1px;border-style:dashed;border-color:grey'>" .
            "<TR><TD><FONT FACE='sans,arial' SIZE=2 COLOR=black>" . 
            "<B>Data Collected at $date</B></FONT></TD></TR></TABLE>";

$Webpage .= "<P>$Output<P>" .

            "<TABLE WIDTH=800 STYLE='border:1px;border-style:dashed;border-color:grey'>" .
            "<TR><TD COLSPAN=2><FONT FACE='sans,arial' SIZE=2 COLOR=black>" .
            "<B>Please cite:</B> Hamilton, R.S., Parton, R.M., Oliveira, R.A., Vendra, G., Ball, G., " . 
            "Nasmyth, K. & Davis, I. (2010) ParticleStats: open source software for the analysis " . 
            "of particle motility. <I>Nucl. Acids Res. Web Server Edition</I> " . 
            "<A HREF='http://dx.doi.org/10.1093/nar/GKQ542' STYLE='text-decoration: none;'>[DOI]</A>" .
            "</TD></TR></TABLE>" . "<P>" .

            "<TABLE WIDTH=800 STYLE='border:1px;border-style:dashed;border-color:grey'>" .
            "<TR><TD COLSPAN=2 ALIGN=left><FONT FACE='sans,arial' SIZE=2 COLOR=black>" .
            "<B>History:</B><BR>" .
            "ParticleStats was originally created by Russell Hamilton and " .
            "<A HREF='http://www.ilandavis.com' STYLE='TEXT-DECORATION: NONE'>Ilan Davis</A> at the " . 
            "<A HREF='http://www.bioch.ox.ac.uk' STYLE='TEXT-DECORATION: NONE'>" . 
            "Department of Biochemistry, University of Oxford</A> and in collaboration with the " . 
            "<A HREF='http://www.micron.ox.ac.uk' STYLE='TEXT-DECORATION: NONE'>Micron Advanced Imaging Facility</A>." .
            "<P><B>Contributions:</B><BR>Malwina Prater, Graeme Ball, Richard Parton, Alexandra Ashcroft, Ben Shaw" .
            "</TD></TR></TABLE>";
$Webpage .= "</BODY></HTML>";

print $Webpage, "\n";

#------------------------------------------------------------------------------
# FIN
#-----------------------------------------------------------------------------
