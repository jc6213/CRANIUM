#!/bin/env python
# This program takes a folder that has been formatted by the "WellFolders.py" script.
# This uses two ImageJ/Fiji macros to stitch together the images from the red channel and
# the green channel for each well, outputting the stitched images into a common folder
# which can be used subsequently for analysis in CellProfiler.

# Optionally, can also specify if you want only certain wells from the folder stitched, instead of
# the entire folder.

import argparse
import os
import re
import subprocess

# Making a function to stitch red and green images for a single well:
def makestitches(well, parentfolderpath):
    # Creating some variables to pass on to the ImageJ macro:
    red_folder = parentfolderpath + '/Red'
    green_folder = parentfolderpath + '/Green'
    red_format = well[0] + ' - ' + well[1:] + '(fld {ii} wv 561 - Orange).tif'
    tile_con = well + 'TileCon.txt'

    # Putting together the parts of the call:
    initial1 = str('/Applications/Fiji.app/Contents/MacOS/ImageJ-macosx --ij2 --headless --run /Users/jessecohn/Desktop/MacroTest.ijm ')
    passed_vars1 = str(f'\'dir1="{red_folder}",FileNames="{red_format}",TileCon="{tile_con}",dir2="{output_folder}"\'')
    quiet = str(' >/dev/null 2>&1')
    full_call1 = initial1 + passed_vars1 + quiet

    # Running the macro to stitch the red channel:
    subprocess.run(full_call, shell=True)

    # Altering the output registration text file to make it use green images file names, and writing it to the green folder
    with open(red_folder + '/' + well + 'TileCon.registered.txt', 'r') as file:
        filedata = file.read()
    filedata = filedata.replace('561 - Orange', '488 - GreenHS')
    with open(green_folder + '/' + well + 'TileCon.registered.txt', 'w') as file:
        file.write(filedata)




# Getting arguments from the command line
parser = argparse.ArgumentParser(description='Takes a folder formatted by WellFolders and makes stitched '
                                             'red and green images for each well in that folder (or each well '
                                             'specified. (Use the top-level folder, i.e. the one that contains all the '
                                             'well subfolders!)', usage='%(prog)s FOLDERPATH --wells A01 A02, etc')
parser.add_argument('folderlocation', type=str, help='Path of the folder to modify', required=True)
parser.add_argument('--wells', type=str, nargs='*', default='all', help='Wells to stitch (does all by default')
args = parser.parse_args()

# Changing the working directory to the folder of interest and making an output folder
os.chdir(args.folderlocation)
os.makedirs('Stitched_Images')
output_folder = os.path.abspath('Stitched_Images')

# Making a list of the wells to stitch:
if args.wells == 'all':
    regex = re.compile(r'^[A-H]\d{2}_Day\d$')
    allfolders = [a.name for a in os.scandir(args.folderlocation) if a.is_dir()]
    allwells = [b.split['_'][0] for b in allfolders if regex.match(b)]
else:
    allwells = [c[0] + c[1:].zfill(2) for c in args.wells]

#