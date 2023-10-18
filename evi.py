"""evi"""
import openeo

connection = openeo.connect("openeo.dataspace.copernicus.eu")
connection.authenticate_oidc()

datacube = connection.load_collection(
  "SENTINEL2_L2A",
  spatial_extent={"west": 5.654634669748851,
                  "south": 52.5084695155183,
                  "east": 5.716226103790471,
                  "north": 52.543503102976246
                  },
  temporal_extent=["2023-09-09", "2023-09-09"],
  bands=["B02", "B04", "B08"]
)

datacube = datacube.median_time()

B02 = datacube.band('B02')
B04 = datacube.band('B04')
B08 = datacube.band('B08')

evi_cube = (2.5 * (B08 - B04)) / ((B08 + 6.0 * B04 - 7.5 * B02) + 1.0)

result = evi_cube.save_result(format="GTiff")

job = result.create_job()

job.start_and_wait()
job.get_results().download_files("output")
