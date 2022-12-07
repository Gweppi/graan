import rasterio
import matplotlib.pyplot as plt
from rasterio import plot
from rasterio.plot import show

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
    plt.title('Final Image')
    plot.show(src, adjust='linear')
