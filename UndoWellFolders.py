#!/bin/env python

# This script undoes the "WellFolders.py" script, aka it empties all of the well folders out into the parent folder.

import os
import re
import argparse

parser = argparse.ArgumentParser(description='Takes a folder formatted by WellFolders and undoes it ',
                                 usage='%(prog)s FOLDERPATH')
parser.add_argument('folderlocation', type=str, help='Absolute path of the folder to modify')
args = parser.parse_args()

regex = re.compile(r'\w{1}\d{2}_Day\d{1}')
allfolders = [file for file in os.scandir(args.folderlocation) if file.is_dir() and regex.match(file.name)]

for folder in allfolders:
    redfolder = folder.path + '/Red/'
    greenfolder = folder.path + '/Green/'
    brightfield = folder.path + '/Brightfield/'

    for foldpath in [redfolder, greenfolder, brightfield]:
        for file in os.scandir(foldpath):
            if file.name.endswith('.txt'):
                os.remove(file.path)
            elif file.name.endswith('.tif'):
                os.rename(file.path, f'{args.folderlocation}/{file.name}')
        os.rmdir(foldpath)

    os.rmdir(folder.path)
