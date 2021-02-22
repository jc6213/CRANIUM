#!/bin/env python
# Script that takes as input a folder of images from a scan, then makes a folder for each well,
# containing a subfolder for each color in that well (Red, Green, Brightfield)
# Run as WellFolders.py path/to/folder DayAsAnInteger

import argparse
import re
import os


# Getting the arguments from the command line
parser = argparse.ArgumentParser(description='Groups a folder full of images into one folder per well '
                                             'with subfolders of red, green, and brightfield',
                                 usage='%(prog)s FOLDERPATH DAYinteger')
parser.add_argument("folderlocation", type=str, help="Path of the folder to modify")
parser.add_argument("day", type=int, help="Which day these pics are from (i.e. Day 3 would just be 3")
args = parser.parse_args()

# Getting a list of all of the images in the folder, then making a list of all the wells represented
allimages = [file for file in os.scandir(args.folderlocation) if file.name.endswith('.tif')]
wells = {image.name[0] + image.name[4:6] for image in allimages}

# Making a parent folder for each well with Red, Green, and Brightfield subfolders
for well in wells:
    for color in ['Red', 'Green', 'Brightfield']:
        os.makedirs(f'{args.folderlocation}/{well}_Day{args.day}/{color}')

# Moving each image file into the correct spot
colordict = {'561': 'Red',
             '488': 'Green',
             'TL-Brightfield': 'Brightfield'}
for image in allimages:
    m = re.match(r'^(?P<row>[A-Z]) - (?P<column>[0-9]{2})\(fld (?P<field>[0-9]{2}) '
                 r'wv (?P<wv>[\w\-]*) - (?P<color>[\w]*)\).tif$', image.name)
    color = colordict[m.group('wv')]
    well = m.group('row') + m.group('column')
    os.rename(image.path, f'{args.folderlocation}/{well}_Day{args.day}/{color}/{image.name}')
