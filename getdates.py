import urllib.request
import json

start_date = '2022-11-11T00:00:00.000Z'
end_date = '2023-08-11T23:59:59.999Z'

dates = []

def get_dates(page=1):
    already_collected_dates = len(dates)
    sat_url = f'https://catalogue.dataspace.copernicus.eu/resto/api/collections/Sentinel2/search.json?cloudCover=[0,30]&startDate={start_date}&completionDate={end_date}&sortParam=startDate&page={page}&geometry=POLYGON ((5.554850262125484 52.53996513567034, 5.555136972613241 52.5355639065524, 5.559451282798307 52.535622038868866, 5.559314753995039 52.54002326215965, 5.554850262125484 52.53996513567034))'.replace(' ', '%20')
    with urllib.request.urlopen(sat_url) as f:
        sat_data = json.load(f)

        for feature in sat_data['features']:
            if feature['properties']['startDate'] not in dates:
                dates.append(feature['properties']['startDate'])

        f.close()
    
    if (len(dates) - already_collected_dates) == 12:
        get_dates(page + 1)

get_dates()
print(dates)