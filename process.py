# from gettext import np
import rasterio
import matplotlib.pyplot as plt
from rasterio import plot
from rasterio.plot import show
import numpy

def rgb(redFile, greenFile, blueFile):
    red = rasterio.open(redFile)
    green = rasterio.open(greenFile)
    blue = rasterio.open(blueFile)

    with rasterio.open('rgb.tiff','w',driver='Gtiff', width=blue.width, height=blue.height, count=3, crs=blue.crs,transform=blue.transform, dtype=blue.dtypes[0]) as rgb:
        rgb.write(blue.read(1),3) 
        rgb.write(green.read(1),2) 
        rgb.write(red.read(1),1) 
        rgb.close()

    src = rasterio.open(r'.\rgb.tiff')
    plt.figure(figsize=(6,6))
    plt.title('RGB')
    plot.show(src, adjust='linear')

def ndvi(redFile, nirFile):
    band_red = rasterio.open(redFile)
    band_nir = rasterio.open(nirFile)
    
    red = band_red.read(1).astype('float64')
    nir = band_nir.read(1).astype('float64')

    ndvi= numpy.where( (nir==0.) | (red ==0.), -255 , numpy.where((nir+red)==0., 0, (nir-red)/(nir+red)))

    src = rasterio.open('./ndvi.tiff', 'w', driver='Gtiff', width=band_red.width, height=band_red.height, count=1, crs=band_red.crs, transform=band_red.transform, dtype='float64')
    src.write(ndvi, 1)
    src.close()

    plt.figure(figsize=(6,6))
    plt.title('NDVI')
    plot.show(src, adjust='linear')
