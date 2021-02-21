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


# A class for each folder that contains red and green image folders.
class WellFolder:
    def __init__(self, folder):
        self.folderpath = folder.path
        self.red_dir = folder.path + '/Red'
        self.green_dir = folder.path + '/Green'
        self.well = folder.name[:3]
        self.row = folder.name[0]
        self.column = folder.name[1:3]


# A function to stitch red and green images for a single well folder and output to the shared output folder:
def makestitches(well_obj):
    # Creating some variables to pass on to the ImageJ macro:
    red_format = well_obj.row + ' - ' + well_obj.column + '(fld {ii} wv 561 - Orange).tif'
    registrationfile1 = well_obj.well + 'TileCon.txt'
    registrationfile2 = well_obj.well + 'TileCon.registered.txt'

    # Putting together the parts of the first call to stitch the red images:
    initial1 = str('/Applications/Fiji.app/Contents/MacOS/ImageJ-macosx --ij2 '
                   '--headless --run /Users/jessecohn/Desktop/MacroTest.ijm ')
    passed_vars1 = str(f'\'dir1="{well_obj.red_dir}",FileNames="{red_format}",'
                       f'TileCon="{registrationfile1}",dir2="{output_folder}"\'')
    quiet = str(' >/dev/null 2>&1')
    full_call1 = initial1 + passed_vars1 + quiet

    # Running the macro to stitch the red channel:
    subprocess.run(full_call1, shell=True)

    # Altering the output registration text file to make it use green images file names,
    # and writing it to the green folder
    with open(f'{well.red_dir}/{registrationfile2}', 'r') as file:
        filedata = file.read()
    filedata = filedata.replace('561 - Orange', '488 - GreenHS')
    with open(f'{well.green_dir}/{registrationfile2}', 'w') as file:
        file.write(filedata)

    # Putting together the parts of the second call to stitch the green images:
    green_format = well_obj.row + '-' + well_obj.column + '(fld {ii} wv 488 - GreenHS.tif'
    

# Getting arguments from the command line
parser = argparse.ArgumentParser(description='Takes a folder formatted by WellFolders and makes stitched '
                                             'red and green images for each well in that folder (or each well '
                                             'specified. (Use the top-level folder, i.e. the one that contains all the '
                                             'well subfolders!)', usage='%(prog)s FOLDERPATH --wells A01 A02, etc')
parser.add_argument('folderlocation', type=str, help='Absolute path of the folder to modify', required=True)
parser.add_argument('--wells', type=str, nargs='*', default='all', help='Wells to stitch (does all by default')
args = parser.parse_args()

# Making the shared output folder
output_folder = args.folderlocation + '/Stitched_Images'
os.makedirs(output_folder)

# Making a list of the folders with pics to stitch:
# First getting all wells folders:
regex = re.compile(r'^[A-H]\d{2}_Day\d$')
wanted_folders = [file for file in os.scandir(args.folderlocation) if file.is_dir() and regex.match(file.name)]
# Then filtering them if the --wells tag was used
if args.wells != 'all':
    passed_wells = [m[0] + m[1:].zfill(2) for m in args.wells]
    wanted_folders = [folder for folder in wanted_folders if folder.name[:3] in passed_wells]

# Calling the stitching command on all the passed folders:
for well in wanted_folders:
    makestitches(WellFolder(well))
