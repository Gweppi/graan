"""probe"""
import openeo

def download(north, east, south, west):
  connection = openeo.connect("openeo.dataspace.copernicus.eu")
  connection.authenticate_oidc()

  datacube = connection.load_collection(
    "SENTINEL2_L2A",
    spatial_extent={"west": west,
                    "south": south,
                    "east": east,
                    "north": north
                    },
    temporal_extent=["2023-09-09", "2023-09-09"],
    bands=["B08", "B04"]
  )

  datacube = datacube.median_time()

  datacube = datacube.process(
    process_id="ndvi",
    arguments={
      "data": datacube,
      "red": "B04",
      "nir": "B08"
    }
  )

  result = datacube.save_result(format="GTiff")

  job = result.create_job()

  job.start_and_wait()
  job.get_results().download_files("output")
