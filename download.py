import os
import folium
import geopandas as gpd
from sentinelsat.sentinel import SentinelAPI
from pathlib import Path
from unzip import unzip

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

m = folium.Map([5.644035710624621, 52.53289344790048], zoom_start=11)
path = Path(__file__).with_name('map.geojson')
print(path)
boundary = gpd.read_file(path)
folium.GeoJson(boundary).add_to(m)

footprint = None
for i in boundary['geometry']:
    footprint = i

user = os.getenv('USER')
password = os.getenv('PASSWORD')

api = SentinelAPI(user, password, 'https://scihub.copernicus.eu/dhus')

products = api.query(footprint, platformname = 'Sentinel-2', processingLevel = 'Level-2A', cloudcoverpercentage = (0,25))

gdf = api.to_dataframe(products)
gdf_sorted = gdf.sort_values(['cloudcoverpercentage'], ascending = [True])
gdf_sorted = gdf_sorted.head(1)

api.download_all(gdf_sorted.index)

unzip()