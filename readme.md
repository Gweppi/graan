# grip

wget -O dates.json "https://catalogue.dataspace.copernicus.eu/resto/api/collections/Sentinel2/search.json?cloudCover=[0,10]&startDate=2023-09-01T00:00:00Z&completionDate=2023-12-31T23:59:59Z&sortParam=startDate&geometry=POLYGON ((5.738637 52.583717, 5.737457 52.580575, 5.741491 52.579962, 5.742778 52.58313, 5.738637 52.583717))"

perfect omlijnd:
POLYGON ((5.738637 52.583717, 5.737457 52.580575, 5.741491 52.579962, 5.742778 52.58313, 5.738637 52.583717))

mooi vierkant:
POLYGON ((5.737328 52.579936, 5.737328 52.583795, 5.742885 52.583795, 5.742885 52.579936, 5.737328 52.579936))

geojson:
{
    "type": "FeatureCollection",
    "features": [
      {
        "type": "Feature",
        "properties": {},
        "geometry": {
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
          ],
          "type": "Polygon"
        }
      }
    ]
  }