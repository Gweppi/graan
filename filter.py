import json
import openeo
import datetime

# Filter dates
dates = []
with open('dates.json') as f:
    data = json.load(f)

    for feature in data['features']:

        if feature['properties']['startDate'] not in dates:
            dates.append(feature['properties']['startDate'])
    
    f.close()

# Connect to openeo
connection = openeo.connect("openeo.dataspace.copernicus.eu")
connection.authenticate_oidc()

# Run jobs
for date in dates:
    sliced_date = date[0:10]

    aoi = {
        "type": "Polygon",
        "coordinates": [
            [
              [
                5.738673553481362,
                52.58376931677191
              ],
              [
                5.737582044866684,
                52.58080431536172
              ],
              [
                5.741627047380092,
                52.58018007898258
              ],
              [
                5.742782762384593,
                52.58315487571764
              ],
              [
                5.738673553481362,
                52.58376931677191
              ]
            ]
          ]
    }

    date = [sliced_date, sliced_date]

    public_url = "https://openeo.dataspace.copernicus.eu/openeo/1.1/processes/u:3e24e251-2e9a-438f-90a9-d4500e576574/EVI"

    evi = connection.datacube_from_process(
        "EVI",
       namespace= public_url,
       date=date,
       aoi=aoi
    )

    result = evi.save_result(format="GTiff")

    job = result.create_job()

    job.start_and_wait()
    job.get_results().download_files("output")