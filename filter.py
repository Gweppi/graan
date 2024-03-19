import json
import urllib.request
import openeo
import datetime

start_date = '2022-11-11T00:00:00.000Z'
end_date = '2023-08-11T23:59:59.999Z'

def short_date(date: str):
  return date[0:10].replace('-', '')

def translate(value, leftMin, leftMax, rightMin, rightMax):
  # Figure out how 'wide' each range is
  leftSpan = leftMax - leftMin
  rightSpan = rightMax - rightMin

  # Convert the left range into a 0-1 range (float)
  valueScaled = float(value - leftMin) / float(leftSpan)

  # Convert the 0-1 range into a value in the right range.
  return rightMin + (valueScaled * rightSpan)

# Get weather data
with urllib.request.urlopen(f'https://www.daggegevens.knmi.nl/klimatologie/daggegevens?start={short_date(start_date)}&end={short_date(end_date)}&vars=TG:Q&stns=269&fmt=json') as f:
  weather_data = json.load(f)

  f.close()

# Filter dates
dates = ['2022-11-16T10:53:21.024Z', '2022-11-23T10:43:51.024Z', '2022-12-01T10:53:19.024Z', '2022-12-06T10:54:31.024Z', '2022-12-13T10:44:41.024Z', '2022-12-16T10:54:41.024Z', '2022-12-21T10:53:49.024Z', '2022-12-26T10:54:51.024Z', '2023-01-17T10:42:59.025Z', '2023-01-30T10:52:09.024Z', '2023-02-06T10:41:29.024Z', '2023-02-14T10:51:41.024Z', '2023-02-26T10:39:19.025Z', '2023-03-01T10:48:59.025Z', '2023-03-03T10:39:31.024Z', '2023-03-13T10:38:21.024Z', '2023-03-23T10:37:11.024Z', '2023-04-02T10:36:21.024Z', '2023-04-05T10:50:31.024Z', '2023-04-30T10:46:19.024Z', '2023-05-20T10:46:29.024Z', '2023-05-22T10:36:31.024Z', '2023-05-27T10:36:29.024Z', '2023-06-04T10:46:21.024Z', '2023-06-06T10:36:29.024Z', '2023-06-09T10:46:29.024Z', '2023-06-11T10:36:31.024Z', '2023-06-14T10:50:31.024Z', '2023-06-16T10:36:29.025Z', '2023-06-21T10:36:31.024Z', '2023-06-24T10:46:21.024Z']
# sat_url = f'https://catalogue.dataspace.copernicus.eu/resto/api/collections/Sentinel2/search.json?cloudCover=[0,30]&startDate={start_date}&completionDate={end_date}&sortParam=startDate&geometry=POLYGON ((5.554850262125484 52.53996513567034, 5.555136972613241 52.5355639065524, 5.559451282798307 52.535622038868866, 5.559314753995039 52.54002326215965, 5.554850262125484 52.53996513567034))'.replace(' ', '%20')
# with urllib.request.urlopen(sat_url) as f:
#     sat_data = json.load(f)

#     for feature in sat_data['features']:
#         if feature['properties']['startDate'] not in dates:
#             dates.append(feature['properties']['startDate'])

#     f.close()

# Connect to openeo
connection = openeo.connect("openeo.dataspace.copernicus.eu")
connection.authenticate_oidc()

# Run jobs
print(f'found {len(dates)} jobs to run')
for date in dates:
    sliced_date = date[0:10]

    aoi = {
        "type": "Polygon",
        "coordinates": [
          [
            [
              5.554850262125484,
              52.53996513567034
            ],
            [
              5.555136972613241,
              52.5355639065524
            ],
            [
              5.559451282798307,
              52.535622038868866
            ],
            [
              5.559314753995039,
              52.54002326215965
            ],
            [
              5.554850262125484,
              52.53996513567034
            ]
          ]
        ]
    }

    date = [sliced_date, sliced_date]

    public_url = "https://openeo.dataspace.copernicus.eu/openeo/1.1/processes/u:3e24e251-2e9a-438f-90a9-d4500e576574/EVI"

    evi = connection.datacube_from_process(
       "EVI",
       namespace=public_url,
       date=date,
       aoi=aoi
    )
 
    result = evi.save_result(format="GTiff")

    job = result.create_job()

    job.start_and_wait()
    job.get_results().download_files(f'output/{sliced_date}')

    # Add evi value
    with open(f'output/{sliced_date}/job-results.json') as f:
      metadata = json.load(f)
      evi_min = metadata['assets']['openEO.tif']['raster:bands'][0]['statistics']['minimum']
      evi_mean = metadata['assets']['openEO.tif']['raster:bands'][0]['statistics']['mean']
      evi_max = metadata['assets']['openEO.tif']['raster:bands'][0]['statistics']['maximum']

      evi_transformed = translate(evi_mean, evi_min, evi_max, 0, 1)

      for weather_date in weather_data:
        sliced_weather_date = weather_date['date'][0:10]
        result_sliced_date = metadata['extent']['temporal']['interval'][0][0][0:10]

        if sliced_weather_date == result_sliced_date:
          weather_date['EVI'] = evi_transformed

        with open(f'output.json', 'w') as w:
          json.dump(weather_data, w)
          w.close()
      f.close()