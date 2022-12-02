import folium
import geopandas as gpd
from sentinelsat.sentinel import SentinelAPI
import rasterio
import matplotlib.pyplot as plt
from rasterio import plot
from rasterio.plot import show
from rasterio.mask import mask
# from osgeo import gdal

print("Hello, World!")

m = folium.Map([5.644035710624621, 52.53289344790048], zoom_start=11)
boundary = gpd.read_file(r'./map.geojson')
folium.GeoJson(boundary).add_to(m)

footprint = None
for i in boundary['geometry']:
    footprint = i

user = 'jeppi'
password = 'pyxhus-cEggos-8sinto'

api = SentinelAPI(user, password, 'https://scihub.copernicus.eu/dhus')

products = api.query(footprint, platformname = 'Sentinel-2', processingLevel = 'Level-2A', cloudcoverpercentage = (0,25))

gdf = api.to_dataframe(products)
gdf_sorted = gdf.sort_values(['cloudcoverpercentage'], ascending = [True])
gdf_sorted = gdf_sorted.head(1)

# print(products)
api.download_all(gdf_sorted.index)
