import json
import urllib.request

start_date = '2022-09-01T00:00:00.000Z'
end_date = '2022-12-31T23:59:59.999Z'

def short_date(date: str):
  return date[0:10].replace('-', '')

weather_url = f'https://www.daggegevens.knmi.nl/klimatologie/daggegevens?start={short_date(start_date)}&end={short_date(end_date)}&vars=TG:Q&stns=269&fmt=json'
with urllib.request.urlopen(weather_url) as f:
    weather_dates = json.load(f)

    rg = []
    for weather_date in weather_dates:
        rg.append(weather_date['Q'])

    f.close()

    sum_rg = sum(rg) / 0.01 # 0.01 is the conversion factor
    dam = 105 * 1_000_000

    elue = dam / sum_rg

    print(elue)