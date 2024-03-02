"""process image"""

import json
from geotiff import GeoTiff

def process_image(image_path, crs_code):
    # Open GTiff
    tiff_file = "output/openEO.tif"
    geo_tiff = GeoTiff(tiff_file, crs_code=crs_code, as_crs=crs_code)

    # Select area
    area_box = [(5.654634669748851, 52.5084695155183), (5.716226103790471, 52.543503102976246)]
    array = geo_tiff.read_box(area_box)
    print(array)

    # print bboc
    print(geo_tiff.tif_bBox)



# Open JSON file with info about image
def get_crs_code():
    with open("output/job-results.json") as json_file:
        job_results = json.load(json_file)
        crs_code = job_results["assets"]["openEO.tif"]["proj:epsg"]
        return crs_code

process_image("output/openEO.tif", crs_code=get_crs_code())