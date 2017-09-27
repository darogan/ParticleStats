#!/bin/bash -f
###############################################################################
#       _____                _       _    _ _                                 #
#      |_   _|_ __ __ _  ___| | __  / \  | (_) __ _ _ __                      #
#        | | | '__/ _` |/ __| |/ / / _ \ | | |/ _` | '_ \                     #
#        | | | | | (_| | (__|   < / ___ \| | | (_| | | | |                    #
#        |_| |_|  \__,_|\___|_|\_|_/   \_\_|_|\__, |_| |_|                    #
#                                             |___/                           #
#                                                                             #
###############################################################################
#       TrackAlign: Open source software for the analysis of tracked data     #
#                   to determine optimal parameters and alignment of tracks   #
#                                                                             #
#       Contact: Russell.Hamilton@bioch.ox.ac.uk                              #
#                http://www.TrackAlign.com                                    #
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


FILES=( TrackAlign_man.xls TrackAlign_auto.xls )
IMAGES=( TrackAlign_image.tif )
ROI=( TrackAlign_roiall.txt)
MULTIPLES=(4)
DIR1="examples"

for j in "${MULTIPLES[@]}"
do
   	echo "     Running $j Squares..."

	#--generatestats --typerandomtracks=Random --ntracks=15 \

	time python TrackAlign.py \
        --xls1 $DIR1/${FILES[0]} --tif $DIR1/${IMAGES[0]} \
        --xls2 $DIR1/${FILES[1]} \
        --boundaryfilter -s $j -g -r -a -o text \
	--TimeTolerance=0 \
	--polygon=$DIR1/$ROI \
        --ArrowColour=red --ROIColour=green \
        --outdir=DivisionFiles/ #> TA_results.txt

	exit

   	time python TrackAlign.py \
	--xls1 $DIR1/${FILES[0]} --tif1 $DIR2/${IMAGES[0]}.tif \
	--xls2 $DIR1/${FILES[1]} --tif2 $DIR2/${IMAGES[0]}.tif \
	--boundaryfilter -s $j -g -r -a -p polygon.text -o text \
	--generatestats --typerandomtracks=Random --ntracks=1000 \
	--ArrowColour=red --ROIColour=green \
	--outhtml=http://idcws.bioch.ox.ac.uk/~rhamilto/ParticleStats2/ \
	--outdir=DivisionFiles/ 

	time python TrackAlign.py \
        --xls1=$DIR1/${FILES[0]} --tif1=$DIR2/${IMAGES[0]}.tif \
        --xls2=$DIR1/${FILES[1]} --tif2=$DIR2/${IMAGES[0]}.tif \
        --boundaryfilter -s $j -g -r -a -p polygon.text -o text \
        --generatestats --typerandomtracks=InputWithRandom --ntracks=1000 \
        --outhtml=http://idcws.bioch.ox.ac.uk/~rhamilto/ParticleStats2/ \
        --outdir=DivisionFiles/

	time python TrackAlign.py \
        --xls1 $DIR1/${FILES[0]} --tif1 $DIR2/${IMAGES[0]}.tif \
        --xls2 $DIR1/${FILES[1]} --tif2 $DIR2/${IMAGES[0]}.tif \
        --boundaryfilter -s $j -g -r -a -p polygon.text -o text \
        --generatestats --typerandomtracks=InputWithNoise --ntracks=1000 \
        --outhtml=http://idcws.bioch.ox.ac.uk/~rhamilto/ParticleStats2/ \
        --outdir=DivisionFiles/
done

