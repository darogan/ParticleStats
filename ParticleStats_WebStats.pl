#!/usr/bin/perl -w
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

my($uploaddir, $webspace, $cgidir, $AgeDirectionality, $date, $q, 
   $url, @CounterData, $i, $Webpage, $Output,@TempCounterData, 
   @IPAddress, %IPHash, $cnt, %Country, $GeoLoc, $element,);

###############################################################################
# Change the values in this section to configure the script for your server

if($ENV{'HTTP_HOST'} =~ /idcws.bioch.ox.ac.uk/)
  {
    $uploaddir = "/home/rhamilto/public_html/ParticleStats2/PS_Out/";
    $webspace  = "http://idcws.bioch.ox.ac.uk/~rhamilto/ParticleStats2";
    $cgidir    = "http://idcws.bioch.ox.ac.uk/cgi-particle2";
  }
elsif($ENV{'HTTP_HOST'} =~ /simulans.bioch.ox.ac.uk/)
  {
    $uploaddir = "/home/particlestats/public_html/PS_Out/";
    $webspace  = "http://simulans.bioch.ox.ac.uk/~particlestats/";
    $cgidir    = "http://simulans.bioch.ox.ac.uk/cgi-particle";
  }
else
  {
    $uploaddir = "/home/particlestats/public_html/PS_Out/";
    $webspace  = "http://idcn1.bioch.ox.ac.uk/~particlestats/";
    $cgidir    = "http://idcn1.bioch.ox.ac.uk/cgi-particle";
  }

#Find out the release dates of the 3 programs

use File::stat;
use Time::localtime;
my $Age_Dir = ctime(stat('ParticleStats_Directionality.py')->mtime);
my $Age_Com = ctime(stat('ParticleStats_Compare.py')->mtime);
my $Age_Kym = ctime(stat('ParticleStats_Kymographs.py')->mtime);
my $Age_Web = ctime(stat('ParticleStats_Web.pl')->mtime);

$q = new CGI;

use LWP::Simple;
use XML::Simple;

my $browser = LWP::UserAgent->new;

$date = `date +%F_%H%M`;
chomp($date);

open(COUNTER,"$uploaddir/Counter.text");
@CounterData = <COUNTER>;
close COUNTER;
$cnt = 1;

