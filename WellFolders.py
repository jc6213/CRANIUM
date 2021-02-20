#!/bin/env python
# Script that takes as input a folder of images from a scan, which makes subfolders for each well,
# and for each color in that well (red, green, brightfield)
# Run as WellFolders.py (pathname) (day as just an integer)

import argparse
import glob
import re
import os


# function to create a folder as "Well_Day%" with 3 subfolders: Red, Green, Brightfield
def makefolders(well):
    for sub in ['Red', 'Green', 'Brightfield']:
        os.makedirs(f'{well}_Day{args.day}/{sub}')


# and a function to move an image file into the correct directory:
def movepic(file_name):
    m = re.match(r'^(?P<row>[A-Z]) - (?P<column>[0-9]{2})\(fld (?P<field>[0-9]{2}) wv (?P<wv>[\w\-]*) - (?P<color>[\w]*)', file_name)
    colordict = {'561': 'Red',
                 '488': 'Green',
                 'TL-Brightfield': 'Brightfield'}
    color = colordict[m.group('wv')]
    well = m.group('row') + m.group('column')
    os.rename(file_name, f'{well}_Day{args.day}/{color}/{file_name}')


# getting the arguments from the command line
parser = argparse.ArgumentParser(description='Groups a folder full of images into one folder per well with subfolders of red, green, and brightfield',
                                 usage='%(prog)s FOLDERPATH DAYinteger')
parser.add_argument("folderlocation", type=str,
                    help="Path of the folder to modify")
parser.add_argument("day", type=int,
                    help="Which day these pics are from, as just an integer (i.e. Day 3 would just be 3")

args = parser.parse_args()

# checking that the day value was given as a single integer
assert(type(args.day) == 'int'), "Need the day argument to be an integer"

# changing the working directory to the folder of interest
os.chdir(args.folderlocation)

# getting a list of all of the images in the folder, then making a list of all the wells represented
allimages = glob.glob('*.tif')
wells = set([name[0] + name[4:6] for name in allimages])

# making all the folders
for well in wells:
    makefolders(well)

# moving files into correct spots
for image in allimages:
    movepic(image)
