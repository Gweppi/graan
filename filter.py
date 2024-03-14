import json
import urllib.request
import openeo
import datetime

start_date = '2022-09-01T00:00:00.000Z'
end_date = '2022-10-31T23:59:59.999Z'

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
dates = []
sat_url = f'https://catalogue.dataspace.copernicus.eu/resto/api/collections/Sentinel2/search.json?cloudCover=[0,10]&startDate={start_date}&completionDate={end_date}&sortParam=startDate&geometry=POLYGON ((5.738637 52.583717, 5.737457 52.580575, 5.741491 52.579962, 5.742778 52.58313, 5.738637 52.583717))'.replace(' ', '%20')
with urllib.request.urlopen(sat_url) as f:
    sat_data = json.load(f)

    for feature in sat_data['features']:
        if feature['properties']['startDate'] not in dates:
            dates.append(feature['properties']['startDate'])

    f.close()

# Connect to openeo
connection = openeo.connect("openeo.dataspace.copernicus.eu")
connection.authenticate_oidc()

# Run jobs
print(f'found {len(dates)} jobs to run')
for date in dates:
    sliced_date = date[0:10]

    # aoi = {
    #     "type": "Polygon",
    #     "coordinates": [
    #         [
    #           [
    #             5.738673553481362,
    #             52.58376931677191
    #           ],
    #           [
    #             5.737582044866684,
    #             52.58080431536172
    #           ],
    #           [
    #             5.741627047380092,
    #             52.58018007898258
    #           ],
    #           [
    #             5.742782762384593,
    #             52.58315487571764
    #           ],
    #           [
    #             5.738673553481362,
    #             52.58376931677191
    #           ]
    #         ]
    #       ]
    # }

    # date = [sliced_date, sliced_date]

    # public_url = "https://openeo.dataspace.copernicus.eu/openeo/1.1/processes/u:3e24e251-2e9a-438f-90a9-d4500e576574/EVI"

    # evi = connection.datacube_from_process(
    #    "EVI",
    #    namespace=public_url,
    #    date=date,
    #    aoi=aoi
    # )

    # result = evi.save_result(format="GTiff")

    # job = result.create_job()

    # job.start_and_wait()
    # job.get_results().download_files(f'output/{sliced_date}')

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
          print(f'{sliced_weather_date}, {result_sliced_date}')
          if sliced_weather_date == result_sliced_date:
            weather_date['EVI'] = evi_transformed

        with open(f'output.json', 'w') as w:
          json.dump(weather_data, w)
          w.close()