import os
from glob import glob
import zipfile
from pathlib import Path
from process import rgb

def searchImages():
    datafolders = [ f.path for f in os.scandir(os.getcwd()) if f.is_dir() ]

    dir = datafolders[0] + '/GRANULE'

    imagefolders = [ f.path for f in os.scandir(dir) if f.is_dir() ]

    imagefolder = imagefolders[0] + '/IMG_DATA/R10m/'

    images = os.listdir(imagefolder)
    
    red = ''
    green = ''
    blue = ''

    for image in images:
        if 'B02' in image:
            red = imagefolder + image
        if 'B03' in image:
            green = imagefolder + image
        if 'B04' in image:
            blue = imagefolder + image

    rgb(red, green, blue)

searchImages()
