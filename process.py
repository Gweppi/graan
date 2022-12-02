import folium
import geopandas as gpd
from sentinelsat.sentinel import SentinelAPI
import rasterio
import matplotlib.pyplot as plt
from rasterio import plot
from rasterio.plot import show

bands = r'.\S2A_MSIL2A_20220719T105041_N0400_R051_T31UFU_20220719T170208.SAFE\GRANULE\L2A_T31UFU_A036942_20220719T105038\IMG_DATA\R10m'
blue = rasterio.open(bands+'\T31UFU_20220719T105041_B02_10m.jp2')
green = rasterio.open(bands+'\T31UFU_20220719T105041_B03_10m.jp2')
red = rasterio.open(bands+'\T31UFU_20220719T105041_B04_10m.jp2')

with rasterio.open('rgb.tiff','w',driver='Gtiff', width=blue.width, height=blue.height, count=3, crs=blue.crs,transform=blue.transform, dtype=blue.dtypes[0]) as rgb:
    rgb.write(blue.read(1),3) 
    rgb.write(green.read(1),2) 
    rgb.write(red.read(1),1) 
    rgb.close()

src = rasterio.open(r'.\rgb.tiff')
plt.figure(figsize=(6,6))
plt.title('Final Image')
plot.show(src, adjust='linear')
