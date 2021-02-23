#!/bin/env python
# This program takes a folder that has been formatted by the "WellFolders.py" script.
# This uses two ImageJ/Fiji macros to stitch together the images from the red channel and
# the green channel for each well, outputting the stitched images into a common folder
# which can be used subsequently for analysis in CellProfiler.

# Optionally, can also specify if you want only certain wells from the folder stitched, instead of
# the entire folder.

# Call should be in the format:
# python3 StitchImages.py path/to/topfolder path/to/redmacro path/to/greenmacro --wells A01 A02

# The only thing hard-coded in that may need to be changed is the location of ImageJ
# (in initial1 and initial2 variables, lines 81 and 104), and the default location of your red/green macros
# if you don't want to have to specify every time.

import argparse
import os
import re
import subprocess


# A class for each folder that contains red and green image folders. Basically takes a DirEntry object
# from os.scandir() and adds some convenience attributes
class WellFolder:
    def __init__(self, folder):
        self.folderpath = folder.path
        self.red_dir = folder.path + '/Red'
        self.green_dir = folder.path + '/Green'
        self.well = folder.name[:3]
        self.row = folder.name[0]
        self.column = folder.name[1:3]


# Getting arguments from the command line
parser = argparse.ArgumentParser(description='Takes a folder formatted by WellFolders and makes stitched '
                                             'red and green images for each well in that folder (or each well '
                                             'specified. (Use the top-level folder, i.e. the one that contains all the '
                                             'well subfolders!)',
                                 usage='%(prog)s FOLDERPATH --REDMACROPATH --GREENMACROPATH --wells A01 A02, etc')
parser.add_argument('folderlocation', type=str, help='Absolute path of the folder to modify')
parser.add_argument('--redmacrolocation', type=str,
                    default='/Users/jessecohn/Desktop/PythonScripts/CRANIUM/RedStitch.ijm',
                    help='Absolute path to the RedStitch.ijm macro')
parser.add_argument('--greenmacrolocation', type=str,
                    default='/Users/jessecohn/Desktop/PythonScripts/CRANIUM/GreenStitch.ijm',
                    help='Absolute path to the GreenStitch.ijm macro')
parser.add_argument('--wells', type=str, nargs='*', default='all', help='Wells to stitch (does all by default',
                    required=False)
args = parser.parse_args()

# Making the shared output folder. If it already exists and some wells have already been stitched,
# this will make a list of already stitched images in order to avoid doing them again
output_folder = args.folderlocation + '/Stitched_Images'
existing_well_images = []
try:
    os.makedirs(output_folder)
except FileExistsError:
    existing_well_images = {pic[:3] for pic in os.listdir(output_folder)}
    pass

# Making a list of the folders with pics to stitch:
# First getting all wells folders:
regex = re.compile(r'^[A-H]\d{2}_Day\d$')
wanted_folders = [file for file in os.scandir(args.folderlocation) if file.is_dir() and regex.match(file.name)]
# Then filtering them if the --wells tag was used
if args.wells != 'all':
    passed_wells = [m[0] + m[1:].zfill(2) for m in args.wells]
    wanted_folders = [folder for folder in wanted_folders if folder.name[:3] in passed_wells]

# Looping through the well folders and stitching the images:
for folder in wanted_folders:
    well_obj = WellFolder(folder)
    if well_obj.well in existing_well_images:
        print(f'Skipping well {well_obj.well}, stitched images already exist')
    else:
        # Creating some variables to pass on to the ImageJ macros:
        red_format = well_obj.row + ' - ' + well_obj.column + '(fld {ii} wv 561 - Orange).tif'
        registrationfile1 = well_obj.well + 'TileConRed.txt'
        registrationfile2 = well_obj.well + 'TileConRed.registered.txt'
        registrationfile3 = well_obj.well + 'TileConGreen.registered.txt'
        end_file_name = 'img_t1_z1_c1'

        # Putting together the parts of the first call to stitch the red images:
        initial1 = str(f'/Applications/Fiji.app/Contents/MacOS/ImageJ-macosx --ij2 '
                       f'--headless --run {args.redmacrolocation} ')
        passed_vars1 = str(f'\'dir1="{well_obj.red_dir}",FileNames="{red_format}",'
                           f'TileCon="{registrationfile1}",dir2="{output_folder}"\'')
        quiet = str(' >/dev/null 2>&1')
        full_call1 = initial1 + passed_vars1 + quiet

        # Running the macro to stitch the red channel:
        print(f'Stitching the red images for {well_obj.well}')
        subprocess.run(full_call1, shell=True)

        # Changing the name of the output file
        os.rename(f'{output_folder}/{end_file_name}', f'{output_folder}/{well_obj.well}_Red_Stitched.tif')

        # Altering the output registration text file to make it use green images file names,
        # and writing it to the green folder
        with open(f'{well_obj.red_dir}/{registrationfile2}', 'r') as file:
            filedata = file.read()
        filedata = filedata.replace('561 - Orange', '488 - GreenHS')
        with open(f'{well_obj.green_dir}/{registrationfile3}', 'w') as file:
            file.write(filedata)

        # Putting together the parts of the second call to stitch the green images:
        initial2 = str(f'/Applications/Fiji.app/Contents/MacOS/ImageJ-macosx --ij2 '
                       f'--headless --run {args.greenmacrolocation} ')
        passed_vars2 = str(f'\'dir1="{well_obj.green_dir}",TileCon="{registrationfile3}",'
                           f'dir2="{output_folder}"\'')
        full_call2 = initial2 + passed_vars2 + quiet

        # Running the macro to stitch the green channel:
        print(f'Stitching the green images for {well_obj.well}')
        subprocess.run(full_call2, shell=True)

        # Changing the name of the output file
        os.rename(f'{output_folder}/{end_file_name}', f'{output_folder}/{well_obj.well}_Green_Stitched.tif')

print("Done stitching images for folders " + ', '.join([well.name for well in wanted_folders]))
