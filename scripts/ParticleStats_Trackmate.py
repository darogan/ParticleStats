#!/usr/bin/env python
"""
Script to extract track data from Fiji's Trackmate tracker,
and export .csv text data for ParticleStats.
"""
__author__ = "Graeme Ball (graemeball@googlemail.com)"
__copyright__ = "Copyright (c) 2013 Graeme Ball"
__license__ = "GPL v3"  # http://www.gnu.org/licenses/gpl.txt
__version__ = "1.0beta"

import sys, os
import argparse
import xml.etree.ElementTree as ET

###############################################################################
# PARSE IN THE USER OPTIONS AND ERROR CHECK

parser = argparse.ArgumentParser(description='ParticleStats_Trackmate.py is a tool for converting trackmate to CSV format to import into Excel')

parser.add_argument('-x', '--xml',           dest='filepath',      action="store", required=True, help='trackmate xml file')
parser.add_argument("-i", "--image",         dest="image_name",    action="store", required=True, help="image single frame jpg")
parser.add_argument("-t", "--time_interval", dest="time_interval", action="store", required=True, help="time interval (between 0 and 10000)")

(options) = parser.parse_args()

if( os.path.exists(str(options.filepath)) != 1):
    print "ERROR: XML file does not exists - check correct path and name"
    sys.exit(0)
#if( os.path.exists(str(options.image_name)) != 1):
#    print "ERROR: image file does not exists - check correct path and name"
#    sys.exit(0)

(FileName,FileExt) = os.path.splitext(options.image_name)
if FileExt != ".tif" and FileExt != ".jpg"  and FileExt != ".gif" and \
   FileExt != ".png" and FileExt != ".jpeg" and FileExt != ".tiff":
   print "ERROR: Image file is not in a supported format Tif(8bit)/PNG/JPG/GIF", options.image_name
   sys.exit(0)

try:
   options.time_interval = float(options.time_interval)
except ValueError:
   print "ERROR: time interval not a float"
   sys.exit(0)
if (options.time_interval <= 0) or (options.time_interval >= 10000) :
   print "ERROR: time interval should be over 0 and less than 10000" 
   sys.exit(0)

###############################################################################
# GLOBAL VARIABLES

trackdata = []  # track data: list of tracks 
                # each track itself a list dicts, one dict per point
point_keys = 'track_no', 'x', 'y', 'z', 't'  # dict keys for points
pstats_fields = "Track #,X,Y,Z,Time Interval,Frame #,Image Name"


###############################################################################
# MAIN CODE

def main():
    filepath      = options.filepath
    image_name    = options.image_name
    time_interval = options.time_interval
    xml_root = import_xml(filepath)
    trackdata = extract_trackdata(xml_root)
    export_pstats(trackdata, image_name, time_interval)

def import_xml(filepath):
    """
    return xml_root
    """
    fh = open(filepath, 'r')
    xml_data = fh.read()
    fh.close()
    xml_root = ET.fromstring(xml_data)
    return xml_root

def extract_trackdata(xml_root):
    """
    using xml_root of trackmate data, build and 
    return trackdata (list of lists of dicts of trackdata)
    """
    particle_sets = xml_root.findall('particle')
    track_no = 0
    for particle_set in particle_sets:
        track_no += 1
        detections = particle_set.findall('detection')
        track = []
        for detection in detections:
            point = {'track_no': track_no}
            for key in detection.keys():
                coordinate = detection.get(key)
                point[key] = coordinate
            track.append(point)
        trackdata.append(track)
    return trackdata

def export_pstats(trackdata, image_name, time_interval):
    """
    print pstats format trackdata to stdout
    """
#    print(pstats_fields)
    for track in trackdata:
        for point in track:
            print("%d,%.3f,%.3f,%.3f,%.4f,%d,%s" % (1+point['track_no'], 
                float(point['x']), float(point['y']), float(point['z']), 
                time_interval, int(point['t'])+1, image_name))

if __name__ == "__main__":
    main()