for($i=0; $i<=$#CounterData; $i++)
   {
     @TempCounterData = split(/\s+/,$CounterData[$i]);

     if ($IPHash{$TempCounterData[2]} < 1 )
       {
         $IPAddress[$cnt] = $TempCounterData[2];
         $url = "http://ipinfodb.com/ip_query.php?ip=$TempCounterData[2]";
         my $response = $browser->get( $url );
         my $ref = XMLin( $response->content );
         $Country{ $ref->{CountryName} }++;
         $GeoLoc .= "&markers=color:red|" . $ref->{Latitude} . "," . $ref->{Longitude}; 
         $cnt++
       }
     $IPHash{$TempCounterData[2]}++;
   }

$Output .= "<P><TABLE WIDTH=800 STYLE='border:1px;border-style:dashed;border-color:grey'>" .
           "<TR><TD><FONT FACE=sans,arial SIZE=4><B>Visitors using ParticleStats:</B><P>";
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
$Output .= "</TABLE>";
$Output .= "</TD></TR></TABLE>";


$Output .= "<P><TABLE WIDTH=800 STYLE='border:1px;border-style:dashed;border-color:grey'>" .
           "<TR><TD VALIGN=top COLSPAN=2><FONT FACE=sans,arial SIZE=4>" . 
           "<B>Countries using ParticleStats:<P></B></TD></TR>";
$Output .= "<TR><TD>";
$Output .= "<TABLE STYLE='border:1px;border-style:solid;border-color:black'>";
$Output .= "<TR><TD VALIGN=top><FONT FACE=sans,arial SIZE=2><I>Country</I></TD>" .
           "<TD><FONT FACE=sans,arial SIZE=2><I>No Visits</I></TD></TR>";
foreach $element (keys %Country)
  {
     $Output .= "<TR><TD BGCOLOR=whitesmoke><FONT FACE=sans,arial SIZE=2>$element</TD>" . 
                "<TD BGCOLOR=whitesmoke><FONT FACE=sans,arial SIZE=2>$Country{$element}</TD></TR>";   
  }
$Output .= "</TABLE>";
$Output .= "</TD>";

$Output .= "<TD ALIGN=right VALIGN=top><IMG SRC=http://maps.google.com/maps/api/staticmap?center=London,UK&size=512x350&maptype=roadmap". $GeoLoc . "&sensor=false></TD></TR></TABLE>";

#ParticleStats code base last updates
$Output .= "<P><TABLE WIDTH=800 STYLE='border:1px;border-style:dashed;border-color:grey'>" .
           "<TR><TD VALIGN=top COLSPAN=2><FONT FACE=sans,arial SIZE=4>" . 
           "<B>ParticleStats code base last updates:<P></B></TD></TR>";
$Output .= "<TR><TD>";
$Output .= "<TABLE STYLE='border:1px;border-style:solid;border-color:black'>";
$Output .= "<TR><TD VALIGN=top><FONT FACE=sans,arial SIZE=2><I>Program</I></TD>" .
           "<TD><FONT FACE=sans,arial SIZE=2><I>Date</I></TD></TR>";
$Output .= "<TR><TD BGCOLOR=whitesmoke><FONT FACE=sans,arial SIZE=2>ParticleStats:Directionality</TD>" . 
           "<TD BGCOLOR=whitesmoke><FONT FACE=sans,arial SIZE=2>$Age_Dir</TD></TR>";
$Output .= "<TR><TD BGCOLOR=whitesmoke><FONT FACE=sans,arial SIZE=2>ParticleStats:Compare</TD>" .      
           "<TD BGCOLOR=whitesmoke><FONT FACE=sans,arial SIZE=2>$Age_Com</TD></TR>";
$Output .= "<TR><TD BGCOLOR=whitesmoke><FONT FACE=sans,arial SIZE=2>ParticleStats:Kymographs</TD>" .       
           "<TD BGCOLOR=whitesmoke><FONT FACE=sans,arial SIZE=2>$Age_Kym</TD></TR>";
$Output .= "<TR><TD BGCOLOR=whitesmoke><FONT FACE=sans,arial SIZE=2>ParticleStats:Web</TD>" .       
           "<TD BGCOLOR=whitesmoke><FONT FACE=sans,arial SIZE=2>$Age_Web</TD></TR>";
$Output .= "</TABLE>";
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
            "<B>Open source software for the analysis of intracellular " .
            "particle motility and cytoskeletal polarity</B>" .
            "</TD><TD><FONT FACE='sans,arial' SIZE=2 COLOR=black>" .
            "<B>By Russell S. Hamilton & Ilan Davis</B><BR>" .
            "Department of Biochemistry, University of Oxford<P>" .
            "Contact:<BR>&nbsp &nbsp Russell.Hamilton -at- bioch.ox.ac.uk<BR>" .
            "&nbsp &nbsp <A HREF='http://www.ilandavis.com' " .
            "STYLE='TEXT-DECORATION: NONE'>[www.ilandavis.com]</A>" .
            "&nbsp &nbsp <A HREF='http://www.particlestats.com' " .
            "STYLE='TEXT-DECORATION: NONE'>[www.particlestats.com]</A>" .
            "</TD></TR>" .
            "<TR><TD COLSPAN=2><FONT FACE='sans,arial' SIZE=2 COLOR=black>" .
            "<A HREF='ParticleStats_Web.pl' STYLE='TEXT-DECORATION: NONE'>[HOME]</A>" .
            "<A HREF='http://www.darogan.co.uk/ParticleStats/ParticleStats_UserGuide.pdf' " . 
            "STYLE='TEXT-DECORATION: NONE'>[ParticleStats_UserGuide.pdf]</A>" .
            "</TD></TR>" .
            "</TABLE>";

$Webpage .= "<P>$Output<P>" .

            "<TABLE WIDTH=800 STYLE='border:1px;border-style:dashed;border-color:grey'>" .
            "<TR><TD COLSPAN=2 ALIGN=center><FONT FACE='sans,arial' SIZE=2 COLOR=black>" .
            "Please cite: Hamilton, R.S., Parton, R.M., Oliveira, R.A., Vendra, G., Ball, G., " . 
            "Nasmyth, K. & Davis, I. (2010) ParticleStats: open source software for the analysis " . 
            "of particle motility. <I>Nucl. Acids Res. Web Server Edition</I> " . 
            "<A HREF='http://dx.doi.org/10.1093/nar/GKQ542' STYLE='text-decoration: none;'>[DOI]</A>" .
            "</TD></TR></TABLE>" . "<P>" .

            "<TABLE WIDTH=800 STYLE='border:1px;border-style:dashed;border-color:grey'>" .
            "<TR><TD COLSPAN=2 ALIGN=center><FONT FACE='sans,arial' SIZE=2 COLOR=black>" .
            "ParticleStats source code last updated on: $Age_Dir</TD></TR>" .
            "<TR><TD ALIGN=center><FONT FACE='sans,arial' SIZE=2>Open Source<BR>" .
            "<A HREF='http://www.opensource.org/docs/definition.php'>" .
            "<IMG SRC='http://opensource.org/trademarks/osi-certified/web/osi-certified-72x60.png' " .
            "border=0 width=72 height=60></a></TD>" .
            "<TD ALIGN=center><FONT FACE='sans,arial' SIZE=2>GNU License<BR>" .
            "<A HREF='http://www.gnu.org'>" .
            "<IMG SRC='$webspace/Images/heckert_gnu.small.png' HEIGHT=60  BORDER=0></A>" .
            "</TD></TR></TABLE>";
$Webpage .= "</BODY></HTML>";

print $Webpage;

#------------------------------------------------------------------------------
# FIN
#-----------------------------------------------------------------------------
