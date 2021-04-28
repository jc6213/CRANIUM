# Uses the StarDist machine learning program to make label images for all green channel photos in subfolders
# of a folder. Used for analyzing images of iPSC nuclei (does a better job at segmenting the nuclei than CellProfiler
# or the InCarta software). These label images can be imported as images of objects into CellProfiler for further
# analysis.

import os
import argparse
import glob
import sys
import numpy as np
from tifffile import imread
from csbdeep.utils import Path, normalize
from csbdeep.io import save_tiff_imagej_compatible
from stardist import _draw_polygons, export_imagej_rois
from stardist.models import StarDist2D


# Getting the location of the folder from the command line:
parser = argparse.ArgumentParser(description='Uses StarDist to create label images for all of the images '
                                             'in a directory, keeping them grouped as they are in the parent folder',
                                 usage='%(prog)s FOLDERPATH')
parser.add_argument("folderlocation", type=str, help="Path of the folder with images")
args = parser.parse_args()

# Making the output folder in the parent directory if it doesn't exist
outputfolder = os.path.dirname(args.folderlocation) + '/labelimages'
if not os.path.exists(outputfolder):
    os.makedirs(outputfolder)

# Instantiating the StarDist model. Using the '2D_versatile_fluo' pre-trained model. I tried several settings on
# the images and found that these parameters work best:
# Normalize the image with a lower threshold of 40 and an upper threshold of 100
# Probability threshold of 0.25, overlap threshold of 0.3

model = StarDist2D.from_pretrained('2D_versatile_fluo')

folder = args.folderlocation
print(f'Working on {folder}')
outdir = outputfolder + '/' + os.path.basename(folder) + '_labels'
os.makedirs(outdir)
greenimagesnames = sorted(glob.glob(folder + '/*.tif'))
greenimages = map(imread, greenimagesnames)
for tif, loc in zip(greenimages, greenimagesnames):
    saveloc = outdir + '/' + os.path.splitext(os.path.basename(loc))[0] + '_labels.tif'
    img = normalize(tif, 40, 100, axis=(0, 1))
    labels, _ = model.predict_instances(img, prob_thresh=0.25, nms_thresh=0.3)
    save_tiff_imagej_compatible(saveloc, labels, axes='YX')

print(f'Done with {folder}.')